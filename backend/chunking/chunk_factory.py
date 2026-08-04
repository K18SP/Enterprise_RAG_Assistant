from .recursive_chunker import RecursiveChunker
from .token_chunker import TokenChunker

from config.constants import CHUNKING_STRATEGY

class ChunkFactory:

    @staticmethod
    def get_chunker(strategy=CHUNKING_STRATEGY):

        if strategy == "recursive":
            return RecursiveChunker()

        elif strategy == "token":
            return TokenChunker()

        else:
            raise ValueError( f"Unknown strategy: {strategy}" )