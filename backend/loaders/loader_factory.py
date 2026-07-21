from .pdf_loader import PDFLoader
from .txt_loader import TXTLoader
from .docx_loader import DOCXLoader
from .csv_loader import CSVDocumentLoader
from .md_loader import MarkdownLoader

# To handle paths of all the files
class LoaderFactory:

    # Added paths of all files
    @staticmethod
    def get_loader(extension: str):

        extension = extension.lower()

        if extension == ".pdf":
            return PDFLoader()

        if extension == ".txt":
            return TXTLoader()

        if extension == ".docx":
            return DOCXLoader()

        if extension == ".csv":
            return CSVDocumentLoader()

        if extension == ".md":
            return MarkdownLoader()

        raise ValueError(f"Unsupported file type: {extension}")