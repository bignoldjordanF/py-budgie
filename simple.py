import pybudgie


def main():
    instance = pybudgie.PBInstance(
        budget = 10_000
    )
    
    instance.projects.append(pybudgie.PBProject(id=1, cost=2_500))
    instance.projects.append(pybudgie.PBProject(id=2, cost=6_500))
    instance.projects.append(pybudgie.PBProject(id=3, cost=1_500))
    instance.projects.append(pybudgie.PBProject(id=4, cost=8_000))

    instance.voters.append(pybudgie.PBVoter(id=1, votes={1: 1, 3: 1, 4: 1}))
    instance.voters.append(pybudgie.PBVoter(id=2, votes={2: 1, 3: 1}))
    instance.voters.append(pybudgie.PBVoter(id=3, votes={3: 1, 4: 1}))
    instance.voters.append(pybudgie.PBVoter(id=3, votes={1: 1}))

    print(instance)


if __name__ == '__main__':
    main()
