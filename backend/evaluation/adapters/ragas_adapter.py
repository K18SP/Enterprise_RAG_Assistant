from datasets import Dataset


class RAGASAdapter:

    @staticmethod
    def to_dataset(
        query: str,
        answer: str,
        contexts: list[str],
        ground_truth: str
    ):

        return Dataset.from_dict(

            {

                "question": [query],

                "answer": [answer],

                "contexts": [contexts],

                "ground_truth": [ground_truth]

            }

        )