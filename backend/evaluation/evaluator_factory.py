from evaluation.pipeline.evaluation_pipeline import EvaluationPipeline

from evaluation.evaluators.retrieval_evaluator import RetrievalEvaluator
from evaluation.evaluators.latency_evaluator import LatencyEvaluator


class EvaluatorFactory:

    @staticmethod
    def create_pipeline():

        return EvaluationPipeline(

            [

                RetrievalEvaluator(),

                LatencyEvaluator()

            ]

        )