from dataclasses import dataclass
from collections import deque
from typing import Tuple, List


@dataclass
class AllocationNode:
    level: int
    utility: int
    bound: int
    cost: int
    allocation: List[int]


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
    
    candidates = sorted(
        [(project, utilities[i], costs[i]) for i, project in enumerate(projects)],
        key=lambda t: t[1]/t[2],
        reverse=True
    )

    queue: deque[Tuple[int, int, int]] = deque()
    queue.append(AllocationNode(-1, 0, 0, 0, []))  # Root Node

    max_utility: int = 0
    max_allocation: List[int] = []

    while queue:
        curr: AllocationNode = queue.popleft()
        child: AllocationNode = AllocationNode(0, 0, 0, 0, [])

        if curr.level == -1:
            child.level = 0

        if curr.level == len(projects) - 1:
            continue

        child.level = curr.level + 1
        child.cost = curr.cost + candidates[child.level][2]
        child.utility = curr.utility + candidates[child.level][1]
        child.allocation = curr.allocation[:] + [candidates[child.level][0]]

        if child.cost <= budget and child.utility > max_utility:
            max_utility = child.utility
            max_allocation = child.allocation

        child.bound = __bound(child, budget, candidates)

        if child.bound > max_utility:
            queue.append(child)
        
        child = AllocationNode(0, 0, 0, 0, [])
        child.level = curr.level + 1
        child.cost = curr.cost
        child.utility = curr.utility
        child.allocation = curr.allocation[:]
        child.bound = __bound(child, budget, candidates)

        if child.bound > max_utility:
            queue.append(child)
    
    return max_allocation, max_utility
