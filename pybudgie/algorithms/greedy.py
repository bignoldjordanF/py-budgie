from typing import List, Tuple


def __run_greedy(
        budget: int,
        candidates: List[Tuple[int, int, int]]
) -> Tuple[List[int], int]:
    
    allocation: List[int] = []
    value: int = 0

    # Iterate through candidates until the budget
    # is exhausted, adding valid candidates to the
    # allocation:
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
    """
    A fast approximation scheme for participatory budgeting problems
    formulated as the binary knapsack problem. The candidates are
    sorted in descending order by their utility-weight ratio and
    picked one by one until the budget or candidates are exhausted.

    Parameters:
        - budget (int): The total budget of the instance.
        - projects (List[int]): A list of project identifiers.
        - costs (List[int]): A list of project costs.
        - utilities (List[int]): A list of project utilities.

    Returns:
        - Tuple[List[int], int]: A pair containing the allocation found, as a list of project
        ids, and the overall value with regard to the welfare function.
    """
    
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
    """
    A fast approximation scheme for participatory budgeting problems
    formulated as the binary knapsack problem. The candidates are
    sorted in descending order by their utilities and picked one
    by one until the budget or candidates have been exhausted.

    Parameters:
        - budget (int): The total budget of the instance.
        - projects (List[int]): A list of project identifiers.
        - costs (List[int]): A list of project costs.
        - utilities (List[int]): A list of project utilities.

    Returns:
        - Tuple[List[int], int]: A pair containing the allocation found, as a list of project
        ids, and the overall value with regard to the welfare function.
    """
    
    candidates = sorted(
        [(project, utilities[i], costs[i]) for i, project in enumerate(projects)],
        key=lambda t: t[1],
        reverse=True
    )

    return __run_greedy(budget, candidates)
