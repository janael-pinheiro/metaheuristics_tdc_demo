import string
from collections import deque
from dataclasses import dataclass
from random import choice
from typing import Callable, List, Deque

from metaheuristics.utils.neighbor import Neighbor
from metaheuristics.utils.score import compute_score


@dataclass
class TabuSearch:
    target: str
    current_solution: str
    cost_function: Callable[[str, str], int]
    get_neighbor_function: Callable[[str], str]
    tabu_list_max_size: int
    max_iterations: int
    number_neighbors: int

    def execute(self):
        tabu_list: Deque[str] = deque(maxlen=self.tabu_list_max_size)
        current_cost: int = self.cost_function(self.target, self.current_solution)

        best_solution: str = self.current_solution
        best_cost = current_cost

        for _ in range(self.max_iterations):
            neighbors: List[str] = [self.get_neighbor_function(
                self.current_solution) for _ in range(self.number_neighbors)]

            found_next_solution = False
            for neighbor in neighbors:
                if neighbor in tabu_list:
                    continue
                self.current_solution = neighbor
                current_cost = self.cost_function(self.target, neighbor)
                if current_cost < best_cost:
                    best_solution = self.current_solution
                    best_cost = current_cost
                tabu_list.append(neighbor)
                found_next_solution = True

            if not found_next_solution:
                break
        return best_solution


if __name__ == "__main__":
    target = "pneumonoultramicroscopicsilicovolcanoconiosi"
    tabu_search = TabuSearch(
        current_solution="".join([choice(string.ascii_lowercase) for _ in range(len(target))]),
        target=target,
        cost_function=compute_score,
        get_neighbor_function=Neighbor().get_neighbor,
        tabu_list_max_size=300,
        max_iterations=10000,
        number_neighbors=500
        )
    best_solution = tabu_search.execute()
    print(f"Best solution: {best_solution.capitalize()}")
