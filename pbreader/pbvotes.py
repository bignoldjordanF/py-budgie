from typing import List


def votes_to_dict(votes: List[str], vote_type: str, points: List[str] = None, num_projects: int = 0):
    """
    Converts a list of votes [and points] to a dictionary of cardinal
    utilities that each voter derives from each project.

    Parameters:
        - votes (List[str]): A list of project ids which the voter has voted for.
        - vote_type (str): The type of voting method, i.e., approval, ordinal, cumulative or scoring.
        - points (List[str]): A list of ordered points associated with each project id for cumulative or scoring methods.
        - num_projects (int): The number of projects in the instance for ordinal voting.
    """
    
    # Ordinal Voting
    if vote_type == 'ordinal':
        num_projects = max(num_projects, len(votes))
        return {pid: num_projects-count for count, pid in enumerate(votes)}
    
    # Cumulative/Scoring Voting
    if vote_type=='cumulative' or vote_type=='scoring':
        points = [0] * len(votes) if not points else points
        return {pid: points[id] for id, pid in enumerate(votes)}
    
    # Approval Voting
    return {pid: 1 for pid in votes}
