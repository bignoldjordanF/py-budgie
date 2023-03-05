from pybudgie import PBInstance, PBProject, PBVoter


def simple():
    instance = PBInstance(
        budget = 10_000
    )
    
    instance.projects.append(PBProject(id=1, cost=2_500))
    instance.projects.append(PBProject(id=2, cost=6_500))
    instance.projects.append(PBProject(id=3, cost=1_500))
    instance.projects.append(PBProject(id=4, cost=8_000))

    instance.voters.append(PBVoter(id=1, votes={1: 1, 3: 1, 4: 1}))
    instance.voters.append(PBVoter(id=2, votes={2: 1, 3: 1}))
    instance.voters.append(PBVoter(id=3, votes={3: 1, 4: 1}))
    instance.voters.append(PBVoter(id=3, votes={1: 1}))
    return instance


def generated():
    from pybudgie.generator import generate_instance

    # Syntax: generate_instance(optional_params...)
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
    print(instance)
