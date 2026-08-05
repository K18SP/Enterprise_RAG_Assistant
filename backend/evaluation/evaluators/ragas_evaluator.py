from ragas import evaluate

from ragas.metrics import (

    faithfulness,

    answer_relevancy,

    context_precision,

    context_recall

)

from evaluation.evaluators.base_evaluator import BaseEvaluator

from evaluation.adapters.ragas_adapter import RAGASAdapter

from evaluation.metrics.evaluation_report import EvaluationReport
from evaluation.metrics.metric_result import MetricResult

class RAGASEvaluator(BaseEvaluator):

    def evaluate(
        self,
        benchmark,
        generated_answer,
        retrieved_documents,
        **kwargs
    ):

        contexts = [

            document.page_content

            for document in retrieved_documents

        ]

        dataset = RAGASAdapter.to_dataset(

            query=benchmark.query,

            answer=generated_answer,

            contexts=contexts,

            ground_truth=benchmark.expected_answer

        )

        results = evaluate(

            dataset,

            metrics=[

                faithfulness,

                answer_relevancy,

                context_precision,

                context_recall

            ]

        )

        scores = results.to_pandas().iloc[0]

        metrics = [

            MetricResult(

                name="Faithfulness",

                score=float(scores["faithfulness"]),

                passed=scores["faithfulness"] >= 0.8,

                description="Answer is supported by retrieved context."

            ),

            MetricResult(

                name="Answer Relevancy",

                score=float(scores["answer_relevancy"]),

                passed=scores["answer_relevancy"] >= 0.8,

                description="Answer relevance."

            ),

            MetricResult(

                name="Context Precision",

                score=float(scores["context_precision"]),

                passed=scores["context_precision"] >= 0.8,

                description="Retrieved context quality."

            ),

            MetricResult(

                name="Context Recall",

                score=float(scores["context_recall"]),

                passed=scores["context_recall"] >= 0.8,

                description="Context completeness."

            )

        ]

        return EvaluationReport(

            evaluator="RAGAS",

            metrics=metrics,

            metadata={

                "query": benchmark.query

            }

        )