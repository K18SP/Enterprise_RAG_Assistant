from backend.pipeline.pipeline_factory import PipelineFactory
from backend.evaluation.evaluation_service import EvaluationService
from backend.evaluation.benchmark.benchmark_case import BenchmarkCase

pipeline = PipelineFactory.create_pipeline()

response = pipeline.ask(

    "Tell me about Machine Learning"

)

evaluation_service.evaluate(

    benchmark=benchmark,

    generated_answer=response.answer,

    retrieved_documents=response.documents

)