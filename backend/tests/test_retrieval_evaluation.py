from evaluation.evaluation_service import EvaluationService

from evaluation.benchmark.benchmark_case import BenchmarkCase

from pipeline.pipeline_factory import PipelineFactory


pipeline = PipelineFactory.create_pipeline()


query = "Tell me about Machine Learning"

documents = pipeline.retriever.retrieve(
    query,
    k=5
)

benchmark = BenchmarkCase(

    query=query,

    expected_sources=[
        "sample.txt"
    ]

)


service = EvaluationService(
    evaluator="retrieval"
)


report = service.evaluate(

    benchmark=benchmark,

    retrieved_documents=documents

)


print(
    report.model_dump_json(
        indent=4
    )
)