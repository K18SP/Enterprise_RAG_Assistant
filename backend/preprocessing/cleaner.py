import re
import ftfy
from langchain_core.documents import Document

class TextCleaner:

    @staticmethod
    def clean_text(text: str) -> str:

        # Clean raw extracted text before chunking

        #Fix broken Unicode
        text = ftfy.fix_text(text)

        #Remove extra spaces
        text = re.sub(r"[ \t]+", " ",text)

        #Remove excessive newlines
        text = re.sub(r'\n{3,}','\n\n', text)

        # Remove page numbers like:
        # Page 1
        # PAGE 5
        text = re.sub(
            r"(?i)^page\s+\d+$",
            "",
            text,
            flags=re.MULTILINE
        )

        return text.strip()
    
    @staticmethod
    def clean_documents(documents):

        cleaned_docs = []

        for doc in documents:

            cleaned_text = TextCleaner.clean_text(doc.page_content)

            cleaned_docs.append(
                Document(
                    page_content = cleaned_text,
                    metadata = doc.metadata
                )
            )

        return cleaned_docs