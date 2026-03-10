from sentence_transformers import SentenceTransformer
import torch

MODEL = None


class EmbeddingService:

    @staticmethod
    def load_model():

        global MODEL

        if MODEL is None:

            print("[Embedding] Loading model...")

            torch.set_num_threads(1)

            MODEL = SentenceTransformer(
                "all-MiniLM-L6-v2",
                device="cpu"
            )

            print("[Embedding] Model loaded")

        return MODEL

    @staticmethod
    def generate(text: str):

        model = EmbeddingService.load_model()

        with torch.no_grad():

            embedding = model.encode(
                text,
                convert_to_numpy=True,
                normalize_embeddings=True
            )

        return embedding.tolist()