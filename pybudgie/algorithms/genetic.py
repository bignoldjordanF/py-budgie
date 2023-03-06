from typing import List, Tuple
import random


def __create_population(n_projects: int, population_size: int) -> List[List[int]]:
    population: List[List[int]] = []
    for _ in range(population_size):
        chromosome: List[int] = [random.randint(0, 1) for _ in range(n_projects)]
        population.append(chromosome)
    return population


def __fitness(
        budget: int,
        costs: List[int],
        utilities: List[int],
        chromosome: List[int]
) -> int:
    
    total_cost: int = 0
    total_utility: int = 0

    for i in range(len(chromosome)):
        if chromosome[i]:
            total_cost += costs[i]
            total_utility += utilities[i]

    if total_cost > budget:
        return -total_utility

    return total_utility



def __selection(
        budget: int,
        costs: List[int],
        utilities: List[int],
        population: List[List[int]]
) -> Tuple[List[int], List[int]]:
    tournament_size: int = 2
    selected_parents: List[List[int]] = []
    for _ in range(tournament_size):
        tournament: List[List[int]] = random.sample(population, tournament_size)
        best_chromosome: List[int] = max(
            tournament,
            key=lambda chromosome: __fitness(budget, costs, utilities, chromosome)
        )
        selected_parents.append(best_chromosome)
    return tuple(selected_parents)


def __crossover(
        crossover_rate: float,
        parent_a: List[int],
        parent_b: List[int]
) -> Tuple[List[int], List[int]]:
    if random.random() > crossover_rate:
        return parent_a, parent_b
    
    crossover_point: int = random.randint(1, len(parent_a) - 1)
    child_a: list = parent_a[:crossover_point] + parent_b[crossover_point:]
    child_b: list = parent_b[:crossover_point] + parent_a[crossover_point:]

    return child_a, child_b


def __mutation(
        mutation_rate: float,
        chromosome: List[int]
) -> List[int]:
    if random.random() > mutation_rate:
        return chromosome
    
    mutation_point: int = random.randint(0, len(chromosome) - 1)
    chromosome[mutation_point] = 1 - chromosome[mutation_point]
    return chromosome


def genetic_algorithm_solver(
        budget: int,
        projects: List[int], 
        costs: List[int],
        utilities: List[int],
        population_size: int = 100,
        mutation_rate: float = 0.3,
        crossover_rate: float = 0.8,
        num_generations: int = 250
) -> Tuple[List[int], int]:
    
    # Initial Population
    population: List[int] = __create_population(len(projects), population_size)

    # Generate offspring num_generations times
    for _ in range(num_generations):
        offspring: List[List[int]] = []
        best_chromosome: List[int] = []

        # The offspring population must be of population_size
        while len(offspring) < len(population):
            
            parent_a, parent_b = __selection(
                budget=budget,
                costs=costs,
                utilities=utilities,
                population=population
            )

            child_a, child_b = __crossover(
                crossover_rate=crossover_rate,
                parent_a=parent_a,
                parent_b=parent_b
            )

            child_a = __mutation(mutation_rate, child_a)
            child_b = __mutation(mutation_rate, child_b)

            offspring.append(child_a)
            offspring.append(child_b)
        
        population = offspring

    best_chromosome: List[int] = max(population, key=lambda chromosome: __fitness(budget, costs, utilities, chromosome))
    best_fitness: int = __fitness(budget, costs, utilities, best_chromosome)

    allocation: List[int] = [projects[idx] for idx, gene in enumerate(best_chromosome) if gene]
    return allocation, best_fitness
