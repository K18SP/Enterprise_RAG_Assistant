from pathlib import Path

from loaders.loader_factory import LoaderFactory

from preprocessing.cleaner import TextCleaner

from chunking.chunk_factory import ChunkFactory

from vectordb.vectorstore_factory import (
    VectorStoreFactory
)

file_path = "data/resume.pdf"

loader = LoaderFactory.get_loader(
    Path(file_path).suffix
)

documents = loader.load(file_path)

documents = TextCleaner.clean_documents(
    documents
)

chunker = ChunkFactory.get_chunker()

chunks = chunker.split(documents)

vector_db = VectorStoreFactory.get_vectorstore()

vector_db.add_documents(chunks)

vector_db.save()

vector_db.load()

results = vector_db.similarity_search(

    "Tell me about Kushal internships",

    k=3

)

for r in results:

    print(r.page_content)

    print(r.metadata)

print("Database Created Successfully")