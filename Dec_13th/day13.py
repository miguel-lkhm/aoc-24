from platform import machine
from unittest import TestCase
from data import data
from typing import List, Tuple
import re

class Button:
    def __init__(self, move_x: int, move_y: int, type: str):
        self.vect = (move_x, move_y)
        if type.upper() == 'A':
            self.cost = 3
        elif type.upper() == 'B':
            self.cost = 1
        else:
            raise ValueError

class Combination:
    def __init__(self, combo: List[Tuple[Button, int]]):
        self.combo = combo

    def cost(self) -> int:
        return sum([s[0].cost * s[1] for s in self.combo])

    def result(self, start_point: Tuple[int, int]) -> Tuple[int, int] :
        x0, y0 = start_point
        x = sum([s[0].vect[0] * s[1] for s in self.combo])
        y = sum([s[0].vect[1] * s[1] for s in self.combo])
        return tuple((x0 + x, y0 + y))


class Machine:
    def __init__(self, button_a: Button, button_b: Button, prize_loc: Tuple[int, int]):
        self.button_a = button_a
        self.button_b = button_b
        self.prize_loc = prize_loc
        self._reset_claw()

    def _reset_claw(self):
        self.claw = (0, 0)

    def best_combination(self) -> int:  # outputs 0 if impossible
        # make a list with all combinations
        # order them by their cost
        i, j = 0, 0
        combo = Combination([(self.button_a, i), (self.button_b, j)])
        if combo.result(self.claw) == self.prize_loc:
            cost = combo.cost()
        return 0


def parse_data(data: str) -> List[Machine]:
    pattern = r'Button A: X([+-]?\d+), Y([+-]?\d+)\nButton B: X([+-]?\d+), Y([+-]?\d+)\nPrize: X=([+-]?\d+), Y=([+-]?\d+)'
    matches = re.findall(pattern, data)
    list_machines = []
    for match in matches:
        button_a = Button(int(match[0]), int(match[1]), "A")
        button_b = Button(int(match[2]), int(match[3]), "B")
        machine = Machine(button_a, button_b, prize_loc=(int(match[4]), int(match[5])))

        list_machines.append(machine)
    return list_machines


class Day13(TestCase):

    def test_day13_part1(self):
        machines = parse_data(data)

    def test_day13_part2(self):
        pass

