from .pdf_loader import PDFLoader
from .txt_loader import TXTLoader
from .docx_loader import DOCXLoader
from .csv_loader import CSVDocumentLoader
from .md_loader import MarkdownLoader

# To handle paths of all the files
class LoaderFactory:

    # Added paths of all files
    loaders = {

        ".pdf": PDFLoader(),

        ".txt": TXTLoader(),

        ".docx": DOCXLoader(),

        ".csv": CSVDocumentLoader(),

        ".md": MarkdownLoader()

    }

    @classmethod # Here we use class method it allows us to call LoaderFactory.get_loader(".pdf") directly without needing to create an object like factory = LoaderFactory().
    def get_loader(cls,extension):

        loader = cls.loaders.get(extension.lower()) # It looks up the lowercase file extension in your dictionary.

        if loader is None:

            raise ValueError(f"Unsupported file type: {extension}")
        
        return loader