from .recursive_chunker import RecursiveChunker
from .token_chunker import TokenChunker


class ChunkFactory:

    @staticmethod
    def get_chunker(strategy="recursive"):

        if strategy == "recursive":
            return RecursiveChunker()

        elif strategy == "token":
            return TokenChunker()

        else:
            raise ValueError( f"Unknown strategy: {strategy}" )