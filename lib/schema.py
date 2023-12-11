from dataclasses import dataclass
from typing import List

@dataclass
class Embedding:
    title: str
    timestamp: int
    vector: List[float]

@dataclass
class Result:
    title: str
    embeddings: List[Embedding]