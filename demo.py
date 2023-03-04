import pbreader
import pybudgie


def main():
    contents = pbreader.read_pb_file('resources/france_toulouse_2019_.pb')
    metadata, projects, voters = contents.metadata, contents.projects, contents.voters

    instance = pybudgie.PBInstance(
        description = metadata['description'],
        budget = metadata['budget'],
        country = metadata['country'],
        region = metadata['unit'],
        district = metadata['district'],
        category = metadata['subunit'],
    )

    for pid, project in projects.items():
        instance.projects.append(pybudgie.PBProject(
            id = pid,
            name = project['name'],
            cost = project['cost'],
            categories = project['category'].split(','),
            targets = project['target'].split(',')
        ))
    
    for vid, voter in voters.items():
        instance.voters.append(pybudgie.PBVoter(
            id = vid,
            age = voter['age'],
            sex = voter['sex'],
            neighborhood = voter['neighborhood'],
            voting_method = voter['voting_method'],
            votes = pbreader.votes_to_dict(voter['vote'].split(','), metadata['vote_type'])
        ))
    
    print(instance)


if __name__ == '__main__':
    main()
