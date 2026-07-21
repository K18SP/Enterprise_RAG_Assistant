from pathlib import Path
from loaders.loader_factory import LoaderFactory
from preprocessing.cleaner import TextCleaner
from utils.logger import logger
# import logging

file_path = 'data/resume.pdf'

extension = Path(file_path).suffix # Extracts the file extension including the leading dot (e.g., '.pdf')

try:

    loader = LoaderFactory.get_loader(extension) # Requests the matching instantiated loader object from the factory

except Exception as e:

    logger.error(e)

    raise

documents = loader.load(file_path) # Polymorphically executes the specific loader's parsing logic

documents = TextCleaner.clean_documents(documents)

# Log the total document count once outside the rendering loop
logger.info(f"Loaded {len(documents)} pages.")

print("=" * 80)
print(f"Total Pages Loaded : {len(documents)}")
print("=" * 80)

for i, doc in enumerate(documents):

    print(f"\nPAGE {i+1}")
    print("-" * 80)

    print("Metadata:")
    print(doc.metadata)

    print("\nContent Preview:")
    print(doc.page_content[:500])