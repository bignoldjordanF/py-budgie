def votes_to_dict(votes, vote_type, points=None, num_projects=0):
    
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
