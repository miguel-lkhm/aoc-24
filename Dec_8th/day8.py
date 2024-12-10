from typing import Optional, Tuple, List
from data import data
from unittest import TestCase
from collections import defaultdict
from itertools import combinations
from math import gcd

class CharMatrix:
    antena_types = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789"

    def __init__(self, data: str):
        lines = data.split('\n')
        self.n, self.m = len(lines), len(lines[0])
        self.matrix = [list(line) for line in lines]

    def is_within_bounds(self, position: Tuple[int, int]) -> bool:
        if position[0] < 0 or position[1] < 0 or position[0] >= self.n or position[1] >= self.m:
            return False
        return True

    @classmethod
    def distance(cls, point_a: Tuple[int, int], point_b: Tuple[int, int]) -> Tuple[int, int]: # it goes in direction a -> b
        return tuple([point_b[0]-point_a[0], point_b[1]-point_a[1]])

    @classmethod
    def move(cls, point: Tuple[int, int], vector: Tuple[int, int]) -> Tuple[int, int]:
        return tuple([point[0]+vector[0], point[1]+vector[1]])

    @classmethod
    def scale_vector(cls, vector: Tuple[int, int], n: int) -> Tuple[int, int]:
        return tuple([n*vector[0], n*vector[1]])

    @classmethod
    def reduce_vector(cls, vector: Tuple[int, int]) -> Tuple[int, int]:
        scale = gcd(vector[0], vector[1])
        return tuple((int(vector[0]/scale), int(vector[1]/scale)))
    
    def get_antinodes_for_pair_of_points(self, point_a: Tuple[int, int], point_b: Tuple[int, int]) -> List[Tuple[int, int]]:
        distance_vect = CharMatrix.distance(point_a=point_a, point_b=point_b)
        antinode_1 = CharMatrix.move(point=point_b, vector=distance_vect)
        antinode_2 = CharMatrix.move(point=point_a, vector=CharMatrix.scale_vector(distance_vect, -1))
        antinodes_l = []
        if self.is_within_bounds(antinode_1):
            antinodes_l.append(antinode_1)
        if self.is_within_bounds(antinode_2):
            antinodes_l.append(antinode_2)
        return antinodes_l
    
    def get_antenas_map(self):
        antenas_map = defaultdict(list)
        for i in range(self.n):
            for j in range(self.m):
                if self.matrix[i][j] in self.antena_types:
                    antenas_map[self.matrix[i][j]].append(tuple([i, j]))
        return antenas_map
    
    def get_antinodes(self) -> List[Tuple[int, int]]:
        antinodes = []
        antenas_map = self.get_antenas_map()
        for antena_type, antenas_list in antenas_map.items():
            for antena_A, antena_B in combinations(antenas_list, 2):
                antinodes.extend(self.get_antinodes_for_pair_of_points(antena_A, antena_B))
        return list(set(antinodes))

    def get_points_in_line_with_pair_of_points(self, point_a: Tuple[int, int], point_b: Tuple[int, int]) -> List[Tuple[int, int]]:
        antinodes_l = []
        distance_vect = CharMatrix.distance(point_a=point_a, point_b=point_b)
        v = CharMatrix.reduce_vector(distance_vect)

        i = 0
        while self.is_within_bounds( antinode := CharMatrix.move(point_a, CharMatrix.scale_vector(v, i)) ):
            antinodes_l.append(antinode)
            i += 1

        i = -1
        while self.is_within_bounds( antinode := CharMatrix.move(point_a, CharMatrix.scale_vector(v, i)) ):
            antinodes_l.append(antinode)
            i -= 1

        return antinodes_l
    
    def get_antinodes_part2(self) -> List[Tuple[int, int]]:
        antinodes = []
        antenas_map = self.get_antenas_map()
        for antena_type, antenas_list in antenas_map.items():
            for antena_A, antena_B in combinations(antenas_list, 2):
                antinodes.extend(self.get_points_in_line_with_pair_of_points(antena_A, antena_B))
        return list(set(antinodes))

class Day8(TestCase):

    def test_day8_part1(self):
        M = CharMatrix(data)
        print(f"number of antinodes: {len(M.get_antinodes())}")

    def test_day8_part2(self):
        M = CharMatrix(data)
        print(f"number of antinodes (line definition): {len(M.get_antinodes_part2())}")


if __name__ == "__main__":
    day8 = Day8()
    day8.test_day8_part2()