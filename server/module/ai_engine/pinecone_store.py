import os
from pinecone import Pinecone

class PineconeService:

    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index = self.pc.Index("sla-tickets")

    def upsert_embedding(self, state):
        self.index.upsert(
            vectors=[{
                "id": state["ticket_id"],
                "values": state["embedding"],
                "metadata": {"tenant_id": state["tenant_id"]}
            }],
            namespace=state["tenant_id"]
        )

    def query_similar(self, state, top_k=5):
        result = self.index.query(
            vector=state["embedding"],
            top_k=top_k,
            namespace=state["tenant_id"]
        )
        return len(result.matches)
