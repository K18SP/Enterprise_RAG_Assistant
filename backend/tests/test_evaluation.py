from evaluation.evaluation_service import EvaluationService


service = EvaluationService()

report = service.evaluate()

print(report.model_dump_json(indent=4))