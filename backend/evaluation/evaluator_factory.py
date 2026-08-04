from evaluation.evaluators.dummy_evaluator import DummyEvaluator


class EvaluatorFactory:

    @staticmethod
    def get_evaluator(
        evaluator: str = "dummy"
    ):

        evaluator = evaluator.lower()

        if evaluator == "dummy":

            return DummyEvaluator()

        raise ValueError(
            f"Unsupported evaluator: {evaluator}"
        )