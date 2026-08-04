from evaluation.evaluators.base_evaluator import BaseEvaluator

from evaluation.metrics.metric_result import MetricResult
from evaluation.metrics.evaluation_report import EvaluationReport

from schemas.latency_metadata import LatencyMetadata

class LatencyEvaluator(BaseEvaluator):

    def evaluate(
        self,
        latency: LatencyMetadata,
        **kwargs
    ) -> EvaluationReport:

        metrics = []

        total = 0.0

        latency_values = latency.model_dump()

        total = latency.total_ms

        for component, value in latency_values.items():

            metrics.append(

                MetricResult(

                    name=component,

                    score=round(value, 2),

                    passed=value < 1000,

                    description=f"{component} latency."

                )

            )

        for component, value in latency.items():

            total += value

            metrics.append(

                MetricResult(
                    name=component,
                    score=round(value, 2),
                    passed=value < 1000,
                    description=f"{component} latency in milliseconds."
                )

            )

        metrics.append(

            MetricResult(
                name="Total",
                score=round(total, 2),
                passed=total < 3000,
                description="Total pipeline latency."
            )

        )

        return EvaluationReport(

            evaluator="Latency Evaluator",

            metrics=metrics,

            metadata=latency

        )