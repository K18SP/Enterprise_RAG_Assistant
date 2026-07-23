from pathlib import Path

from loaders.loader_factory import LoaderFactory
from preprocessing.cleaner import TextCleaner
from chunking.chunk_factory import ChunkFactory
from embeddings.embedding_factory import EmbeddingFactory

# file_path = "data/resume.pdf"
file_path = "data/sample.txt"

loader = LoaderFactory.get_loader(Path(file_path).suffix)

documents = loader.load(file_path)

documents = TextCleaner.clean_documents(documents)

chunker = ChunkFactory.get_chunker()

chunks = chunker.split(documents)

texts = [doc.page_content for doc in chunks]

embedding_model = EmbeddingFactory.get_embedding()

vectors = embedding_model.embed_documents(texts)

print("Total Chunks :", len(chunks))

print("Embedding Dimension :", len(vectors[0]))

print("First 10 Values :")

print(vectors[0][:10])