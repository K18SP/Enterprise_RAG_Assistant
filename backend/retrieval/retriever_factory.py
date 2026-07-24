from .similarity_retriever import SimilarityRetriever

from .mmr_retriever import MMRRetriever

from config.constants import RETRIEVER

class RetrieverFactory:

    @staticmethod
    def get_retriever(vector_db,retriever=RETRIEVER):

        retriever = retriever.lower()

        if retriever == 'similarity':

            return SimilarityRetriever(vector_db)

        if retriever == 'mmr':

            return MMRRetriever(vector_db)

        raise ValueError("Unsupported Retriever")
