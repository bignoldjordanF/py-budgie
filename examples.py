from pybudgie import PBInstance, PBProject, PBVoter


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
    instance.projects.append(PBProject(id=1, cost=2_500))
    instance.projects.append(PBProject(id=2, cost=6_500))
    instance.projects.append(PBProject(id=3, cost=1_500))
    instance.projects.append(PBProject(id=4, cost=8_000))

    # Add Voters & Votes
    instance.voters.append(PBVoter(id=1, utilities={1: 1, 3: 1, 4: 1}))
    instance.voters.append(PBVoter(id=2, utilities={2: 1, 3: 1}))
    instance.voters.append(PBVoter(id=3, utilities={3: 1, 4: 1}))
    instance.voters.append(PBVoter(id=4, utilities={1: 1}))

    return instance


def generated():
    """
    An example demonstrating the random generation of a
    PBInstance with some predefined limits.
    """

    from pybudgie.pbgenerator import generate_instance

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

    from pybudgie.pbreader import read_file

    # Syntax: read_file('path/to/pb/file.pb')
    instance: PBInstance = \
        read_file('resources/poland_warszawa_2019_ursynow.pb')
    return instance


def solve(instance: PBInstance):
    """
    An example showing how the solving algorithms can be
    individually called to retrieve potential allocations.
    """
    
    from pybudgie import PBSolver, PBAlgorithm, PBWelfare
    solver: PBSolver = PBSolver(instance)
    result = solver.solve(PBAlgorithm.GREEDY, PBWelfare.UTILITARIAN)
    print(result)


def main():
    instance: PBInstance = parsed()
    solve(instance)


if __name__ == '__main__':
    main()
