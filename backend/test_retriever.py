from embeddings.embedding_factory import EmbeddingFactory
from vectordb.vectorstore_factory import VectorStoreFactory
from retrieval.retriever_factory import RetrieverFactory

embedding = EmbeddingFactory.get_embedding()

vector_db = VectorStoreFactory.get_vectorstore(
    embedding
)

vector_db.load()

retriever = RetrieverFactory.get_retriever(
    vector_db,
    "similarity"
)

results = retriever.retrieve(
    "Tell me about Machine Learning",
    k=3
)

print("=" * 80)

print("Similarity Search")

print("=" * 80)

for i, doc in enumerate(results, 1):

    print(f"\nResult {i}")

    print(doc.metadata)

    print(doc.page_content[:300])