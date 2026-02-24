from .graph import build_graph

class AIEngine:

    def process_ticket(self, db, ticket_id):

        graph = build_graph(db)

        initial_state = {
            "ticket_id": ticket_id,
            "tenant_id": "",
            "description": "",
            "urgency": "",
            "embedding": [],
            "similar_count": 0,
            "breach_probability": 0.0,
            "confidence_score": 0.0,
            "priority": "",
            "escalation_required": False,
            "loop_count": 0
        }

        return graph.invoke(initial_state)
