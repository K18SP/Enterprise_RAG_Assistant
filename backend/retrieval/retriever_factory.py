from .similarity_retriever import SimilarityRetriever

from .mmr_retriever import MMRRetriever

class RetrieverFactory:

    @staticmethod
    def get_retriever(vector_db,retriever='similarity'):

        if retriever == 'similarity':

            return SimilarityRetriever(vector_db)

        elif retriever == 'mmr':

            return MMRRetriever(vector_db)

        raise ValueError("Unsupported Retriever")
