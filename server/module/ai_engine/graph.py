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

    def load_ticket(state):
        ticket = db.query(Ticket).filter(
            Ticket.id == state["ticket_id"]
        ).first()

        state["description"] = ticket.description
        state["urgency"] = ticket.urgency_requested
        state["tenant_id"] = ticket.tenant_id
        state["loop_count"] = 0
        return state

  
    def embed(state):
        state["embedding"] = EmbeddingService.generate(
            state["description"]
        )
        return state


    def retrieve(state):
        matches = pinecone.query_similar(
            state["embedding"],
            namespace=state["tenant_id"]
        )

        state["similar_count"] = len(matches)
        return state

    def llm_node(state):
        return llm_reasoning(state)

   
    def confidence_router(state):

        if state["confidence_score"] < 0.60 and state["loop_count"] < 2:
            state["loop_count"] += 1
            return "retry"

        return "continue"

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
        return state

   
    def escalation_router(state):

        if state["breach_probability"] > 0.80:
            return "escalate"

        return "persist"

    def email_node(state):
        send_escalation_email(state)
        return state

 
    def persist(state):

        ticket = db.query(Ticket).filter(
            Ticket.id == state["ticket_id"]
        ).first()

        ticket.breach_probability = state["breach_probability"]
        ticket.confidence_score = state["confidence_score"]
        ticket.priority_final = state["priority"]

        if state["breach_probability"] > 0.80:
            ticket.status = "escalated"

        db.commit()

        log_trace(state)
        return state

  
    graph = StateGraph(TicketState)

    graph.add_node("load", load_ticket)
    graph.add_node("embed", embed)
    graph.add_node("retrieve", retrieve)
    graph.add_node("llm", llm_node)
    graph.add_node("hybrid", hybrid_scoring)
    graph.add_node("email", email_node)
    graph.add_node("persist", persist)

    graph.set_entry_point("load")

    graph.add_edge("load", "embed")
    graph.add_edge("embed", "retrieve")
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
