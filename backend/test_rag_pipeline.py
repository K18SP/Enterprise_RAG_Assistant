from pipeline.pipeline_factory import PipelineFactory

pipeline = PipelineFactory.create_pipeline()

query = input("Ask a question: ")

response = pipeline.ask(query)

print("=" * 80)
print("Answer")
print("=" * 80)

print(response.answer)
print("\nQuery:")
print(response.query)

print("\nMetadata:")
print(response.metadata)

print("\nRetrieved Documents:")
for i, doc in enumerate(response.documents, start=1):
    print(f"\nDocument {i}")
    print(f"Source: {doc.metadata.get('source', 'Unknown')}")
    print(f"Page: {doc.metadata.get('page', '-')}")
    print(doc.content[:200], "...")