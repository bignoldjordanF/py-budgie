from pybudgie import PBInstance, PBProject, PBVoter
from pybudgie import PBSolver, PBAlgorithm, PBWelfare
from pybudgie import PBResult
from pybudgie.pbgenerator import generate_instance
from pybudgie.pbreader import read_file


def simple():
    """
    An example demonstrating the creation of a PBInstance with
    manually defined values.
    """

    # Syntax: PBInstance(
    #   Optional Parameters...
    # )
    instance = PBInstance(
        budget = 10_000,
        # ...
    )
    
    # Add Projects
    instance.add_project(PBProject(id=1, cost=2_500))
    instance.add_project(PBProject(id=2, cost=6_500))
    instance.add_project(PBProject(id=3, cost=1_500))
    instance.add_project(PBProject(id=4, cost=8_000))

    # Add Voters & Votes
    instance.add_voter(PBVoter(id=1, utilities={1: 1, 3: 1, 4: 1}))
    instance.add_voter(PBVoter(id=2, utilities={2: 1, 3: 1}))
    instance.add_voter(PBVoter(id=3, utilities={3: 1, 4: 1}))
    instance.add_voter(PBVoter(id=4, utilities={1: 1}))

    return instance


def generated():
    """
    An example demonstrating the random generation of a
    PBInstance with some predefined limits.
    """

    # Syntax: generate_instance(
    #   Optional Parameters...
    # )
    instance: PBInstance = generate_instance(
        min_budget=1_000_000,
        max_budget=10_000_000,
        voting_chance=0.1
        # ...
    )
    return instance


def parsed():
    """
    An example demonstrating the creation of a PBInstance
    from a .pb file in the format provided by pabulib.org.
    """

    # Syntax: read_file('path/to/pb/file.pb')
    instance: PBInstance = \
        read_file('resources/poland_warszawa_2019_ursynow.pb')
    return instance


def solve(instance: PBInstance):
    """
    An example showing how the solving algorithms can be
    individually called to retrieve potential allocations.
    """
    
    solver: PBSolver = PBSolver(instance)
    result: PBResult = solver.solve(PBAlgorithm.DYNAMIC_PROGRAMMING, PBWelfare.UTILITARIAN)
    print(result.runtime_ms)

    # Examples:
    # - solver.solve(PBAlgorithm.GREEDY, PBWelfare.UTILITARIAN)
    # - solver.solve(PBAlgorithm.SIMULATED_ANNEALING, PBWelfare.UTILITARIAN)
    # - solver.solve(PBAlgorithm.GENETIC_ALGORITHM, PBWelfare.UTILITARIAN)
    # - solver.solve(PBAlgorithm.DYNAMIC_PROGRAMMING, PBWelfare.UTILITARIAN)
    # - solver.solve(PBAlgorithm.BRANCH_AND_BOUND, PBWelfare.UTILITARIAN)


def main():
    instance: PBInstance = parsed()
    solve(instance)


if __name__ == '__main__':
    main()
