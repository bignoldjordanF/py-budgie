from .project import PBProject
from .voter import PBVoter
from typing import List, Dict


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
    ) -> None:
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
        self._projects = {} if not projects else {project.id: project for project in projects}
        self._voters = {} if not voters else {voter.id: voter for voter in voters}
    
    # --- Projects ---
    @property
    def projects(self) -> List[PBProject]:
        return self._projects.values()

    def get_project(self, project_id: int) -> PBProject:
        return self._projects[project_id]

    def add_project(self, project: PBProject) -> None:
        self._projects[project.id] = project

    def remove_project(self, project_id: PBProject) -> None:
        if project_id in self._projects:
            self._projects.pop(project_id)

    # --- Voters ---
    @property
    def voters(self) -> List[PBVoter]:
        return self._voters.values()

    def get_voter(self, voter_id: int) -> PBVoter:
        return self._voters[voter_id]

    def add_voter(self, voter: PBVoter) -> None:
        self._voters[voter.id] = voter

    def remove_voter(self, voter_id: PBVoter) -> None:
        if voter_id in self._voters:
            self._voters.pop(voter_id)

    # --- Dunder ---
    def __str__(self) -> str:
        return str(self.__dict__)
