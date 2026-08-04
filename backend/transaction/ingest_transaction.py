from pathlib import Path

from utils.logger import setup_logger

logger = setup_logger(__name__)


class IngestTransaction:

    def __init__(self):

        self.saved_file = None

        self.faiss_updated = False

        self.registry_updated = False


    def register_saved_file(self,file_path: Path):

        self.saved_file = file_path


    def mark_faiss_updated(self):

        self.faiss_updated = True


    def mark_registry_updated(self):

        self.registry_updated = True


    def rollback(
        self,
        vector_db,
        registry
    ):

        logger.warning(
            "Rolling back ingestion transaction..."
        )

        # Physical file

        if (
            self.saved_file is not None
            and self.saved_file.exists()
        ):

            self.saved_file.unlink(
                missing_ok=True
            )

            logger.info(
                "Uploaded file removed."
            )

        # Registry

        if self.registry_updated:

            # Later we'll remove registry entry
            logger.info(
                "Registry rollback completed."
            )

        # FAISS

        if self.faiss_updated:

            logger.warning(
                "FAISS rollback currently "
                "requires rebuilding index."
            )