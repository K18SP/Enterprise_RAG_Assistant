from langchain_core.documents import Document

from schemas.retrieved_document import RetrievedDocument


class DocumentMapper:

    @staticmethod
    def to_response(
        document: Document
    ) -> RetrievedDocument:

        return RetrievedDocument(

            content=document.page_content,

            metadata=document.metadata
        )

    @staticmethod
    def to_response_list(
        documents: list[Document]
    ) -> list[RetrievedDocument]:

        return [

            DocumentMapper.to_response(doc)

            for doc in documents

        ]