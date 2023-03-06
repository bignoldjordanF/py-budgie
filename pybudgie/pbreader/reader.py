from ..instance import PBInstance
from ..project import PBProject
from ..voter import PBVoter

from collections import defaultdict
from typing import List, Dict
import random
import string
import csv


# Warning: This is untested!
# TODO: We need to test for lots of .pb files.


def __random_id():
    """
    Returns:
        - A random 8-character alpha-numeric string object.
    """
    # Reference: https://stackoverflow.com/questions/13484726/safe-enough-8-character-short-unique-random-string
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))


def derive_utilities(
        vote_type: str,
        votes: List[str],
        points: List[str]=None,
        num_projects: int=0
) -> Dict[str, int]:
    """
    Derives the utilities that voters derive from projects from a set of
    voting data found in .pb files.

    Parameters:
        - vote_type (str): One of "approval", "ordinal", "cumulative" or "scoring".
        This defaults to "approval" voting.
        - votes (List[str]): A list of project ids which the voter is expressing their
        preference over. For example, ["4", "69", "3", "2"].
        - points (List[str]): A list of points used in "cumulative" or "scoring" to
        express, in order, the number of points assigned to each project id in votes.
        - num_projects (List[str]): The number of projects in the instance to derive
        utilities in "ordinal" voting.
    
    Returns:
        - Dict[str, int]: A dictionary of project ids mapped to integer utility values.
        Please note that not *all* projects are returned, only those the voter has
        expressed their preferences over.
    """

    # "approval", "ordinal", "cumulative" or "scoring"
    stripped_voting_method = vote_type.strip().lower()

    # Convert Points To Integers
    points = [int(point) if point.isnumeric() else 0 for point in points]

    # Ordinal Voting Method
    if stripped_voting_method == 'ordinal':
        num_projects = max(num_projects, len(votes))
        return {pid: num_projects - count for count, pid in enumerate(votes)}
    
    # Cumulative & Scoring Voting Method
    if stripped_voting_method in ('cumulative', 'scoring'):
        discrep_limit = min(len(votes), len(points) if points else 0)
        points = points if points else [0] * discrep_limit
        votes, points = votes[:discrep_limit], points[:discrep_limit]
        return {pid: points[id] for id, pid in enumerate(votes)}

    # Approval Voting
    return {pid: 1 for pid in votes}


# Reference:
# [1] http://pabulib.org/format
# [2] http://pabulib.org/code

def read_file(filepath: str) -> PBInstance:
    """
    Reads the contents of a .pb file [1] into a PBFileContents
    dataclass object. See reference [2] for source.

    Parameters:
        - filepath (str): The path to the .pb file.

    Returns:
        - PBInstance
    """

    metadata, projects, votes = defaultdict(str), {}, {}
    
    if not filepath.endswith('.pb'):
        filepath += '.pb'

    with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
        section, header, reader = '', [], csv.reader(csvfile, delimiter=';')
        for row in reader:
            if str(row[0]).strip().lower() in ('meta', 'projects', 'votes'):
                section = str(row[0]).strip().lower()
                header = next(reader)

            elif section == 'meta':
                metadata[row[0]] = row[1].strip()

            elif section == 'projects':
                projects[row[0]] = defaultdict(str)
                for it, key in enumerate(header[1:]):
                    projects[row[0]][key.strip()] = row[it+1].strip()
            
            elif section == 'votes':
                votes[row[0]] = defaultdict(str)
                for it, key in enumerate(header[1:]):
                    votes[row[0]][key.strip()] = row[it+1].strip()
    
    # Force Budget Value
    if metadata['budget'] == '' or \
        not metadata['budget'].isnumeric():
            metadata['budget'] = 0


    instance = PBInstance(
        description=metadata['description'],
        budget=int(metadata['budget']),
        country=metadata['country'],
        region=metadata['unit'],
        district=metadata['district'],
        categories=metadata['subunit'].split(',')
    )

    for pid, project in projects.items():

        # Force Project ID
        if pid == '':
            pid = __random_id()

        # Force Project Cost
        if project['cost'] == '' or \
            not project['cost'].isnumeric():
                project['cost'] = 0

        instance.projects.append(PBProject(
            id=pid,
            name=project['name'],
            cost=int(project['cost']),
            categories=project['category'].split(','),
            targets=project['target'].split(',')
        ))

    for vid, voter in votes.items():
        
        # Force Voter ID
        if vid == '':
            vid = __random_id()

        # Force Age Numeric
        if not voter['age'].isnumeric():
            voter['age'] = -1
        
        vote_type = metadata['vote_type']
        voter_votes = voter['vote'].split(',')
        voter_points = voter['points'].split(',')
        num_projects = len(instance.projects)

        voter_utilities = derive_utilities(
            vote_type=vote_type,
            votes=voter_votes,
            points=voter_points,
            num_projects=num_projects
        )

        instance.voters.append(PBVoter(
            id=vid,
            age=voter['age'],
            sex=voter['sex'],
            neighborhood=voter['neighborhood'],
            voting_method=voter['voting_method'],
            utilities=voter_utilities
        ))
    
    return instance
