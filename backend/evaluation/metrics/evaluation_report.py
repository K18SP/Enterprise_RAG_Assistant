from pydantic import BaseModel
from typing import List

from .metric_result import MetricResult


class EvaluationReport(BaseModel):

    evaluator: str

    metrics: List[MetricResult]

    metadata: dict = {}

"""
Example;

{
  "evaluator": "retrieval",

  "metrics": [
      ...
  ],

  "metadata": {
      "documents":5
  }
}
"""