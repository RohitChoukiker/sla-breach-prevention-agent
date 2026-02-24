

# module/ai_engine/retrieval.py

from sqlalchemy import text

class RetrievalService:

    def retrieve_similar(self, db, embedding, limit=5):

        results = db.execute(
            text("""
            SELECT id
            FROM tickets
            WHERE embedding IS NOT NULL
            ORDER BY embedding <-> :embedding
            LIMIT :limit
            """),
            {"embedding": embedding, "limit": limit}
        ).fetchall()

        return len(results)
