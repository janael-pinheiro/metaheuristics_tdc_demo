import sys
from dataclasses import dataclass, field
from typing import List, Callable, Set, Tuple
from random import choice, choices, sample, randint
import string

from metaheuristics.utils.score import compute_score


@dataclass
class GeneticString:
    population_size: int
    target: str
    fitness_function: Callable[[str, str], int]
    __cache: Set[str] = field(default_factory=set)

    def evolve(self):
        best = ""
        best_fitness = sys.maxsize
        generation = self.__create_initial_population()

        step = 0
        while best_fitness > 0:
            try:
                fitness = [self.fitness_function(self.target, individual) for individual in generation]
                selected_individuals = self.select(generation, fitness, self.population_size // 10)
                sorted_individuals, sorted_fitness = self.__sort_individuals(generation, fitness)
                if sorted_fitness[-1] < best_fitness:
                    best_fitness = sorted_fitness[-1]
                    best = sorted_individuals[-1]
                generation = []
                for _ in range(int(self.population_size * 0.9)):
                    generation.append(self.create_new_individual(selected_individuals))
                step += 1
            except KeyboardInterrupt:
                print(f"Best: {best}")
        print(f"Steps: {step}")

    def __sort_individuals(self, individuals: List[str], fitness: List[float]) -> Tuple[List[str], List[float]]:
        zipped = sorted(zip(fitness, individuals), reverse=True)
        sorted_individuals = [x for _, x in zipped]
        sorted_fitness = [y for y, _ in zipped]
        return sorted_individuals, sorted_fitness

    def create_new_individual(self, individuals: List[str]) -> str:
        child = self.crossover(individuals)
        mutated_child = self.mutate(child)
        return mutated_child

    def mutate(self, individual: str):
        index: int = randint(0, len(individual) - 1)
        split_solution = [letter for letter in individual]
        split_solution[index] = choice(string.ascii_lowercase)
        neighbor = "".join(split_solution)
        if neighbor in self.__cache:
            self.mutate(neighbor)
        self.__cache.add(neighbor)
        return neighbor

    def crossover(self, individuals: List[str]) -> str:
        parent_one, parent_two = sample(individuals, 2)
        if len(self.target) % 2 == 0:
            number_chromosomes = len(parent_one) // 2 + len(parent_two) // 2
        else:
            number_chromosomes = (len(parent_one) // 2 + len(parent_two) // 2) + 1
        child = sample(parent_one + parent_two, number_chromosomes)
        return "".join(child)

    def select(self, individuals: List[str], fitness: List[float], number_individuals: int) -> List[str]:
        max_fitness = max(fitness)
        probabilities = [(max_fitness - fit) / len(fitness) for fit in fitness]
        return choices(individuals, weights=probabilities, k=number_individuals)

    def __create_initial_population(self) -> List[str]:
        return [self.__create_individual() for _ in range(self.population_size)]

    def __create_individual(self) -> str:
        return "".join([choice(string.ascii_lowercase) for _ in range(len(self.target))])


if __name__ == "__main__":
    genetic = GeneticString(
        population_size=100,
        target="pneumonoultramicroscopicsilicovolcanoconiosi",
        fitness_function=compute_score)
    genetic.evolve()
