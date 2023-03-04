from .project import PBProject
from .voter import PBVoter
from typing import List


class PBInstance:
    def __init__(
            self,
            description: str = '',
            country: str = '',
            region: str = '',
            district: str = '',
            category: str = '',
            budget: int = 0,
            projects: List[PBProject] = None,
            voters: List[PBVoter] = None,
    ):
        # These attributes can and should be accessed
        # directly from the object.
        self.description = description
        self.country = country
        self.region = region
        self.district = district
        self.category = category
        self.budget = budget
        self.projects = [] if not projects else projects
        self.voters = [] if not voters else voters
    
    def __str__(self):
        return str(self.__dict__)
