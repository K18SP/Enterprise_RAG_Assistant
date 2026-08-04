import json
from pathlib import Path

from schemas.document_record import DocumentRecord
from utils.logger import setup_logger


logger = setup_logger(__name__)


class DocumentRegistry:

    def __init__(self, registry_path):

        self.registry_path = Path(
            registry_path
        )

        self.registry_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # Create valid empty registry if file
        # does not exist.
        if not self.registry_path.exists():

            self._write({})

            logger.info(
                f"Created document registry at "
                f"'{self.registry_path}'."
            )

        logger.info(
            f"Document Registry initialized at "
            f"'{self.registry_path}'."
        )


    def _read(self) -> dict:

        try:

            # ---------------------------------------
            # Missing file
            # ---------------------------------------

            if not self.registry_path.exists():
                return {}


            # ---------------------------------------
            # Empty file
            # ---------------------------------------

            if self.registry_path.stat().st_size == 0:

                logger.warning(
                    "Document registry is empty. "
                    "Using empty registry."
                )

                return {}


            # ---------------------------------------
            # Read JSON
            # ---------------------------------------

            with self.registry_path.open(
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)


            # Registry should always be an object
            if not isinstance(data, dict):

                raise ValueError(
                    "Document registry must contain "
                    "a JSON object."
                )


            return data


        except json.JSONDecodeError as e:

            logger.exception(
                "Document registry contains invalid JSON."
            )

            raise ValueError(
                "Document registry is corrupted."
            ) from e


        except OSError as e:

            logger.exception(
                "Failed to read document registry."
            )

            raise ValueError(
                "Failed to read document registry."
            ) from e


    def _write(
        self,
        registry: dict
    ) -> None:

        try:

            with self.registry_path.open(
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    registry,
                    file,
                    indent=4
                )


        except OSError as e:

            logger.exception(
                "Failed to write document registry."
            )

            raise ValueError(
                "Failed to write document registry."
            ) from e


    def exists(
        self,
        document_id: str
    ) -> bool:

        registry = self._read()

        return document_id in registry


    def get(
        self,
        document_id: str
    ) -> DocumentRecord | None:

        registry = self._read()

        data = registry.get(
            document_id
        )

        if data is None:
            return None

        return DocumentRecord(
            **data
        )


    def add(
        self,
        record: DocumentRecord
    ) -> None:

        registry = self._read()

        registry[record.document_id] = (
            record.model_dump()
        )

        self._write(
            registry
        )

        logger.info(
            f"Document registered: "
            f"{record.document_id}"
        )


    def get_all(
        self
    ) -> list[DocumentRecord]:

        registry = self._read()

        return [
            DocumentRecord(**record)
            for record in registry.values()
        ]


    def delete(
        self,
        document_id: str
    ) -> bool:

        registry = self._read()

        if document_id not in registry:
            return False

        del registry[document_id]

        self._write(
            registry
        )

        logger.info(
            f"Document removed from registry: "
            f"{document_id}"
        )

        return True