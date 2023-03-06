from dataclasses import dataclass
from collections import deque
from typing import Tuple, List


@dataclass
class AllocationNode:
    level: int
    """The level of the node in the decision tree (i.e. the item index)."""

    utility: int
    """The total utility on this path in the decision tree."""

    bound: int
    """The upper bound of maximum profit in the subtree of this node."""

    cost: int
    """The total cost on this path of the decision tree."""

    allocation: List[int]
    """The allocation found by this path in the decision tree."""


def __bound(node: AllocationNode, budget: int, candidates: List[Tuple[int, int, int]]) -> float:
    if node.cost >= budget:
        return 0
    
    utility_bound: int = node.utility
    level: int = node.level + 1
    cost: int = node.cost

    while level < len(candidates) and candidates[level][2] <= budget:
        cost += candidates[level][2]
        utility_bound += candidates[level][1]
        level += 1
    
    if level < len(candidates):
        utility_bound += (budget - cost) * \
            candidates[level][1] / candidates[level][2]
    
    return utility_bound


def branch_and_bound_solver(
        budget: int,
        projects: List[int], 
        costs: List[int],
        utilities: List[int]
) -> Tuple[List[int], int]:
    """
    An exact algorithm for participatory budgeting problems formulated as the
    binary knapsack problem.

    The branch-and-bound algorithm essentially traverses a decision tree, where
    from any node we generate two additional nodes, one including the current
    item and one excluding it. We only generate and hence expand promising
    nodes, i.e., nodes for which expanding its children may lead to higher
    utility values. We stop expanding when we have no more nodes to expand
    or we have generated nodes for every item.

    Parameters:
        - budget (int): The total budget of the instance.
        - projects (List[int]): A list of project identifiers.
        - costs (List[int]): A list of project costs.
        - utilities (List[int]): A list of project utilities.

    Returns:
        - Tuple[List[int], int]: A pair containing the allocation found, as a list of project
        ids, and the overall value with regard to the welfare function.
    """

    # The candidates are sorted by their utility-cost ratio for the bound
    # algorithm, which uses a greedy approach:
    candidates = sorted(
        [(project, utilities[i], costs[i]) for i, project in enumerate(projects)],
        key=lambda t: t[1]/t[2],
        reverse=True
    )

    # Make a queue to store generated nodes:
    queue: deque[Tuple[int, int, int]] = deque()
    queue.append(AllocationNode(-1, 0, 0, 0, []))  # Root Node

    max_utility: int = 0
    max_allocation: List[int] = []

    # Each allocation node has a level attribute, which considers
    # all projects in the project subset {1, ..., level}.
    while queue:
        curr: AllocationNode = queue.popleft()
        child: AllocationNode = AllocationNode(0, 0, 0, 0, [])

        # If curr is the root node, then the child is
        # at level zero:
        if curr.level == -1:
            child.level = 0

        # If the current level (project subset) considers
        # all items, then nothing more is to be done:
        if curr.level == len(projects) - 1:
            continue

        # Our first possible child considers the solution
        # with the current project (level) included:
        child.level = curr.level + 1
        child.cost = curr.cost + candidates[child.level][2]
        child.utility = curr.utility + candidates[child.level][1]
        child.allocation = curr.allocation[:] + [candidates[child.level][0]]

        # Update max_utility and max_allocation if including this
        # item yields the best allocation and utility so far:
        if child.cost <= budget and child.utility > max_utility:
            max_utility = child.utility
            max_allocation = child.allocation

        # The upper bound gives the optimal solution for this
        # child node if we can partially include the remaining
        # items {level + 1, ..., n}.
        child.bound = __bound(child, budget, candidates)

        # If the child bound is larger than max_utility,
        # then there is potential, so add it to the queue.
        if child.bound > max_utility:
            queue.append(child)
        
        # We repeat the process for a child node that does
        # not include the current item (level). We hence do
        # not try to update max_value or max_allocation: 
        child = AllocationNode(0, 0, 0, 0, [])
        child.level = curr.level + 1
        child.cost = curr.cost
        child.utility = curr.utility
        child.allocation = curr.allocation[:]
        child.bound = __bound(child, budget, candidates)

        if child.bound > max_utility:
            queue.append(child)
    
    return max_allocation, max_utility
