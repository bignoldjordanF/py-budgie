from typing import List, Tuple


def greedy_solver(
        budget: int,
        projects: List[int], 
        costs: List[int],
        utilities: List[int]
) -> Tuple[List[int], int]:
    
    S = sorted(
        [(project, costs[i], utilities[i]) for i, project in enumerate(projects)],
        key=lambda t: t[2],
        reverse=True
    )

    allocation: List[int] = []
    value: int = 0
    
    idx: int = 0
    while 0 < budget and idx < len(S):
        candidate: Tuple[str, int, int] = S[idx]
        if candidate[1] <= budget:
            allocation.append(candidate[0])
            value += candidate[2]
            budget -= candidate[1]
        idx += 1

    return allocation, value
