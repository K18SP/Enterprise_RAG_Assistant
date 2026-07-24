from pipeline.pipeline_factory import PipelineFactory

pipeline = PipelineFactory.create_pipeline()

query = input("Ask a question: ")

response = pipeline.ask(query)

print("=" * 80)
print("Answer")
print("=" * 80)

print(response.answer)