from unittest import TestCase
from typing import List, Tuple
from data import data

class CharMatrix:
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    directions = [UP, DOWN, LEFT, RIGHT]

    def __init__(self, data: str):
        lines = data.split('\n')
        self.n, self.m = len(lines), len(lines[0])
        self.matrix = [list(line) for line in lines]

    def value_at(self, point: Tuple[int, int]) -> str:
        if point[0] < 0 or point[0] >= self.n or point[1] < 0 or point[1] >= self.m:
            return "$"
        return self.matrix[point[0]][point[1]]

    def move(self, point: Tuple[int, int], dir: Tuple[int, int]) -> Tuple[int, int]:
        return tuple((point[0] + dir[0], point[1] + dir[1]))

    def get_neighbours(self, point: Tuple[int, int]) -> List[Tuple[int, int]]:
        return [tuple((point[0]+dir[0], point[1]+dir[1])) for dir in self.directions]

class Garden(CharMatrix):
    def __init__(self, data: str):
        super().__init__(data)
        self.regions = self._search_regions()

    def _search_regions(self) -> List["Region"]:
        visited_points = set()
        regions = []
        for i in range(self.n):
            for j in range(self.m):
                if (i, j) not in visited_points:
                    new_region = self._traverse_region((i, j))
                    regions.append(new_region)
                    visited_points.update([plot.point for plot in new_region.plots])
        return regions

    def _traverse_region(self, point: Tuple[int, int]) -> "Region":
        plots_positions = [point]  # List to hold visited positions
        stack = [point]  # Stack to hold points to be visited

        while stack:  # While there are points to visit
            p = stack.pop()  # Pop the next point from the stack
            for n in self.get_neighbours(p):  # Visit neighbors
                if self.value_at(n) == self.value_at(point) and n not in plots_positions:
                    plots_positions.append(n)  # Add neighbor to visited positions
                    stack.append(n)  # Push neighbor to the stack to visit later

        return Region([Plot(pos, self) for pos in plots_positions])

    def total_fence_price(self) -> int:
        return sum([reg.fence_price() for reg in self.regions])

class Plot:
    def __init__(self, point : Tuple[int, int], garden: Garden):
        self.point = point
        self.garden = garden
        self.value = garden.value_at(self.point)
        self.number_akin_neighbors = sum([1 if self.value == garden.value_at(garden.move(self.point, dir)) else 0
                                          for dir in garden.directions])

class Region:
    def __init__(self, plots: List[Plot]):
        self.plots = plots

    def area(self) -> int:
        return len(self.plots)

    def perimeter(self) -> int:
        return sum([4 - plot.number_akin_neighbors for plot in self.plots])

    def fence_price(self) -> int:
        return self.area() * self.perimeter()


class Day12(TestCase):

    def test_day12_part1(self):
        garden = Garden(data)
        print(f"Total price of fence {garden.total_fence_price()}")

    def test_day12_part2(self):
        pass