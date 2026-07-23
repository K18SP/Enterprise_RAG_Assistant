from .faiss_store import FAISSStore


class VectorStoreFactory:

    @staticmethod
    def get_vectorstore(
        embedding,
        vectorstore="faiss"
    ):

        if vectorstore.lower() == "faiss":

            return FAISSStore(embedding)

        raise ValueError(
            f"Unsupported Vector Store: {vectorstore}"
        )