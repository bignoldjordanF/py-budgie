from typing import List
from enum import Enum


class PBVoteType(Enum):
    APPROVAL = 0
    ORDINAL = 1
    CUMULATIVE = 2
    SCORING = 3
    NONE = 4

    def from_string(self, type: str) -> 'PBVoteType':
        stripped: str = type.strip().lower()

        if stripped == 'approval':
            return PBVoteType.APPROVAL
        elif stripped == 'ordinal':
            return PBVoteType.ORDINAL
        elif stripped == 'cumulative':
            return PBVoteType.CUMULATIVE
        elif stripped == 'scoring':
            return PBVoteType.SCORING

        return PBVoteType.NONE


class PBInstance:
    def __init__(
            self,
            description: str = '',
            budget: int = 0,
            vote_type: str = PBVoteType.NONE,
            country: str = '',
            region: str = '',
            district: str = '',
            category: str = '',
    ):
        # These attributes can and should be accessed
        # directly from the object.
        self.description = description
        self.budget = budget
        self.vote_type = vote_type
        self.country = country
        self.region = region
        self.district = district
        self.category = category
    
    def __str__(self):
        return str(self.__dict__)
