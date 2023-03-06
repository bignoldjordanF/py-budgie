from typing import List, Tuple
from dataclasses import dataclass
import numpy as np
import random


# Ignore Exp Overflow
np.seterr(over='ignore')


@dataclass
class SAAllocation:
    budget: int
    costs: List[int]
    utilities: List[int]
    allocation: List[int]
    utility: int
    cost: int

    def neighbor(self):
        _allocation = self.allocation[:]
        _utility = self.utility
        _cost = self.cost

        ridx: int = random.randint(0, len(_allocation) - 1)
        _allocation[ridx] = int(not _allocation[ridx])

        pos_neg = 1 if _allocation[ridx] else -1
        _utility = abs(_utility) + (pos_neg * self.utilities[ridx])
        _cost += pos_neg * self.costs[ridx]

        if _cost > self.budget:
            _cost = -_cost
        
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
    
    current_temperature: float = initial_temperature
    count_num_non_improve: int = 0

    current_allocation: SAAllocation = SAAllocation(
        budget=budget,
        costs=costs,
        utilities=utilities,
        allocation=[0] * len(costs),
        utility=0,
        cost=0
    )
    best_allocation: SAAllocation = current_allocation

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
        
        # After TL iterations, update the temperature:
        current_temperature *= cooling_ratio
    
    result = [projects[idx] for idx, val in enumerate(best_allocation.allocation) if val]
    return result, best_allocation.utility
