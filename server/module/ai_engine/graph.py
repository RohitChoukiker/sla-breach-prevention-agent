from langgraph.graph import StateGraph, END
from models.ticket import Ticket

from .state import TicketState
from .embedding import EmbeddingService
from .pinecone_store import PineconeService
from .scoring import calculate_breach_probability, calculate_priority
from .llm_node import llm_reasoning
from .audit import log_trace
from .email_service import send_escalation_email


def build_graph(db):

    pinecone = PineconeService()

    # -------------------------
    # LOAD TICKET
    # -------------------------
    def load_ticket(state):

        ticket = db.query(Ticket).filter(
            Ticket.id == state["ticket_id"]
        ).first()

        state["description"] = ticket.description
        state["urgency"] = ticket.urgency_requested
        state["tenant_id"] = ticket.tenant_id
        state["loop_count"] = 0

        return state

    # -------------------------
    # EMBEDDING
    # -------------------------
    def embed(state):

        print("[Graph] Embedding step started")

        try:

            state["embedding"] = EmbeddingService.generate(
                state["description"]
            )

        except Exception as e:

            print("[Embedding ERROR]", e)

            state["embedding"] = [0.0] * 384

        return state

    # -------------------------
    # STORE EMBEDDING
    # -------------------------
    def store(state):

        try:

            pinecone.upsert_embedding(state)

            print("[Pinecone] Embedding stored")

        except Exception as e:

            print("[Pinecone UPSERT ERROR]", e)

        return state

    # -------------------------
    # RETRIEVE CONTEXT
    # -------------------------
    def retrieve(state):

        namespace = state.get("tenant_id") or "default"

        matches = pinecone.query_similar(
            state["embedding"],
            namespace=namespace
        )

        state["similar_count"] = len(matches)

        print(
            f"[Graph] Similar tickets found: {state['similar_count']}"
        )

        return state

    # -------------------------
    # LLM REASONING
    # -------------------------
    def llm_node(state):

        return llm_reasoning(state)

    # -------------------------
    # CONFIDENCE ROUTER
    # -------------------------
    def confidence_router(state):

        print(
            "[Router] confidence:",
            state["confidence_score"],
            "loop:",
            state.get("loop_count")
        )

        if "loop_count" not in state:
            state["loop_count"] = 0

        if state["confidence_score"] < 0.60:

            if state["loop_count"] >= 2:

                print("[Router] Max retries reached")

                return "continue"

            state["loop_count"] += 1

            print("[Router] Retrying retrieval")

            return "retry"

        return "continue"

    # -------------------------
    # HYBRID SCORING
    # -------------------------
    def hybrid_scoring(state):

        deterministic_prob = calculate_breach_probability(
            state["urgency"],
            state["similar_count"]
        )

        final_prob = max(
            deterministic_prob,
            state["breach_probability"]
        )

        state["breach_probability"] = final_prob

        state["priority"] = calculate_priority(final_prob)

        print(
            "[Graph] Final probability:",
            state["breach_probability"]
        )

        return state

    # -------------------------
    # ESCALATION ROUTER
    # -------------------------
    def escalation_router(state):

        if state["breach_probability"] > 0.80:

            print("[Router] Escalation triggered")

            return "escalate"

        return "persist"

    # -------------------------
    # EMAIL NODE
    # -------------------------
    def email_node(state):

        print("[Graph] Sending escalation email")

        send_escalation_email(state)

        return state

    # -------------------------
    # PERSIST RESULTS
    # -------------------------
    def persist(state):

        ticket = db.query(Ticket).filter(
            Ticket.id == state["ticket_id"]
        ).first()

        ticket.breach_probability = state["breach_probability"]
        ticket.confidence_score = state["confidence_score"]
        ticket.priority_final = state["priority"]
        ticket.processing_status = "completed"

        if state["breach_probability"] > 0.80:

            ticket.status = "escalated"

        db.commit()

        log_trace(state)

        print("[Graph] Ticket updated")

        return state

    # -------------------------
    # BUILD GRAPH
    # -------------------------

    graph = StateGraph(TicketState)

    graph.add_node("load", load_ticket)
    graph.add_node("embed", embed)
    graph.add_node("store", store)
    graph.add_node("retrieve", retrieve)
    graph.add_node("llm", llm_node)
    graph.add_node("hybrid", hybrid_scoring)
    graph.add_node("email", email_node)
    graph.add_node("persist", persist)

    graph.set_entry_point("load")

    graph.add_edge("load", "embed")
    graph.add_edge("embed", "store")
    graph.add_edge("store", "retrieve")
    graph.add_edge("retrieve", "llm")

    graph.add_conditional_edges(
        "llm",
        confidence_router,
        {
            "retry": "retrieve",
            "continue": "hybrid"
        }
    )

    graph.add_conditional_edges(
        "hybrid",
        escalation_router,
        {
            "escalate": "email",
            "persist": "persist"
        }
    )

    graph.add_edge("email", "persist")
    graph.add_edge("persist", END)

    return graph.compile()