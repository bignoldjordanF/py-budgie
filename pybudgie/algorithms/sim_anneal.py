from typing import List, Tuple
from dataclasses import dataclass
import numpy as np
import random


# Ignore Exp Overflow
np.seterr(over='ignore')


@dataclass
class SAAllocation:
    # Instance Data
    budget: int
    costs: List[int]
    utilities: List[int]

    # Allocation Data
    allocation: List[int]  # e.g. [1, 0, 0, 1, 0]
    utility: int
    cost: int

    def neighbor(self) -> 'SAAllocation':
        """
        Generates a neighbour by randomly flipping a single bit and
        adding or subtracting the corresponding cost and utility
        from the allocation totals. Allocations exceeding the
        instance budget are given a negative utility, such that
        the default allocation (all zeroes) is better.

        Example:
        self:      [1, 0, 0, 1, 0]
        neighbour: [1, 0, 0, 1, 1]
                                ^

        Returns:
            - SAAllocation: A neighbouring allocation object.
        """

        # Create a deep copy of the allocation:
        _allocation = self.allocation[:]
        _utility = self.utility
        _cost = self.cost

        # Generate randomly an index in the allocation and flip
        # the bit, i.e., include/exclude the item at that index:
        ridx: int = random.randint(0, len(_allocation) - 1)
        _allocation[ridx] = int(not _allocation[ridx])

        # Update the utility and cost by setting false bits to
        # -1 such that it subtracts if the item was excluded:
        pos_neg = 1 if _allocation[ridx] else -1
        _utility = abs(_utility) + (pos_neg * self.utilities[ridx])
        _cost += pos_neg * self.costs[ridx]

        # We negatively value allocations whose costs exceed
        # the budget. We still preserve its value, and use
        # abs(_cost) above to update it where one of its
        # neighbours may reduce the total weight below the
        # knapsack capacity:
        if _cost > self.budget:
            _utility = -_utility
        
        return SAAllocation(
            budget=self.budget,
            costs=self.costs,
            utilities=self.utilities,
            allocation=_allocation,
            utility=_utility,
            cost=_cost
        )


def simulated_annealing_solver(
        budget: int,
        projects: List[int], 
        costs: List[int],
        utilities: List[int],
        initial_temperature: float = 10.0,
        temperature_length: int = 1,
        cooling_ratio: float = 0.999,
        num_non_improve: int = 100_000
) -> Tuple[List[int], int]:
    """
    A relatively fast approximation scheme for participatory budgeting
    problems formulated as the binary knapsack problem. We pose each
    solution to the problem as an allocation, and generate neighbours
    by including or excluding a single project. The simulated 
    annealing algorithm works as follows:

    We generate a neighbouring solution from the current solution
    and compare their utilities. A better utility means the neighbour
    becomes current. Otherwise, it becomes current with some decreasing
    probability, i.e. less worse solutions accepted as process continues.
    Accepting worse solutions allows us to escape local optima. We
    record the best solution found throughout annealing and return it
    at the end.

    Parameters:
        - budget (int): The total budget of the instance.
        - projects (List[int]): A list of projects included in the instance.
        - costs (List[int]): A list of costs for each project in the instance.
        - utilities (List[int]): A list of utilities for each project in the instance.
        - initial_temperature (float): An optional initial temperature parameter for simulated annealing.
        - temperature_length (int): An optional temperature length parameter for simulated annealing.
        - cooling_ratio (float): An optional cooling ratio parameter for simulated annealing.
        - num_non_improve (int): An optional num-non-improve parameter for simulated annealing.

    Returns:
        - Tuple[List[int], int]: A pair containing the allocation found, as a list of project
        ids, and the overall value with regard to the welfare function.
    """

    current_temperature: float = initial_temperature
    count_num_non_improve: int = 0

    # The initial allocation is the empty allocation,
    # with no utility and no cost.
    current_allocation: SAAllocation = SAAllocation(
        budget=budget,
        costs=costs,
        utilities=utilities,
        allocation=[0] * len(costs),
        utility=0,
        cost=0
    )
    best_allocation: SAAllocation = current_allocation

    # As long as we have improved within the deadline:
    while count_num_non_improve < num_non_improve:
        for _ in range(temperature_length):
            # Generate a neighbour and compare utilities:
            neighbor_allocation: SAAllocation = current_allocation.neighbor()
            delta_utility: int = neighbor_allocation.utility - current_allocation.utility

            # A better allocation instantly becomes current:
            if delta_utility >= 0:
                current_allocation = neighbor_allocation
                count_num_non_improve += 1
                # Update best_allocation if it is the best:
                if current_allocation.utility > best_allocation.utility:
                    best_allocation = current_allocation
                    # We have improved, so reset the count:
                    count_num_non_improve = 0

            # Otherwise, accept worse allocation with probability p:
            else:
                q = random.random()
                p = np.exp(-delta_utility / current_temperature)
                if q < p:
                    current_allocation = neighbor_allocation
                count_num_non_improve += 1
        
        # After temperature_length iterations, update the temperature:
        current_temperature *= cooling_ratio
    
    # Record the project ids of those projects in the best allocation:
    result = [projects[idx] for idx, val in enumerate(best_allocation.allocation) if val]
    return result, best_allocation.utility
