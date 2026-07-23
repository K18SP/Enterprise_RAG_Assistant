from embeddings.embedding_factory import EmbeddingFactory
from vectordb.vectorstore_factory import VectorStoreFactory
from retrieval.retriever_factory import RetrieverFactory
from reranker.reranker_factory import RerankerFactory


# Create embedding model
embedding = EmbeddingFactory.get_embedding()

# Create vector store
vector_db = VectorStoreFactory.get_vectorstore(
    embedding
)

# Load vector database
vector_db.load()

# Create retriever
retriever = RetrieverFactory.get_retriever(
    vector_db,
    "similarity"
)

# Retrieve documents
documents = retriever.retrieve(
    query="Tell me about Machine Learning",
    k=10
)

print("=" * 80)
print("Before Reranking")
print("=" * 80)

for i, doc in enumerate(documents, start=1):

    print(f"\nResult {i}")
    print(doc.metadata)
    print(doc.page_content)

# Create reranker
reranker = RerankerFactory.get_reranker()

# Rerank documents
reranked_docs = reranker.rerank(
    query="Tell me about Machine Learning",
    documents=documents,
    top_k=5
)

print("\n" + "=" * 80)
print("After Reranking")
print("=" * 80)

for i, doc in enumerate(reranked_docs, start=1):

    print(f"\nResult {i}")
    print("Reranker Score :", doc.metadata["reranker"]["score"])
    print(doc.metadata)
    print(doc.page_content)