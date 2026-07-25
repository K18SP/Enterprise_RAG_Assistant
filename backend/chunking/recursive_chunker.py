from typing import List
from langchain_core.documents import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter
from .base_chunker import BaseChunker

# Recursive Chunker
"""
-> It uses a prioritized list of separators to divide the text. f a chunk is still too big, it moves to the next smaller separator.
-> It keeps paragraphs and sentences whole, protecting the natural meaning of the text.
-> It's primary use is RAG applications

"""

class RecursiveChunker(BaseChunker):

    def __init__(self, chunk_size = 500, chunk_overlap = 50):
        """
        Initializes the chunker with safe, logical token window constraints.
        """

        # Ensure chunk size is always strictly greater than overlap window
        if chunk_overlap >= chunk_size:
            raise ValueError("Chunk overlap must be strictly less than chunk size")

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,

            # Fallback hierarchy ordered from largest block to single character
            separators=[ "\n,\n", "\n", ". "," ", ""]

        )

    def split(self, documents: List[Document]) -> List[Document]:

        return self.splitter.split_documents(documents)