from evaluation.evaluators.retrieval_evaluator import RetrievalEvaluator
from evaluation.evaluators.latency_evaluator import LatencyEvaluator
from evaluation.evaluators.generation_evaluator import GenerationEvaluator

from evaluation.pipeline.evaluation_pipeline import EvaluationPipeline

from evaluation.evaluators.ragas_evaluator import RAGASEvaluator


class EvaluatorFactory:

    @staticmethod
    def create_pipeline():

        return EvaluationPipeline(

            [

                RetrievalEvaluator(),

                LatencyEvaluator(),

                GenerationEvaluator(),

                RAGASEvaluator(),

            ]

        )