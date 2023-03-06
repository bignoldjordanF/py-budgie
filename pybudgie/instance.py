from .project import PBProject
from .voter import PBVoter
from typing import List, Dict


class PBVoter:
    def __init__(
            self,
            id: int,
            age: int = -1,
            sex: str = '',
            neighborhood: str = '',
            voting_method: str = '',
            utilities: Dict[str, int] = None
    ) -> None:
        """
        Constructs a PBVoter object from an id, optional project information and a dictionary of votes over projects.

        Parameters:
            - id (int): The mandatory id of the voter.
            - age (int): The optional age of the voter.
            - sex (str): The optional sex of the voter ('M' or 'F').
            - neighborhood (str): The optional neighborhood of the voter.
            - voting_method (str): The optional method of voting used by the voter.
            Otherwise assumed from the parent instance.
            - utilities (Dict[str, int]): A mapping from project id to cardinal utility
            that this voter derives from each project. For example, in approval
            voting, we might have {'34': 1}, meaning this voter approves project 34.
        """

        self.id = id
        self.age = age
        self.sex = sex
        self.neighborhood = neighborhood
        self.voting_method = voting_method
        self.utilities = {} if not utilities else utilities

    def __repr__(self) -> str:
        return str(self.__dict__)


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
        """
        Returns:
            - List[PBProject]: The projects in the instance as a list.
        """
        return self._projects.values()

    def get_project(self, project_id: int) -> PBProject:
        """
        Parameters:
            - project_id (int): A project id whose PBProject object to return.
        
        Returns:
            - PBProject: A PBProject object with the supplied project id.
        """
        return self._projects[project_id]

    def add_project(self, project: PBProject) -> None:
        """
        Parameters:
            - project (PBProject): A PBProject object to add to the instance.
        """
        self._projects[project.id] = project

    def remove_project(self, project_id: PBProject) -> None:
        """
        Parameters:
            - project_id (int): The project id of the PBProject object to
            remove from the instance.
        """
        if project_id in self._projects:
            self._projects.pop(project_id)

    # --- Voters ---
    @property
    def voters(self) -> List[PBVoter]:
        """
        Returns:
            - List[PBVoter]: The voters in the instance as a list.
        """
        return self._voters.values()

    def get_voter(self, voter_id: int) -> PBVoter:
        """
        Parameters:
            - voter_id (int): A voter id whose PBVoter object to return.
        
        Returns:
            - PBVoter: A PBVoter object with the supplied voter id.
        """
        return self._voters[voter_id]

    def add_voter(self, voter: PBVoter) -> None:
        """
        Parameters:
            - voter (PBVoter): A PBVoter object to add to the instance.
        """
        self._voters[voter.id] = voter

    def remove_voter(self, voter_id: PBVoter) -> None:
        """
        Parameters:
            - voter_id (int): The voter id of the PBVoter object to
            remove from the instance.
        """
        if voter_id in self._voters:
            self._voters.pop(voter_id)

    # --- Dunder ---
    def __str__(self) -> str:
        return str(self.__dict__)
