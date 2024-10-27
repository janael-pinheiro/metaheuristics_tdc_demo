import string
from dataclasses import dataclass, field
from random import randint, choice
from typing import Set


@dataclass
class Neighbor:
    __lower_case_letters: str = field(default=string.ascii_lowercase)
    __cache: Set[str] = field(default_factory=set)

    def get_neighbor(self, current_solution: str) -> str:
        index: int = randint(0, len(current_solution)-1)
        split_solution = [letter for letter in current_solution]
        split_solution[index] = choice(self.__lower_case_letters)
        neighbor = "".join(split_solution)
        if neighbor in self.__cache:
            self.get_neighbor(neighbor)
        self.__cache.add(neighbor)
        return neighbor
