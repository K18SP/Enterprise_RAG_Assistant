from pathlib import Path

from config.constants import DATA_DIR

from utils.logger import setup_logger


logger = setup_logger(__name__)


class UserWorkspace:

    """
    Creates and manages the workspace of a single user.

    Example:

    data/
        users/
            kushal/
                uploads/
                vector_db/
                registry.json
    """

    def __init__(
        self,
        user_id: str
    ):

        self.user_id = user_id

        self.root = (
            Path(DATA_DIR)
            / "users"
            / user_id
        )

        self.upload_path = (
            self.root
            / "uploads"
        )

        self.vector_db_path = (
            self.root
            / "vector_db"
        )

        self.registry_path = (
            self.root
            / "document_registry.json"
        )

        self._initialize()

    def _initialize(self) -> None:

        self.upload_path.mkdir(
            parents=True,
            exist_ok=True
        )

        self.vector_db_path.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.registry_path.exists():

            self.registry_path.write_text(
                "{}",
                encoding="utf-8"
            )

        logger.info(
            f"Workspace initialized for user '{self.user_id}'."
        )

    def __repr__(self) -> str:

        return (
            f"UserWorkspace("
            f"user_id='{self.user_id}')"
        )