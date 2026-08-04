from pydantic import BaseModel


class MetricResult(BaseModel):

    name: str

    score: float

    passed: bool

    description: str

"""
Example;

{
    "name": "Recall@5",
    "score": 0.92,
    "passed": true,
    "description": "Retriever returned relevant documents."
}
"""