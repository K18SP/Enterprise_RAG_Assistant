from pathlib import Path

from loaders.loader_factory import LoaderFactory
from preprocessing.cleaner import TextCleaner
from chunking.chunk_factory import ChunkFactory

file_path = "data/resume.pdf"

loader = LoaderFactory.get_loader(Path(file_path).suffix)

documents = loader.load(file_path)

documents = TextCleaner.clean_documents(documents)

chunker = ChunkFactory.get_chunker("recursive")

chunks = chunker.split(documents)

print(f"Original Pages : {len(documents)}")
print(f"Chunks Created : {len(chunks)}")

print("\nFirst Chunk:\n")
print(chunks[0].page_content)

print("\nMetadata:")
print(chunks[0].metadata)