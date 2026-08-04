from exceptions.document_exception import DocumentError


class DocumentNotFoundError(DocumentError):

    def __init__(self, document_id: str):

        self.document_id = document_id

        super().__init__(
            f"Document not found: {document_id}"
        )