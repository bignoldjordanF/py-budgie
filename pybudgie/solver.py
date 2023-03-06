from .instance import PBInstance
from .project import PBProject
from .voter import PBVoter

from collections import defaultdict
from typing import Tuple, List
from enum import Enum
import math


# TODO: Think about the utility flattening process. 
# I'm almost certain the egaliatarian and nash
# welfare ideas do not make any sense.


class PBAlgorithm(Enum):
    GREEDY = 0
    RATIO_GREEDY = 1
    SIMULATED_ANNEALING = 2
    GENETIC_ALGORITHM = 3
    DYNAMIC_PROGRAMMING = 4
    BRANCH_AND_BOUND = 5


class PBWelfare(Enum):
    UTILITARIAN = 0
    EGALITARIAN = 1
    NASH = 2

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

        # If the projects list is provided, and thus we want to
        # include them in the election (even if no votes were
        # cast), then we add them all here with a null value
        # and initialise them depending on the welfare:
        flattened = defaultdict(int)  # Project ID -> Utility
        if projects:
            for project in projects:
                flattened[project.id] = -1

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
                    flattened[project] = max(0, flattened[project]) + utility

                # Egalitarian Welfare
                elif self == PBWelfare.EGALITARIAN:
                    if project not in flattened or flattened[project] == -1:
                        flattened[project] = utility
                    flattened[project] = min(flattened[project], utility)

                # Nash Welfare
                elif self == PBWelfare.NASH:
                    flattened[project] = max(0, flattened[project]) + int(math.log(max(1, utility)))

        # We must convert any null utilities to zeroes:
        for pid in flattened:
            if flattened[pid] == -1:
                flattened[pid] = 0
        
        return flattened.keys(), flattened.values()


class PBSolver:
    def __init__(self, instance: PBInstance):
        self.instance: PBInstance = instance
    
    def solve(self, algorithm: PBAlgorithm, maximise_welfare: PBWelfare) -> Tuple[List[int], int]:
        flattened: List[int] = maximise_welfare.flatten(
            voters=self.instance.voters,
            projects=self.instance.projects
        )
        print(flattened)
