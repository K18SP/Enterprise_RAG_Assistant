from typing import List

from langchain_core.documents import Document

from langchain_text_splitters import TokenTextSplitter

from .base_chunker import BaseChunker

## Token Chunker:
"""

-> It cuts precisely when it hits a fixed token count
-> It is primarily use when we need to enforce hard input constraints for LLM

"""

class TokenChunker(BaseChunker):

    def __init__(self, chunk_size = 300, chunk_overlap = 50):

        self.splitter = TokenTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap)

    def split(self, documents: List[Document]) -> List[Document]:

        return self.splitter.split_documents(documents)