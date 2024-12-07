from typing import Optional, Tuple
from data import data
from unittest import TestCase

class CharMatrix:
    def __init__(self, data: str):
        lines = data.split('\n')
        self.n, self.m = len(lines), len(lines[0])
        self.matrix = [list(line) for line in lines]

    def get_value(self, point: Tuple[int, int]) -> str:
        if point[0] < 0 or point[0] >= self.n or point[1] < 0 or point[1] >= self.m:
            return "$"
        return self.matrix[point[0]][point[1]]

    def set_value(self, point: Tuple[int, int], value: str):
        if point[0] < 0 or point[0] >= self.n or point[1] < 0 or point[1] >= self.m:
            raise IndexError
        self.matrix[point[0]][point[1]] = value

    def move_from(self, point: Tuple[int, int], dir: Tuple[int, int]) -> Tuple[int, int]:
        if not (dir[0] in [-1, 0, 1] and dir[1] in [-1, 0, 1]):
            raise ValueError("Invalid direction")
        return [point[0] + dir[0], point[1] + dir[1]]

    def find_first_value(self, val: str) -> Optional[Tuple[int, int]]:
        for i in range(self.n):
            for j in range(self.m):
                if self.get_value((i, j)) == val:
                    return (i, j)
        return None

class Day6(TestCase):

    def test_day6_part1(self):
        M = CharMatrix(data)
        start = M.find_first_value("^")
        assert start is not None

        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)] # up, right, down, left
        idx_dir = 0
        count = 0
        current_pos = start
        while M.get_value(current_pos) != "$":
            if M.get_value(current_pos) != "X": # count & mark
                count += 1
                M.set_value(current_pos, "X")

            if M.get_value(M.move_from(current_pos, directions[idx_dir])) == "#":
                idx_dir = (idx_dir + 1) % 4 # change direction to relative right

            current_pos = M.move_from(current_pos, directions[idx_dir])

        print(f"number of visited positions = {count}")
    
    def test_day6_part2(self):
        pass