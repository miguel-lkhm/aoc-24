from unittest import TestCase
from typing import Tuple, List
from data import data
from itertools import product

class DigitMatrix:
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def __init__(self, data: str):
        lines = data.split('\n')
        self.n, self.m = len(lines), len(lines[0])
        self.matrix = [[int(dig) for dig in line] for line in lines]

    def is_within_bounds(self, point: Tuple[int, int]) -> bool:
        if point[0] < 0 or point[0] >= self.n or point[1] < 0 or point[1] >= self.m:
            return False
        return True

    def get_value(self, point: Tuple[int, int]) -> int:
        if self.is_within_bounds(point):
            return self.matrix[point[0]][point[1]]
        else:
            raise IndexError

    def get_neighbours(self, point: Tuple[int, int]) -> List[Tuple[int, int]]:
        return [tuple((point[0]+dir[0], point[1]+dir[1])) for dir in self.directions
            if self.is_within_bounds(tuple((point[0]+dir[0], point[1]+dir[1])))]

    def get_trailheads(self) -> List[Tuple[int, int]]:
        trailheads = []
        for i in range(self.n):
            for j in range(self.m):
                if self.matrix[i][j] == 0:
                    trailheads.append((i, j))
        return trailheads

    def blaze_trails(self, starting_point: Tuple[int, int]) -> List[Tuple[int, int]]:
        peaks_reachable = []
        def climb(point: Tuple[int, int]):
            for n in self.get_neighbours(point):
                if self.get_value(n) == self.get_value(point) + 1:
                    if self.get_value(n) == 9:
                        peaks_reachable.append(n)
                    else:
                        climb(n)
        climb(starting_point)
        # return list(set(peaks_reachable)) # set: to remove repeated tuples
        return peaks_reachable

    def print(self):
        for row in self.matrix:
            print("\t".join([str(n) for n in row]))


class Day10(TestCase):

    def test_day10_part_1(self):
        # map = DigitMatrix(data)
        # map.print()
        # print("*************************")
        # trailheads = map.get_trailheads()
        # total = sum([len(map.blaze_trails(th)) for th in trailheads])
        #
        # print(f"sum of the scores of all trailheads is {total}")
        pass


    def test_day10_part_2(self):
        # the code is the same as before, i just stopped counting as one the trails that lead to the same destination
        map = DigitMatrix(data)
        map.print()
        print("*************************")
        trailheads = map.get_trailheads()
        total = sum([len(map.blaze_trails(th)) for th in trailheads])

        print(f"sum of the scores of all trailheads is {total}")