from .faiss_store import FAISSStore

class VectorStoreFactory:

    @staticmethod
    def get_vectorstore(store='faiss'):

        if store == 'faiss':

            return FAISSStore()
        
        raise ValueError("Unknown vector store")