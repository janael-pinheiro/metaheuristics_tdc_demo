import string
from dataclasses import dataclass, field
from math import exp
from random import choice, random
from typing import Callable

from metaheuristics.utils.neighbor import Neighbor
from metaheuristics.utils.score import compute_score


@dataclass
class SimulatedAnnealing:
    target: str
    current_solution: str
    maximum_temperature: float
    minimum_temperature: float
    minimum_energy: int
    energy_function: Callable[[str, str], int]
    get_neighbor_function: Callable[[str], str]
    alpha: float = field(default=0.01)

    def __post_init__(self):
        self.__current_energy = self.energy_function(self.target, self.current_solution)
        self.__best_solution = self.current_solution
        self.__best_energy = self.__current_energy
        self.__current_temperature = self.maximum_temperature

    def execute(self) -> str:
        steps = 1
        while self.__should_continue():
            neighbor = self.get_neighbor_function(self.current_solution)
            neighbor_energy = self.energy_function(self.target, neighbor)
            delta_energy = neighbor_energy - self.__current_energy
            if delta_energy < 0:
                self.__update(neighbor, neighbor_energy)
            else:
                if exp(-delta_energy/self.__current_temperature) > random():
                    self.__update(neighbor, neighbor_energy)
            self.__current_temperature /= 1 + self.alpha
            steps += 1
        print(f"Steps: {steps}.")
        return self.__best_solution

    def __update(self, neighbor: str, neighbor_energy: int):
        self.current_solution = neighbor
        self.__current_energy = neighbor_energy
        if neighbor_energy < self.__best_energy:
            self.__update_best(neighbor, neighbor_energy)

    def __update_best(self, neighbor: str, neighbor_energy: int):
        self.__best_solution = neighbor
        self.__best_energy = neighbor_energy

    def __should_continue(self) -> bool:
        return self.__current_temperature > self.minimum_temperature and\
            self.__current_energy > self.minimum_energy


if __name__ == "__main__":
    target = "pneumonoultramicroscopicsilicovolcanoconiosi"
    simulated_annealing = SimulatedAnnealing(
        current_solution="".join([choice(string.ascii_lowercase) for _ in range(len(target))]),
        target=target,
        maximum_temperature=100,
        minimum_temperature=0,
        minimum_energy=0,
        energy_function=compute_score,
        get_neighbor_function=Neighbor().get_neighbor)
    solution = simulated_annealing.execute()
    print(f"Solution: {solution}")
    assert target == solution
