from ..instance import PBInstance
from ..project import PBProject
from ..voter import PBVoter
import random


def generate_instance(
        min_budget: int = 100_000,
        max_budget: int = 1_000_000,
        min_num_projects: int = 10,
        max_num_projects: int = 100,
        min_project_cost: int = 10_000,
        max_project_cost: int = 1_000_000,
        min_num_voters: int = 500,
        max_num_voters: int = 10_000,
        voting_chance: float = 0.3,
        generate_metadata: bool = False
) -> PBInstance:
    """
    Randomly generates an approval-voting PBInstance within default or provided parameters.
    By approval voting, we mean that projects are either approved or they are not, i.e.,
    binary utilities.

    Parameters:
        - min_budget (int): The minimum budget that will be generated for the instance.
        - max_budget (int): The maximum budget that will be generated for the instance.
        - min_num_projects (int): The minimum number of projects that will be generated for the instance.
        - max_num_projects (int): The maximum number of projects that will be generated for the instance.
        - min_project_cost (int): The minimum project cost possible for each project in the instance.
        - max_project_cost (int): The maximum project cost possible for each project in the instance.
        - min_num_voters (int): The minimum number of voters voting on projects in the instance.
        - max_num_voters (int): The maximum number of voters voting on projects in the instance.
        - voting_chance (float): The probability of a voter voting on a project.
        - generate_metadata (bool): This is not yet implemented. It will randomly generate instance,
        project and voter string data.

    returns:
        - PBInstance
    """

    # Generate Budget
    budget = random.randint(min_budget, max_budget)

    # Create PBInstance
    instance = PBInstance(
        description='A randomly generated participatory budgeting instance!',
        budget=budget
    )

    # Generate Num Projects
    num_projects = random.randint(min_num_projects, max_num_projects)

    # Generate Projects
    for id in range(num_projects):
        instance.projects.append(PBProject(
            id=id+1,
            cost=random.randint(min_project_cost, max_project_cost),
            name=f'Random Project {id}'
        ))

    # Generate Num Voters
    num_voters = random.randint(min_num_voters, max_num_voters)

    # Generate Voters & Votes
    for id in range(num_voters):
        votes = {}
        for pid in range(num_projects):
            # The voting chance decides the number
            # of projects voted on per user:
            if random.random() < voting_chance:
                votes[pid+1] = 1
        instance.voters.append(PBVoter(
            id=id+1,
            utilities=votes
        ))

    return instance
