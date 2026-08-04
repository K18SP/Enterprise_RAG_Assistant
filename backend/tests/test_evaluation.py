from evaluation.evaluation_service import EvaluationService

service = EvaluationService()

reports = service.evaluate(

    latency={

        "embedding": 23,

        "retriever": 17,

        "reranker": 38,

        "llm": 612

    }

)

for report in reports:

    print(report.model_dump_json(indent=4))