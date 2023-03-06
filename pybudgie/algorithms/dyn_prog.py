from typing import List, Tuple


def dynamic_programming_solver(
        budget: int,
        projects: List[int], 
        costs: List[int],
        utilities: List[int]
) -> Tuple[List[int], int]:
    """
    An exact algorithm for participatory budgeting problems formulated as the
    binary knapsack problem.

    We build a dynamic programming matrix that holds the maximum value achievable
    at any (i, j) pair, where i means we only have access to the first i projects, 
    i.e., {1, 2, ..., i}, and j means we only have j budget available. The base
    cases are simple: dp[0][j] = 0 for all j because there are no items to choose
    from, and dp[i][0] = 0 for all i, assuming all values are positive, because
    we have no budget. Each successive case can then use previous solutions.

    Parameters:
        - budget (int): The total budget of the instance.
        - projects (List[int]): A list of project identifiers.
        - costs (List[int]): A list of project costs.
        - utilities (List[int]): A list of project utilities.

    Returns:
        - Tuple[List[int], int]: A pair containing the allocation found, as a list of project
        ids, and the overall value with regard to the welfare function.
    """
    
    # The dynamic programming matrix is initialised with zeroes,
    # thuis the base cases are already filled:
    dp: List[List[int]] = [
        [0 for _ in range(budget + 1)]
        for _ in range(len(projects) + 1)
    ]

    # We iterate through every possible item subset with every
    # possible integer budget {1, 2, ..., budget}:
    for i in range(1, len(projects) + 1):
        for j in range(1, budget + 1):

            # At each (i, j) pair, we decide either to exclude
            # or include the item i:
            utility_without_project: int = dp[i - 1][j]
            budget_can_fund: bool = costs[i - 1] <= j

            # If the capacity cannot include i, naturally
            # exclude it:
            if not budget_can_fund:
                dp[i][j] = utility_without_project
                continue

            # Otherwise, our value is the current item value,
            # plus the maximum value achievable with the 
            # remaining items {1, 2, ..., i - 1} and the
            # remaining budget j - costs[i].
            utility_with_project: int = dp[i - 1][j - costs[i - 1]] + utilities[i - 1]
            dp[i][j] = max(utility_with_project, utility_without_project)
    
    # The best value is stored at the very end of the matrix.
    # We can find the optimal allocation that gives this
    # value by backtracking.
    best_value: int = dp[-1][-1]
    allocation: List[int] = []
    i: int = len(projects)
    j: int = budget

    # We add item indexes where the maximum value possible changes,
    # because it must be the case that the item was included.
    while i > 0 and j > 0:
        if dp[i][j] != dp[i - 1][j]:
            allocation.append(projects[i - 1])
            j -= costs[i - 1]
        i -= 1
    
    return allocation, best_value
