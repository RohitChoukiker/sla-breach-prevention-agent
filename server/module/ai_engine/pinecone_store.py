import os
from pinecone import Pinecone


class PineconeService:

    def __init__(self):
        print("[Pinecone] Initializing PineconeService...")

        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY not found in environment variables")

        self.pc = Pinecone(api_key=api_key)

        index_name = os.getenv("PINECONE_INDEX", "sla-tickets")

        self.index = self.pc.Index(index_name)

        print(f"[Pinecone] Connected to index: {index_name}")

    

    def upsert_embedding(self, state):

        namespace = state.get("tenant_id") or "default"

        print(f"[Pinecone] Upserting embedding for ticket_id: {state['ticket_id']}")

        self.index.upsert(
            vectors=[
                {
                    "id": state["ticket_id"],
                    "values": state["embedding"],
                    "metadata": {
                        "tenant_id": namespace
                    }
                }
            ],
            namespace=namespace
        )

        print("[Pinecone] Upsert complete.")

    # ----------------------------------------
    # QUERY SIMILAR
    # ----------------------------------------

    def query_similar(self, embedding, namespace="default", top_k=5):

        namespace = namespace or "default"

        print("[Pinecone] Querying similar vectors...")

        try:

            result = self.index.query(
                vector=embedding,
                top_k=top_k,
                namespace=namespace
            )

            matches = result.matches if result and result.matches else []

            print(f"[Pinecone] Found {len(matches)} similar vectors")

            return matches

        except Exception as e:

            print("[Pinecone ERROR]", e)

            return []