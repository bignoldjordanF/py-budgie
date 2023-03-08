from dataclasses import dataclass
from typing import List


@dataclass
class PBResult:
    allocation: List[int]
    utility: int
    runtime_ms: float

