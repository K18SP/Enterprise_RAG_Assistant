from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from .base_vectorstore import BaseVectorStore

from exceptions.vectorstore_exception import VectorStoreError
from utils.logger import setup_logger


logger = setup_logger(__name__)


class FAISSStore(BaseVectorStore):

    def __init__(self, embedding, save_path):

        self.embedding = embedding
        self.db = None
        self.save_path = Path(save_path)

        logger.info(
            f"Initializing FAISS vector store at '{self.save_path}'."
        )

    def exists(self) -> bool:

        index_file = self.save_path / "index.faiss"
        metadata_file = self.save_path / "index.pkl"

        return (
            index_file.exists()
            and metadata_file.exists()
        )

    def add_documents(
        self,
        documents: List[Document]
    ):

        if not documents:
            return

        try:

            if self.db is None:

                logger.info(
                    f"Creating FAISS index with "
                    f"{len(documents)} chunk(s)."
                )

                self.db = FAISS.from_documents(
                    documents,
                    self.embedding.embedding
                )

            else:

                logger.info(
                    f"Adding {len(documents)} chunk(s) "
                    f"to existing FAISS index."
                )

                self.db.add_documents(
                    documents
                )

            logger.info(
                "Documents added to FAISS successfully."
            )

        except Exception as e:

            logger.exception(
                "Failed to add documents to FAISS."
            )

            raise VectorStoreError(
                "Failed to add documents to vector database."
            ) from e


    def similarity_search(
        self,
        query: str,
        k: int = 5
    ):

        if self.db is None:

            raise VectorStoreError(
                "Vector database is not loaded."
            )

        try:

            return self.db.similarity_search(
                query,
                k=k
            )

        except Exception as e:

            logger.exception(
                "FAISS similarity search failed."
            )

            raise VectorStoreError(
                "Vector database search failed."
            ) from e


    def mmr_search(
        self,
        query: str,
        k: int = 5,
        fetch_k: int = 20
    ):

        if self.db is None:

            raise VectorStoreError(
                "Vector database is not loaded."
            )

        try:

            return self.db.max_marginal_relevance_search(
                query,
                k=k,
                fetch_k=fetch_k
            )

        except Exception as e:

            logger.exception(
                "FAISS MMR search failed."
            )

            raise VectorStoreError(
                "Vector database search failed."
            ) from e

    def delete_document(
        self,
        document_id: str
    ) -> int:

        if self.db is None:

            raise VectorStoreError(
                "Vector database is not loaded."
            )

        try:

            logger.info(
                f"Removing FAISS chunks for "
                f"document_id: {document_id}"
            )

            ids_to_delete = []

            # FAISS docstore contains:
            #
            # docstore_id -> Document

            for docstore_id, document in (
                self.db.docstore._dict.items()
            ):

                if (
                    document.metadata.get("document_id")
                    == document_id
                ):

                    ids_to_delete.append(
                        docstore_id
                    )


            if not ids_to_delete:

                logger.warning(
                    f"No FAISS chunks found for "
                    f"document_id: {document_id}"
                )

                return 0


            self.db.delete(
                ids=ids_to_delete
            )


            logger.info(
                f"Removed {len(ids_to_delete)} "
                f"chunk(s) from FAISS."
            )

            return len(ids_to_delete)


        except Exception as e:

            logger.exception(
                f"Failed to delete document "
                f"'{document_id}' from FAISS."
            )

            raise VectorStoreError(
                "Failed to delete document from vector database."
            ) from e


    def save(self):

        if self.db is None:

            raise VectorStoreError(
                "No vector database to save."
            )

        try:

            self.save_path.mkdir(
                parents=True,
                exist_ok=True
            )

            self.db.save_local(
                str(self.save_path)
            )

            logger.info(
                "FAISS index saved successfully."
            )

        except Exception as e:

            logger.exception(
                "Failed to save FAISS index."
            )

            raise VectorStoreError(
                "Failed to save vector database."
            ) from e


    def load(self):

        try:

            logger.info(
                f"Loading FAISS index from "
                f"'{self.save_path}'."
            )

            self.db = FAISS.load_local(
                str(self.save_path),
                self.embedding.embedding,
                allow_dangerous_deserialization=True
            )

            logger.info(
                "FAISS index loaded successfully."
            )

        except Exception as e:

            logger.exception(
                "Failed to load FAISS index."
            )

            raise VectorStoreError(
                "Failed to load vector database."
            ) from e