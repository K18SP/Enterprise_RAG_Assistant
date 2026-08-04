from pydantic import BaseModel
from typing import List


class BenchmarkCase(BaseModel):

    query: str

    expected_document_ids: List[str]

    expected_answer: str | None = None

    expected_keywords: List[str] = []

"""
Example;

BenchmarkCase(
    query="Tell me about ML",

    expected_sources=[
        "sample.txt"
    ]
)

"""