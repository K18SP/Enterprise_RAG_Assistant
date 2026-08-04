from evaluation.evaluators.base_evaluator import BaseEvaluator

from evaluation.metrics.metric_result import MetricResult
from evaluation.metrics.evaluation_report import EvaluationReport


class DummyEvaluator(BaseEvaluator):

    def evaluate(
        self,
        **kwargs
    ) -> EvaluationReport:

        metric = MetricResult(
            name="Dummy Metric",
            score=1.0,
            passed=True,
            description="Evaluation framework initialized successfully."
        )

        return EvaluationReport(
            evaluator="dummy",
            metrics=[metric],
            metadata={
                "status": "ready"
            }
        )