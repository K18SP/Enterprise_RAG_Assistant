from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from evaluation.evaluators.base_evaluator import BaseEvaluator
from evaluation.metrics.metric_result import MetricResult
from evaluation.metrics.evaluation_report import EvaluationReport
from evaluation.benchmark.benchmark_case import BenchmarkCase


class GenerationEvaluator(BaseEvaluator):

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def evaluate(
        self,
        benchmark: BenchmarkCase,
        generated_answer: str,
        **kwargs
    ) -> EvaluationReport:

        expected = benchmark.expected_answer.strip()
        generated = generated_answer.strip()

        # ---------------------------------------
        # Exact Match
        # ---------------------------------------

        exact_match = (
            expected.lower() == generated.lower()
        )

        # ---------------------------------------
        # Semantic Similarity
        # ---------------------------------------

        expected_embedding = self.model.encode(
            expected,
            convert_to_tensor=True
        )

        generated_embedding = self.model.encode(
            generated,
            convert_to_tensor=True
        )

        similarity = float(

            cos_sim(
                expected_embedding,
                generated_embedding
            )[0][0]

        )

        # ---------------------------------------
        # Keyword Coverage
        # ---------------------------------------

        keywords = benchmark.expected_keywords

        if keywords:

            matched = sum(

                keyword.lower() in generated.lower()

                for keyword in keywords

            )

            keyword_coverage = matched / len(keywords)

        else:

            keyword_coverage = 1.0

        # ---------------------------------------
        # Answer Length Ratio
        # ---------------------------------------

        expected_words = max(
            len(expected.split()),
            1
        )

        generated_words = len(
            generated.split()
        )

        length_ratio = (
            generated_words /
            expected_words
        )

        # ---------------------------------------
        # Metrics
        # ---------------------------------------

        metrics = [

            MetricResult(

                name="Exact Match",

                score=float(exact_match),

                passed=exact_match,

                description="Exact answer comparison."

            ),

            MetricResult(

                name="Semantic Similarity",

                score=round(similarity, 4),

                passed=similarity >= 0.80,

                description="Cosine similarity between expected and generated answer."

            ),

            MetricResult(

                name="Keyword Coverage",

                score=round(keyword_coverage, 4),

                passed=keyword_coverage >= 0.80,

                description="Coverage of expected keywords."

            ),

            MetricResult(

                name="Answer Length Ratio",

                score=round(length_ratio, 4),

                passed=0.5 <= length_ratio <= 2.0,

                description="Generated answer length compared to expected."

            )

        ]

        return EvaluationReport(

            evaluator="Generation Evaluator",

            metrics=metrics,

            metadata={

                "query": benchmark.query,

                "expected_answer": expected,

                "generated_answer": generated,

                "expected_keywords": keywords

            }

        )