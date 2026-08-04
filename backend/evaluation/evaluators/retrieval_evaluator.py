from math import log2

from evaluation.evaluators.base_evaluator import BaseEvaluator

from evaluation.metrics.metric_result import MetricResult
from evaluation.metrics.evaluation_report import EvaluationReport

from evaluation.benchmark.benchmark_case import BenchmarkCase


class RetrievalEvaluator(BaseEvaluator):

    def evaluate(
        self,
        benchmark: BenchmarkCase,
        retrieved_documents,
        **kwargs
    ) -> EvaluationReport:

        # ---------------------------------------
        # Retrieved document ids (preserve ranking)
        # ---------------------------------------

        retrieved_ids = [

            document.metadata.get(
                "document_id"
            )

            for document in retrieved_documents

            if document.metadata.get(
                "document_id"
            ) is not None

        ]

        expected_ids = benchmark.expected_document_ids

        expected_set = set(expected_ids)

        retrieved_set = set(retrieved_ids)

        intersection = expected_set & retrieved_set

        k = len(retrieved_ids)

        # ---------------------------------------
        # Recall@K
        # ---------------------------------------

        recall = (
            len(intersection)
            /
            len(expected_set)
        ) if expected_set else 0.0

        # ---------------------------------------
        # Precision@K
        # ---------------------------------------

        precision = (
            len(intersection)
            /
            k
        ) if k else 0.0

        # ---------------------------------------
        # Hit Rate
        # ---------------------------------------

        hit_rate = (
            1.0
            if len(intersection) > 0
            else 0.0
        )

        # ---------------------------------------
        # Mean Reciprocal Rank (MRR)
        # ---------------------------------------

        mrr = 0.0

        for rank, document_id in enumerate(retrieved_ids, start=1):

            if document_id in expected_set:

                mrr = 1 / rank

                break

        # ---------------------------------------
        # DCG
        # ---------------------------------------

        dcg = 0.0

        for rank, document_id in enumerate(retrieved_ids, start=1):

            if document_id in expected_set:

                dcg += 1 / log2(rank + 1)

        # ---------------------------------------
        # IDCG
        # ---------------------------------------

        ideal_hits = min(
            len(expected_set),
            k
        )

        idcg = 0.0

        for rank in range(1, ideal_hits + 1):

            idcg += 1 / log2(rank + 1)

        ndcg = (
            dcg / idcg
        ) if idcg else 0.0

        # ---------------------------------------
        # Metrics
        # ---------------------------------------

        metrics = [

            MetricResult(
                name=f"Recall@{k}",
                score=round(recall, 4),
                passed=recall >= 0.80,
                description="Fraction of relevant documents retrieved."
            ),

            MetricResult(
                name=f"Precision@{k}",
                score=round(precision, 4),
                passed=precision >= 0.80,
                description="Fraction of retrieved documents that are relevant."
            ),

            MetricResult(
                name="Hit Rate",
                score=round(hit_rate, 4),
                passed=hit_rate == 1.0,
                description="Whether at least one relevant document was retrieved."
            ),

            MetricResult(
                name="MRR",
                score=round(mrr, 4),
                passed=mrr >= 0.50,
                description="Mean Reciprocal Rank."
            ),

            MetricResult(
                name="nDCG",
                score=round(ndcg, 4),
                passed=ndcg >= 0.80,
                description="Normalized Discounted Cumulative Gain."
            )

        ]

        # ---------------------------------------
        # Report
        # ---------------------------------------

        return EvaluationReport(

            evaluator="Retrieval Evaluator",

            metrics=metrics,

            metadata={

                "query": benchmark.query,

                "retrieval_k": k,

                "expected_document_ids": expected_ids,

                "retrieved_document_ids": retrieved_ids,

                "matched_document_ids": list(intersection)

            }

        )