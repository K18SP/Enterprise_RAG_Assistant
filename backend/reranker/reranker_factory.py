from .cross_encoder_reranker import CrossEncoderReranker
from .base_reranker import BaseReranker

from config.constants import RERANKER

class RerankerFactory:

    @staticmethod
    def get_reranker(reranker: str = RERANKER) -> BaseReranker:

        reranker = reranker.lower()

        if reranker.lower() == "cross_encoder":

            return CrossEncoderReranker()

        raise ValueError(
            f"Unsupported Reranker: {reranker}"
        )