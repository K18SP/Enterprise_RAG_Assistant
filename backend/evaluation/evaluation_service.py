from evaluation.evaluator_factory import EvaluatorFactory

from utils.logger import setup_logger


logger = setup_logger(__name__)


class EvaluationService:

    def __init__(
        self,
        evaluator: str = "dummy"
    ):

        logger.info(
            "Initializing Evaluation Service."
        )

        self.evaluator = (
            EvaluatorFactory.get_evaluator(
                evaluator
            )
        )

        logger.info(
            "Evaluation Service initialized."
        )


    def evaluate(
        self,
        **kwargs
    ):

        logger.info(
            "Running evaluation."
        )

        report = self.evaluator.evaluate(
            **kwargs
        )

        logger.info(
            "Evaluation completed."
        )

        return report