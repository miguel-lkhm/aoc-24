from typing import List
from unittest import TestCase
from data import data

class CharMatrix:
    def __init__(self, data: str):
        lines = data.split('\n')
        self.n, self.m = len(lines), len(lines[0])
        self.matrix = [list(line) for line in lines]

    def get_value(self, point: List[int]) -> str:
        if point[0] < 0 or point[0] >= self.n or point[1] < 0 or point[1] >= self.m:
            return "$"
        return self.matrix[point[0]][point[1]]

    def move_from(self, point: List[int], dir: List[int]) -> List[int]:
        if not (dir[0] in [-1, 0, 1] and dir[1] in [-1, 0, 1]):
            raise ValueError("Invalid direction")
        return [point[0] + dir[0], point[1] + dir[1]]

    def check_string_from_point_in_dir(self, point : List[int], dir : List[int], string_ref: str) -> bool:
        for char in string_ref:
            if self.get_value(point) != char:
                return False
            point = self.move_from(point, dir)
        return True

    def count_matches_string_from_point(self, point : List[int], string_ref: str) -> int:
        num = 0
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if self.check_string_from_point_in_dir(point, [x,y], string_ref):
                    num += 1
        return num

class Day4(TestCase):

    def test_day4_part1(self):
        M = CharMatrix(data)
        total = 0
        for i in range(M.n):
            for j in range(M.m):
                total += M.count_matches_string_from_point([i, j], "XMAS")

        print(total)

    def test_day4_part2(self):
        pass
