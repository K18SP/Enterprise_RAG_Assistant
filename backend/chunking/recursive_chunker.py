from typing import List
from langchain_core.documents import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter
from .base_chunker import BaseChunker

# Recursive Chunker
"""

-> Tries larger structural boundaries first, falling back to smaller
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