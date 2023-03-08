from .instance import PBInstance
from .project import PBProject
from .voter import PBVoter
from .algorithms import greedy_solver, \
    ratio_greedy_solver, \
    simulated_annealing_solver, \
    genetic_algorithm_solver, \
    dynamic_programming_solver, \
    branch_and_bound_solver
from .result import PBResult
        

from timeit import default_timer as timer
from typing import Tuple, List, Dict
from collections import defaultdict
from enum import Enum
import logging


class PBAlgorithm(Enum):
    GREEDY = 0
    RATIO_GREEDY = 1
    SIMULATED_ANNEALING = 2
    GENETIC_ALGORITHM = 3
    DYNAMIC_PROGRAMMING = 4
    BRANCH_AND_BOUND = 5


class PBWelfare(Enum):
    UTILITARIAN = 0

    def flatten(
            self,
            voters: List[PBVoter],
            projects: List[PBProject]=None,
    ) -> Tuple[List[str], List[int]]:
        """
        Flattens a list of voters, i.e., their utilities over projects, into
        two lists of projects and total utilities by aggregating votes using
        some welfare function to be maximised.

        Parameters:
            - voters (List[PBVoter]): A list of PBVoter objects containing the
            voters and specifically their utilities over projects.
            - projects (List[PBProject]): An optional list of PBProject objects
            containing the projects. If this is provided, then all projects
            in the election will be considered, even if they have no votes.
            Otherwise, only those projects with votes will be considered.
        
        Returns:
            - Tuple[List[str], List[int]]: The first index contains a list of
            the project ids, and the second index contains the flattened
            total utility for each project (sequentially).
        """

        flattened = defaultdict(int)  # Project ID -> Utility
        if projects:
            for project in projects:
                flattened[project.id] = 0

        # We aggregate the utilities of all the voters,
        # using the welfare functions:
        for voter in voters:
            for project, utility in voter.utilities.items():

                # Ignore any votes for unlisted projects
                # if and only if the projects list is
                # provided in the function call:
                if projects and project not in flattened:
                    continue

                # Utilitarian Welfare
                if self == PBWelfare.UTILITARIAN:
                    flattened[project] += utility

        return flattened


class PBSolver:
    def __init__(self, instance: PBInstance):
        self.instance: PBInstance = instance
    
    def solve(self, algorithm: PBAlgorithm, maximise_welfare: PBWelfare) -> PBResult:
        """
        Finds an allocation for the participatory budgeting instance using the provided algorithm
        to maximise the provided welfare function.

        Parameters:
            - algorithm (PBAlgorithm): The algorithm to use to find the allocation by maximising
            the welfare function, e.g., PBAlgorithm.GREEDY, PBAlgorithm.GENETIC_ALGORITHM, etc.
            - maximise_welfare (PBWelfare): The welfare function to be maximised in finding
            the allocation, e.g., PBWelfare.UTILITARIAN.

        Returns:
            - Tuple[List[int], int]: A pair containing the allocation found, as a list of project
            ids, and the overall value with regard to the welfare function.
        """

        # TODO: Rethink the flattening function, i.e., do we want it to
        # return a dictionary which we need to process further?
        # Do we want to do this every time we call this function?

        start_time = timer()

        # Flatten the individual voter utilities into a one-dimension:
        flattened: Dict[str, int] = maximise_welfare.flatten(
            voters=self.instance.voters,
            projects=self.instance.projects
        )

        # Convert the instance into three separate lists for solving:
        projects: List[str] = [project for project in flattened.keys()]
        costs: List[int] = [self.instance.get_project(project_id).cost for project_id in flattened.keys()]
        utilities: List[int] = [project for project in flattened.values()]

        allocation: List[int] = []
        utility: int = 0

        # Compute the result using the provided algorithm:
        if algorithm == PBAlgorithm.GREEDY:
            allocation, utility = greedy_solver(
                budget=self.instance.budget,
                projects=projects,
                costs=costs,
                utilities=utilities
            )
        
        if algorithm == PBAlgorithm.RATIO_GREEDY:
            allocation, utility = ratio_greedy_solver(
                budget=self.instance.budget,
                projects=projects,
                costs=costs,
                utilities=utilities
            )

        if algorithm == PBAlgorithm.SIMULATED_ANNEALING:
            allocation, utility = simulated_annealing_solver(
                budget=self.instance.budget,
                projects=projects,
                costs=costs,
                utilities=utilities
            )

        if algorithm == PBAlgorithm.GENETIC_ALGORITHM:
            allocation, utility = genetic_algorithm_solver(
                budget=self.instance.budget,
                projects=projects,
                costs=costs,
                utilities=utilities,
                population_size=1000,
                num_generations=250
            )

        if algorithm == PBAlgorithm.DYNAMIC_PROGRAMMING:
            logging.warning('Dynamic programming is an exact algorithm and may take a long time!')
            allocation, utility = dynamic_programming_solver(
                budget=self.instance.budget,
                projects=projects,
                costs=costs,
                utilities=utilities
            )

        if algorithm == PBAlgorithm.BRANCH_AND_BOUND:
            logging.warning('Branch and bound is an exact algorithm and may take a long time!')
            allocation, utility = branch_and_bound_solver(
                budget=self.instance.budget,
                projects=projects,
                costs=costs,
                utilities=utilities
            )

        end_time = timer()
        runtime_ms: float = (end_time - start_time) * 1_000

        return PBResult(allocation, utility, runtime_ms)
