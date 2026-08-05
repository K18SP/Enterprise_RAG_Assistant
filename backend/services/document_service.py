from pathlib import Path
import shutil
import tempfile

from fastapi import UploadFile

from utils.file_utils import FileUtils
from utils.logger import setup_logger

from schemas.delete_response import DeleteResponse

from config.constants import (
    UPLOAD_DIR,
    CHUNKING_STRATEGY
)

from loaders.loader_factory import LoaderFactory
from preprocessing.cleaner import TextCleaner
from chunking.chunk_factory import ChunkFactory

from exceptions.document_not_found_exception import DocumentNotFoundError

from exceptions.document_exception import DocumentError

from schemas.upload_response import UploadResponse
from schemas.document_record import DocumentRecord

from transaction.ingest_transaction import (
    IngestTransaction
)


logger = setup_logger(__name__)


class DocumentService:

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".txt",
        ".docx",
        ".csv",
        ".md"
    }


    def __init__(
        self,
        vector_db,
        document_registry,
        workspace
    ):

        self.vector_db = vector_db
        self.document_registry = document_registry

        self.workspace = workspace

        self.upload_dir = Path(UPLOAD_DIR)

        self.upload_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.chunker = ChunkFactory.get_chunker(
            CHUNKING_STRATEGY
        )

        logger.info(
            f"Document Service initialized at '{self.upload_dir}'."
        )


    # =========================================================
    # PROCESS / UPLOAD DOCUMENT
    # =========================================================

    def process_document(
        self,
        file: UploadFile
    ) -> UploadResponse:

        transaction = IngestTransaction()

        filename = Path(
            file.filename or ""
        ).name

        if not filename:

            raise DocumentError(
                "Uploaded file does not have a valid filename."
            )

        extension = Path(
            filename
        ).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:

            raise DocumentError(
                f"Unsupported file type: {extension or 'unknown'}"
            )

        temp_path = None

        try:

            # ---------------------------------------
            # STEP 1: Save temporary file
            # ---------------------------------------

            logger.info(
                f"Receiving uploaded document: {filename}"
            )

            with tempfile.NamedTemporaryFile(
                mode="wb",
                delete=False,
                suffix=extension,
                dir=self.upload_dir
            ) as temp_file:

                shutil.copyfileobj(
                    file.file,
                    temp_file
                )

                temp_path = Path(
                    temp_file.name
                )


            # ---------------------------------------
            # STEP 2: Validate file
            # ---------------------------------------

            size_bytes = temp_path.stat().st_size

            if size_bytes == 0:

                raise DocumentError(
                    "Uploaded file is empty."
                )


            # ---------------------------------------
            # STEP 3: Generate document ID
            # ---------------------------------------

            document_hash = FileUtils.calculate_sha256(
                temp_path
            )

            logger.info(
                f"Document ID generated for "
                f"'{filename}': {document_hash}"
            )


            # ---------------------------------------
            # STEP 4: Duplicate detection
            # ---------------------------------------

            if self.document_registry.exists(
                document_hash
            ):

                existing_document = (
                    self.document_registry.get(
                        document_hash
                    )
                )

                logger.warning(
                    f"Duplicate document detected: "
                    f"'{filename}' | "
                    f"document_id: {document_hash}"
                )

                raise DocumentError(
                    f"Document already indexed: "
                    f"{existing_document.filename}"
                )


            # ---------------------------------------
            # STEP 5: Store permanently
            # ---------------------------------------

            stored_filename = (
                f"{document_hash}{extension}"
            )

            file_path = (
                self.upload_dir /
                stored_filename
            )

            temp_path.replace(
                file_path
            )

            temp_path = None

            transaction.register_saved_file(file_path)

            logger.info(
                f"Document '{filename}' stored as "
                f"'{stored_filename}'."
            )


            # ---------------------------------------
            # STEP 6: Load
            # ---------------------------------------

            logger.info(
                f"Loading document: {filename}"
            )

            loader = LoaderFactory.get_loader(
                extension
            )

            documents = loader.load(
                str(file_path)
            )

            if not documents:

                raise DocumentError(
                    "No content could be extracted from the document."
                )


            # ---------------------------------------
            # STEP 7: Add metadata
            # ---------------------------------------

            for document in documents:

                document.metadata["document_id"] = document_hash
                document.metadata["filename"] = filename
                document.metadata["stored_filename"] = stored_filename
                document.metadata["extension"] = extension


            logger.info(
                f"Loaded {len(documents)} document(s) "
                f"from '{filename}'."
            )


            # ---------------------------------------
            # STEP 8: Clean
            # ---------------------------------------

            logger.info(
                f"Cleaning document: {filename}"
            )

            cleaned_documents = TextCleaner.clean_documents(
                documents
            )

            if not cleaned_documents:

                raise DocumentError(
                    "Document contains no usable text after cleaning."
                )

            logger.info(
                f"Cleaned {len(cleaned_documents)} "
                f"document(s)."
            )


            # ---------------------------------------
            # STEP 9: Chunk
            # ---------------------------------------

            logger.info(
                f"Chunking document: {filename}"
            )

            chunks = self.chunker.split(
                cleaned_documents
            )

            if not chunks:

                raise DocumentError(
                    "No chunks were created from the document."
                )

            logger.info(
                f"Created {len(chunks)} chunk(s) "
                f"from '{filename}'."
            )


            # ---------------------------------------
            # STEP 10: Add chunks to FAISS
            # ---------------------------------------

            logger.info(
                f"Adding {len(chunks)} chunk(s) "
                f"to vector database."
            )

            self.vector_db.add_documents(
                chunks
            )

            logger.info(
                "Chunks added to vector database."
            )


            # ---------------------------------------
            # STEP 11: Persist FAISS
            # ---------------------------------------

            logger.info(
                "Saving updated vector database."
            )

            self.vector_db.save()

            transaction.mark_faiss_updated()

            logger.info(
                "Updated vector database saved successfully."
            )


            # ---------------------------------------
            # STEP 12: Register document
            # ---------------------------------------

            record = DocumentRecord(
                document_id=document_hash,
                filename=filename,
                stored_filename=stored_filename,
                extension=extension,
                size_bytes=size_bytes,
                documents_loaded=len(documents),
                chunks_created=len(chunks)
            )

            self.document_registry.add(
                record
            )

            transaction.mark_registry_updated()

            logger.info(
                f"Document '{filename}' registered successfully."
            )


            # ---------------------------------------
            # STEP 13: Return response
            # ---------------------------------------

            return UploadResponse(
                document_id=document_hash,
                filename=filename,
                extension=extension,
                size_bytes=size_bytes,
                documents_loaded=len(documents),
                chunks_created=len(chunks),
                status="Processed successfully"
            )


        except DocumentError:

            raise


        except Exception as e:

            logger.exception(
                f"Failed to process document '{filename}'."
            )

            transaction.rollback(
                self.vector_db,
                self.document_registry
            )

            raise DocumentError(
                "Failed to process uploaded document."
            ) from e


        finally:

            # Remove temporary file if processing
            # failed before permanent storage.

            if (
                temp_path is not None
                and temp_path.exists()
            ):

                temp_path.unlink(
                    missing_ok=True
                )

                logger.info(
                    f"Temporary upload removed for "
                    f"'{filename}'."
                )


    # =========================================================
    # GET ALL DOCUMENTS
    # =========================================================

    def get_documents(
        self,
        document_id: str
    ) -> DocumentRecord:

        logger.info(
            f"Retrieving document: {document_id}"
        )

        try:

            document = self.document_registry.get(
                document_id
            )

            if document is None:

                raise DocumentNotFoundError(
                    document_id
                )

            logger.info(
                f"Document found: {document.filename}"
            )

            return document


        except DocumentError:
            raise


        except Exception as e:

            logger.exception(
                f"Failed to retrieve document: "
                f"{document_id}"
            )

            raise DocumentError(
                "Failed to retrieve document."
            ) from e


    # =========================================================
    # GET DOCUMENT BY ID
    # =========================================================

    def get_document(
        self,
        document_id: str
    ) -> DocumentRecord:

        logger.info(
            f"Retrieving document: {document_id}"
        )

        try:

            document = (
                self.document_registry.get(
                    document_id
                )
            )

            if document is None:

                raise DocumentError(
                    f"Document not found: {document_id}"
                )

            logger.info(
                f"Document found: "
                f"{document.filename}"
            )

            return document


        except DocumentError:

            raise


        except Exception as e:

            logger.exception(
                f"Failed to retrieve document: "
                f"{document_id}"
            )

            raise DocumentError(
                "Failed to retrieve document."
            ) from e

    # =========================================================
    # GET DOCUMENT BY ID
    # =========================================================

    def delete_document(
        self,
        document_id: str
    ) -> DeleteResponse:

        logger.info(
            f"Deleting document: {document_id}"
        )

        try:

            # ---------------------------------------
            # STEP 1: Get registry record
            # ---------------------------------------

            document = self.document_registry.get(
                document_id
            )

            if document is None:

                raise DocumentNotFoundError(
                    document_id
                )


            # ---------------------------------------
            # STEP 2: Delete chunks from FAISS
            # ---------------------------------------

            deleted_chunks = (
                self.vector_db.delete_document(
                    document_id
                )
            )

            logger.info(
                f"Deleted {deleted_chunks} "
                f"chunk(s) from vector database."
            )


            # ---------------------------------------
            # STEP 3: Persist updated FAISS
            # ---------------------------------------

            self.vector_db.save()

            logger.info(
                "Updated vector database saved."
            )


            # ---------------------------------------
            # STEP 4: Delete physical file
            # ---------------------------------------

            file_path = (
                self.upload_dir /
                document.stored_filename
            )

            if file_path.exists():

                file_path.unlink()

                logger.info(
                    f"Deleted stored file: "
                    f"{document.stored_filename}"
                )

            else:

                logger.warning(
                    f"Stored file not found: "
                    f"{document.stored_filename}"
                )


            # ---------------------------------------
            # STEP 5: Remove registry record
            # ---------------------------------------

            self.document_registry.delete(
                document_id
            )

            logger.info(
                f"Document '{document.filename}' "
                f"deleted successfully."
            )


            # ---------------------------------------
            # Response
            # ---------------------------------------

            return DeleteResponse(
                document_id=document_id,
                filename=document.filename,
                chunks_deleted=deleted_chunks,
                status="Deleted successfully"
            )


        except DocumentError:
            raise


        except Exception as e:

            logger.exception(
                f"Failed to delete document: "
                f"{document_id}"
            )

            raise DocumentError(
                "Failed to delete document."
            ) from e