from sentence_transformers import SentenceTransformer

class EmbeddingService:
    _model = None

    @classmethod
    def load(cls):
        if cls._model is None:
            cls._model = SentenceTransformer("all-MiniLM-L6-v2")
        return cls._model

    @classmethod
    def generate(cls, text: str):
        model = cls.load()
        return model.encode(text).tolist()
