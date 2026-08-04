from evaluation.evaluation_service import EvaluationService
from evaluation.benchmark.benchmark_case import BenchmarkCase

benchmark = BenchmarkCase(

    query="Tell me about Machine Learning",

    expected_document_ids=[],

    expected_answer="Machine Learning is a subset of Artificial Intelligence.",

    expected_keywords=[
        "Machine Learning",
        "Artificial Intelligence"
    ]

)

service = EvaluationService()

reports = service.evaluate(

    benchmark=benchmark,

    generated_answer="Machine Learning is a subset of Artificial Intelligence."

)

for report in reports:

    print(report.model_dump_json(indent=4))