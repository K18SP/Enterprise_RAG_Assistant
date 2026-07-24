from langchain_core.documents import Document

from schemas.retrieved_document import RetrievedDocument


class DocumentMapper:

    @staticmethod
    def to_schema(
        document: Document
    ) -> RetrievedDocument:

        return RetrievedDocument(
            content=document.page_content,
            metadata=document.metadata
        )

    @staticmethod
    def to_schema_list(
        documents: list[Document]
    ) -> list[RetrievedDocument]:

        return [
            DocumentMapper.to_schema(doc)
            for doc in documents
        ]