from config.constants import EMBEDDING_MODEL

from .huggingface_embedding import HuggingFaceEmbedding


class EmbeddingFactory:

    @staticmethod
    def get_embedding(
        provider: str = "huggingface"
    ):

        provider = provider.lower()

        if provider == "huggingface":

            return HuggingFaceEmbedding(
                model_name=EMBEDDING_MODEL
            )

        raise ValueError(
            f"Unsupported embedding provider: {provider}"
        )