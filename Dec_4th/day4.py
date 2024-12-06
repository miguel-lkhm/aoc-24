from typing import List, Tuple
from unittest import TestCase
from data import data
import itertools

class CharMatrix:
    def __init__(self, data: str):
        lines = data.split('\n')
        self.n, self.m = len(lines), len(lines[0])
        self.matrix = [list(line) for line in lines]

    def get_value(self, point: Tuple[int, int]) -> str:
        if point[0] < 0 or point[0] >= self.n or point[1] < 0 or point[1] >= self.m:
            return "$"
        return self.matrix[point[0]][point[1]]

    def move_from(self, point: Tuple[int, int], dir: Tuple[int, int]) -> Tuple[int, int]:
        if not (dir[0] in [-1, 0, 1] and dir[1] in [-1, 0, 1]):
            raise ValueError("Invalid direction")
        return [point[0] + dir[0], point[1] + dir[1]]

    def check_string_from_point_in_dir(self, point : Tuple[int, int], dir : Tuple[int, int], string_ref: str) -> bool:
        for char in string_ref:
            if self.get_value(point) != char:
                return False
            point = self.move_from(point, dir)
        return True

    def count_matches_string_from_point(self, point : Tuple[int, int], string_ref: str) -> int:
        directions = itertools.product([-1, 0, 1], repeat=2)
        return sum([1 if self.check_string_from_point_in_dir(point, (dir[0], dir[1]), string_ref) else 0 for dir in directions])

    def get_corners_for_point(self, point: Tuple[int, int]) -> List[str]:
        dirs = [(-1, -1), (1, -1), (1, 1), (-1, 1)] # NW, SW, SE, NE directions
        return [self.get_value(self.move_from(point, dir)) for dir in dirs]

    def check_X_shaped_MAS(self, point: Tuple[int, int]) -> bool:
        if self.get_value(point) != "A":
            return False
        corners = self.get_corners_for_point(point)
        indices_M, indices_S = [i for i, val in enumerate(corners) if val == "M"], [i for i, val in enumerate(corners) if val == "S"]
        # check there are 2 M's & 2 S's
        if len(indices_M) != 2 or len(indices_S) != 2:
            return False
        # check the M's are consecutive (same row or column) -> sum of the 2 indices is odd
        if sum(indices_M) % 2 == 0:
            return False
        return True

class Day4(TestCase):

    def test_day4_part1(self):
        M = CharMatrix(data)
        total = 0
        for i in range(M.n):
            for j in range(M.m):
                total += M.count_matches_string_from_point((i, j), "XMAS")

        print(f"number of appearances of XMAS {total}")

    def test_day4_part2(self):
        M = CharMatrix(data)
        total = 0
        for i in range(1, M.n-1):
            for j in range(1, M.m-1):
                total += 1 if M.check_X_shaped_MAS((i, j)) else 0
        
        print(f"number of X-shaped MAS: {total}")
