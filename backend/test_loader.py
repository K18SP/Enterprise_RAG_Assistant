from pathlib import Path
from loaders.loader_factory import LoaderFactory
# import logging

file_path = 'D:/resume/Kushal_Resume.pdf'

extension = Path(file_path).suffix # Extracts the file extension including the leading dot (e.g., '.pdf')

loader = LoaderFactory.get_loader(extension) # Requests the matching instantiated loader object from the factory

documents = loader.load(file_path) # Polymorphically executes the specific loader's parsing logic

# Log the total document count once outside the rendering loop
# logger.info("Successfully loaded %d document pages from %s", len(documents), file_path)

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