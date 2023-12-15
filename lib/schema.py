from dataclasses import dataclass
from typing import Tuple
from datetime import timedelta

@dataclass
class Embedding:
    title: str
    timestamp: timedelta
    vector: Tuple[float]

@dataclass
class Result:
    title: str
    embeddings: Tuple[Embedding]

    def __str__(self):
        return 'Result'
    
@dataclass
class PredictResult:
    name: str
    hours: int
    minutes: int
    seconds: int
    score: int