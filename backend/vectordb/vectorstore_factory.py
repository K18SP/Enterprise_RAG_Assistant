from .faiss_store import FAISSStore
from .base_vectorstore import BaseVectorStore

from config.constants import VECTORSTORE


class VectorStoreFactory:

    @staticmethod
    def get_vectorstore(
        embedding,
        vectorstore=VECTORSTORE
    )-> BaseVectorStore:

        vectorstore = vectorstore.lower()

        if vectorstore == "faiss":

            return FAISSStore(embedding)

        raise ValueError(
            f"Unsupported Vector Store: {vectorstore}"
        )