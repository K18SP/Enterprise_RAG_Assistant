from vectordb.faiss_store import FAISSStore


class VectorStoreFactory:

    @staticmethod
    def get_vectorstore(
        embedding,
        vectorstore,
        save_path
    ):

        vectorstore = vectorstore.lower()

        if vectorstore == "faiss":

            return FAISSStore(
                embedding=embedding,
                save_path=save_path
            )

        raise ValueError(
            f"Unsupported vector store: {vectorstore}"
        )