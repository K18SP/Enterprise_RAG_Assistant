from .faiss_store import FAISSStore
from .base_vectorstore import BaseVectorStore

from config.constants import VECTORSTORE

from config.constants import VECTOR_DB_SAVE_PATH


class VectorStoreFactory:

    @staticmethod
    def get_vectorstore(
        embedding,
        vectorstore=VECTORSTORE
    )-> BaseVectorStore:

        vectorstore = vectorstore.lower()

        if vectorstore == "faiss":

            return FAISSStore(embedding = embedding,save_path = VECTOR_DB_SAVE_PATH)

        raise ValueError(
            f"Unsupported Vector Store: {vectorstore}"
        )