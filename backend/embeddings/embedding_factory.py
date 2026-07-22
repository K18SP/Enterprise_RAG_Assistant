from .huggingface_embedding import HuggingFaceEmbedding


class EmbeddingFactory:

    @staticmethod
    def get_embedding(model="huggingface"):

        if model == "huggingface":
            return HuggingFaceEmbedding()

        raise ValueError("Unsupported embedding model")