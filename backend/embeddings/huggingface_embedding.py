from typing import List

from langchain_huggingface import HuggingFaceEmbeddings

from .base_embedding import BaseEmbedding


class HuggingFaceEmbedding(BaseEmbedding):

    def __init__(
        self,
        model_name="BAAI/bge-small-en-v1.5"
    ):

        self.embedding = HuggingFaceEmbeddings(

            model_name=model_name,

            model_kwargs={
                "device": "cpu"
            },

            encode_kwargs={
                "normalize_embeddings": True
            }
        )

    def embed_documents(
        self,
        texts: List[str]
    ):

        return self.embedding.embed_documents(texts)

    def embed_query(
        self,
        text: str
    ):

        return self.embedding.embed_query(text)