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
            categories: List[str] = None,
            budget: int = 0,
            projects: List[PBProject] = None,
            voters: List[PBVoter] = None,
    ):
        """
        Constructs a PBInstance from optional metadata, a budget and a list of projects and voters.

        Parameters:
            - description (str): A description of the objective of the instance.
            - country (str): The country in which the instance takes place.
            - region (str): The region of said country in which in the instance takes place.
            - district (str): The district of said region in which the instance takes place.
            - categories (List[str]): The categories of the instance.
            - budget (int): The maximum budget of the instance.
            - projects (List[PBProject]): A list of PBProject objects which wrap the projects to be funded.
            - voters (List[PBVoter]): A list of PBVoter objects which wrap the voters and their votes on the projects.
        """

        # These attributes can and should be accessed
        # directly from the object.
        self.description = description
        self.country = country
        self.region = region
        self.district = district
        self.categories = [] if not categories else categories
        self.budget = budget
        self.projects = [] if not projects else projects
        self.voters = [] if not voters else voters
    
    def __str__(self):
        return str(self.__dict__)
