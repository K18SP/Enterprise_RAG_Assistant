from evaluation.evaluator_factory import EvaluatorFactory

from utils.logger import setup_logger


logger = setup_logger(__name__)


class EvaluationService:

    def __init__(self):

        self.pipeline = (
            EvaluatorFactory.create_pipeline()
        )

    def evaluate(self, **kwargs):

        return self.pipeline.evaluate(
            **kwargs
        )