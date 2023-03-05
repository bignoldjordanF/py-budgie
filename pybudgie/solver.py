from enum import Enum


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


class PBSolver:
    pass

