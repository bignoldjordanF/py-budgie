from typing import List, Tuple


def __run_greedy(
        budget: int,
        candidates: List[Tuple[int, int, int]]
) -> Tuple[List[int], int]:
    
    allocation: List[int] = []
    value: int = 0

    for candidate in candidates:
        if budget == 0:
            break

        if candidate[2] <= budget:
            allocation.append(candidate[0])
            value += candidate[1]
            budget -= candidate[2]
    
    return allocation, value


def ratio_greedy_solver(
        budget: int,
        projects: List[int],
        costs: List[int],
        utilities: List[int]
) -> Tuple[List[int], int]:
    
    candidates = sorted(
        [(project, utilities[i], costs[i]) for i, project in enumerate(projects)],
        key=lambda t: t[1]/t[2],
        reverse=True
    )

    return __run_greedy(budget, candidates)


def greedy_solver(
        budget: int,
        projects: List[int], 
        costs: List[int],
        utilities: List[int]
) -> Tuple[List[int], int]:
    
    candidates = sorted(
        [(project, utilities[i], costs[i]) for i, project in enumerate(projects)],
        key=lambda t: t[1],
        reverse=True
    )

    return __run_greedy(budget, candidates)
