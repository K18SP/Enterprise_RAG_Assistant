from .cross_encoder_reranker import CrossEncoderReranker


class RerankerFactory:

    @staticmethod
    def get_reranker(reranker: str = "cross_encoder"):

        if reranker.lower() == "cross_encoder":

            return CrossEncoderReranker()

        raise ValueError(
            f"Unsupported Reranker: {reranker}"
        )