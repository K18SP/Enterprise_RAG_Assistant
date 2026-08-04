from evaluation.evaluators.latency_evaluator import LatencyEvaluator
from evaluation.evaluators.retrieval_evaluator import RetrievalEvaluator

from evaluation.pipeline.evaluation_pipeline import EvaluationPipeline

class EvaluatorFactory:

    @staticmethod
    def create_pipeline():

        evaluators = [

            RetrievalEvaluator(),

            LatencyEvaluator()

        ]

        return EvaluationPipeline(
            evaluators
        )