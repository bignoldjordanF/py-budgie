from project import PBProject
from voter import PBVoter

from typing import List
import warnings

# TODO:
# 1. Change projects, voters type hints
# 2. Consider other metadata parameters

class PBInstance:
    def __init__(
            self,
            description: str = '',
            country: str = '',
            region: str = '',
            district: str = '',
            category: str = '',
            budget: int = 0,
            projects: List['PBProject'] = None,
            voters: List['PBVoter'] = None,
    ):
        self.description = description
        self.country = country
        self.region = region
        self.district = district
        self.category = category
        self.budget = budget
        self._projects = {}
        self._voters = {}

        if projects:
            self.set_projects(projects)

        if voters:
            self.set_voters(voters)

    # --- Projects Property ---

    def projects(self) -> List[PBProject]:
        return self._projects
    
    def set_projects(self, projects: List[PBProject]) -> bool:
        for project in projects:
            self.add_project(project)

    def add_project(self, project: PBProject) -> None:
        if not isinstance(project, PBProject):
            warnings.warn('The project passed is not a PBProject object and has been ignored.', stacklevel=2)
        self._projects[project.id] = project

    def remove_project(self, project_id: int) -> None:
        if project_id not in self._projects:
            warnings.warn('The project id does not exist in the PBInstance.', stacklevel=2)
        self._projects.pop(project_id)
    
    # --- Voters Property ---

    def voters(self) -> List[PBVoter]:
        return self._voters
    
    def set_voters(self, voters: List[PBVoter]) -> bool:
        for voter in voters:
            self.add_voter(voter)
    
    def add_voter(self, voter: PBVoter) -> bool:
        if not isinstance(voter, PBVoter):
            warnings.warn('The voter passed is not a PBVoter object and has been ignored.', stacklevel=2)
            return False

        self._voters[voter.id] = voter
        return True

    def remove_voter(self, voter_id: int) -> bool:
        if voter_id not in self._voters:
            warnings.warn('The voter id does not exist in the PBInstance.', stacklevel=2)
            return False

        self._voters.pop(voter_id)
        return True


if __name__ == '__main__':
    instance = PBInstance(projects=[PBProject(2), PBProject(4)])
    instance.add_project(PBProject(id=1))
    print(instance.projects())
