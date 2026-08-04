from evaluation.metrics.evaluation_report import EvaluationReport


class EvaluationPipeline:

    def __init__(self, evaluators):

        self.evaluators = evaluators


    def evaluate(self, **kwargs):

        reports = []

        for evaluator in self.evaluators:

            report = evaluator.evaluate(
                **kwargs
            )

            reports.append(report)

        return reports