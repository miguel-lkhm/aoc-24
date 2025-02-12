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
        self.cost = self._cost()

    def _cost(self) -> int:
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
        combos = [Combination([(self.button_a, i), (self.button_b, j)]) 
                for i in range(1, 101) for j in range(1, 101)]
        valid_combos = list(filter(lambda c: c.result(self.claw) == self.prize_loc, combos))
        if valid_combos:
            best_combo = sorted(valid_combos, key=lambda combo: combo.cost)[0]
            return best_combo.cost
        else: 
            return 0

class LinEq2by2:
    """
    a1 * x + b1 * y = p1}
    a2 * x + b2 * y = p2}
    """
    def __init__(self, matrix: Tuple[Tuple[int, int], Tuple[int, int]], vector: Tuple[int, int]):
        self.a1 = float(matrix[0][0])
        self.b1 = float(matrix[0][1])
        self.a2 = float(matrix[1][0])
        self.b2 = float(matrix[1][1])

        self.p1 = float(vector[0])
        self.p2 = float(vector[1])
    
    def has_unique_solution(self) -> bool:
        return not (self.a1*self.b2 + self.a2*self.b1) == 0



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
        total_token_cost = sum([machine.best_combination() for machine in machines])
        print(f"total token cost: {total_token_cost}")

    def test_day13_part2(self):
        machines = parse_data(data)
        for m in machines: # offset prize location
            m.prize_loc = (m.prize_loc[0] + 10000000000000, m.prize_loc[1] + 10000000000000)

        

if __name__ == "__main__":
    day13 = Day13()
    day13.test_day13_part1()