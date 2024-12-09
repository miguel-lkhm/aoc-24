from unittest import TestCase
from data import data
from itertools import product
from typing import List

class Formula:
    def __init__(self, numbers: List[int], operators: List[str]):
        if len(operators) != len(numbers)-1:
            raise ValueError
        self.numbers = numbers
        self.operators = operators

    def eval(self) -> int:
        result = self.numbers[0]
        for i, op in enumerate(self.operators, start=1):
            if op == "+":
                result += self.numbers[i]
            elif op == "*":
                result *= self.numbers[i]
            elif op == "!":
                result = int(str(result) + str(self.numbers[i]))
            else:
                raise ValueError
        return result


class Equation:
    def __init__(self, result: int, numbers: List[int]):
        self.result = result
        self.numbers = numbers
    def get_possible_operator_combos(self) -> List[str]:
        return list(product(["+", "*", "!"], repeat=len(self.numbers)-1))
    def get_possible_formulas(self) -> List[Formula]:
        return [Formula(numbers=self.numbers, operators=op_list) for op_list in self.get_possible_operator_combos()]
    def is_equation_valid_for_some_op_combo(self) -> bool:
        return any([self.result == formula.eval() for formula in self.get_possible_formulas()])

class Day7(TestCase):

    def test_day7_part1(self):
        lines = data.splitlines()
        equations = [Equation(result=int(line.split(":")[0]), numbers=[int(w) for w in line.split(" ")[1:]]) for line in lines]
        total = sum([eq.result for eq in equations if eq.is_equation_valid_for_some_op_combo()])
        # print(f"total {total}")

    def test_day7_part2(self):
        # same code as before, just added the additional operator
        lines = data.splitlines()
        equations = [Equation(result=int(line.split(":")[0]), numbers=[int(w) for w in line.split(" ")[1:]]) for line in lines]
        total = sum([eq.result for eq in equations if eq.is_equation_valid_for_some_op_combo()])
        print(f"total part2 {total}")

