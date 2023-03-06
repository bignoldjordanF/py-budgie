from typing import List, Tuple
import random


def __create_population(n_projects: int, population_size: int) -> List[List[int]]:
    """
    Creates an initial population of population_size chromosomes
    in the form e.g. [0, 1, 0, 1, 1], where each index is a
    binary gene representing one item. A one gene means that the
    corresponding item is in the allocation.

    Parameters:
        - n_projects (int): The number of projects, i.e., the length
        of the chromosomes.
        - population_size (int): The number of chromosomes in the
        population.

    Returns:
        - List[List[int]]: A list of n_projects-length population_size chromosomes.
    """

    population: List[List[int]] = []
    for _ in range(population_size):
        # The initial chromosomes are randomly generated for each item
        # in the instance:
        chromosome: List[int] = [random.randint(0, 1) for _ in range(n_projects)]
        population.append(chromosome)
    return population


def __fitness(
        budget: int,
        costs: List[int],
        utilities: List[int],
        chromosome: List[int]
) -> int:
    """
    Calculates the fitness of chromosomes by summing the
    utilities of all the projects included in the allocation.
    Those chromosomes that exceed the budget have a negative
    fitness.
    
    Parameters:
        - budget (int): The budget of the instance.
        - costs (List[int]): The costs of the projects in the instance.
        - utilities (List[int]): The utilities of the projects in the instance.
        - chromosome (List[int]): The chromosome to calculate the fitness for.

    Returns:
        - int: The fitness (i.e. utility) value of the chromosome.
    """

    total_cost: int = 0
    total_utility: int = 0

    for i in range(len(chromosome)):
        if chromosome[i]:
            total_cost += costs[i]
            total_utility += utilities[i]

    # We want to heavily discourage invalid chromosomes
    # because they are not fit for survival.
    if total_cost > budget:
        return -total_utility

    return total_utility



def __selection(
        budget: int,
        costs: List[int],
        utilities: List[int],
        population: List[List[int]]
) -> Tuple[List[int], List[int]]:
    """
    Selects two chromosomes based on fitness.

    Parameters:
        - budget (int): The budget of the instance.
        - costs (List[int]): The costs of the projects in the instance.
        - utilities (List[int]): The utilities of the projects in the instance.
        - population (List[List[int]]): A list of chromosomes.

    Returns:
        - Tuple[List[int], List[int]]: Two chromosomes from fitness-based tournament selection.
    """

    tournament_size: int = 2
    selected_parents: List[List[int]] = []
    for _ in range(2):
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
    """
    Performs a crossover between two chromosomes with probability crossover_rate by
    randomly selecting a crossover point and swapping the genes between the two
    chromosomes after that point.

    Parameters:
        - crossover_rate (float): The probability of a crossover occuring between two chromosomes.
        - parent_a (List[int]): The first parent chromosome.
        - parent_b (List[int]): The second parent chromosome.
    
    Returns:
        - Tuple[List[int], List[int]]: The chromosomes after crossover.
    """

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
    """
    Mutates a single gene of a chromosome with probability mutation_rate by
    randomly selecting a mutation point and flipping the bit (gene) at
    that point.

    Parameters:
        - mutation_rate (float): The probability of a mutation occurring.
        - chromosome (List[int]): The chromosome to mutate.
    
    Returns:
        - List[int]: The potentially mutated chromosome.
    """

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
    """
    A relatively fast approximation scheme for participatory budgeting
    problems formulated as the binary knapsack problem.

    Parameters:
        - budget (int): The total budget of the instance.
        - projects (List[int]): A list of projects included in the instance.
        - costs (List[int]): A list of costs for each project in the instance.
        - utilities (List[int]): A list of utilities for each project in the instance.
        - population_size (int): The size (number of chromosomes) of the population.
        - mutation_rate (float): The probability of a chromosome being mutated.
        - crossover_rate (float): The probability of two chromosome crossing over.
        - num_generations (int): The number of generations before returning the
        best chromosome found.

    Returns:
        - Tuple[List[int], int]: A pair containing the allocation found, as a list of project
        ids, and the overall value with regard to the welfare function.
    """
    
    # Initial Population
    population: List[int] = __create_population(len(projects), population_size)

    # Generate offspring num_generations times
    for _ in range(num_generations):
        offspring: List[List[int]] = []

        # The offspring population must be of population_size,
        # otherwise we continue generating:
        while len(offspring) < len(population):
            
            # Use tournament selection to choose two
            # chromosomes based on fitness values:
            parent_a, parent_b = __selection(
                budget=budget,
                costs=costs,
                utilities=utilities,
                population=population
            )

            # Create two new chromosomes by crossing-over
            # the parent chromosomes:
            child_a, child_b = __crossover(
                crossover_rate=crossover_rate,
                parent_a=parent_a,
                parent_b=parent_b
            )

            # Mutate the child chromosomes with probability
            # mutation_rate:
            child_a = __mutation(mutation_rate, child_a)
            child_b = __mutation(mutation_rate, child_b)

            # Add the child chromosomes to the offspring:
            offspring.append(child_a)
            offspring.append(child_b)
        
        # Set the offspring population as the new population:
        population = offspring

    # Compute the best chromosome found and its fitness value:
    best_chromosome: List[int] = max(population, key=lambda chromosome: __fitness(budget, costs, utilities, chromosome))
    best_fitness: int = __fitness(budget, costs, utilities, best_chromosome)

    # Convert from the binary allocation to project ids:
    allocation: List[int] = [projects[idx] for idx, gene in enumerate(best_chromosome) if gene]
    return allocation, best_fitness
