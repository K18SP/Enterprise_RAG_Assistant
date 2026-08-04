from abc import ABC, abstractmethod

from evaluation.metrics.evaluation_report import EvaluationReport


class BaseEvaluator(ABC):

    @abstractmethod
    def evaluate(
        self,
        **kwargs
    ) -> EvaluationReport:
        """
        Evaluate the RAG pipeline and return
        a structured evaluation report.
        """
        pass