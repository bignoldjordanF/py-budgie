from pybudgie import PBInstance, PBProject, PBVoter, PBWelfare


def simple():
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
    instance.voters.append(PBVoter(id=1, votes={1: 1, 3: 1, 4: 1}))
    instance.voters.append(PBVoter(id=2, votes={2: 1, 3: 1}))
    instance.voters.append(PBVoter(id=3, votes={3: 1, 4: 1}))
    instance.voters.append(PBVoter(id=3, votes={1: 1}))

    return instance


def generated():
    from pybudgie.pbgenerator import generate_instance

    # Syntax: generate_instance(
    #   Optional Parameters...
    # )
    instance: PBInstance = generate_instance(
        min_budget=1_000_000,
        max_budget=10_000_000,
        # ...
    )
    return instance


def parsed():
    from pybudgie.pbreader import read_file

    # Syntax: read_file('path/to/pb/file.pb')
    instance: PBInstance = \
        read_file('resources/poland_warszawa_2019_ursynow.pb')
    return instance


if __name__ == '__main__':
    instance = generated()

    from pybudgie.solvers import greedy_solver
    result = greedy_solver(instance, PBWelfare.UTILITARIAN)
