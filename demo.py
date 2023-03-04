import pbreader
import pybudgie


def votes_to_dict(votes, vote_type, points=None, num_projects=0):
    if vote_type=='ordinal':
        num_projects = max(num_projects, len(votes))
        return {pid: num_projects-count for count, pid in enumerate(votes)}
    if vote_type=='cumulative' or vote_type=='scoring':
        points = [0] * len(votes) if not points else points
        return {pid: points[id] for id, pid in enumerate(votes)}
    return {pid: 1 for pid in votes}  # Approval


def main():
    contents = pbreader.read_pb_file('resources/poland_warszawa_2019_ursynow.pb')
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
            votes = votes_to_dict(voter['vote'].split(','), 'approval')
        ))
    
    print(instance)


if __name__ == '__main__':
    main()
