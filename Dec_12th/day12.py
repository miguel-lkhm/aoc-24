from unittest import TestCase
from typing import List, Tuple, Dict, Set
from data import data
from collections import defaultdict

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

        return Region([Plot(pos, self) for pos in plots_positions], self)

    def total_fence_price(self) -> int:
        return sum([reg.fence_price() for reg in self.regions])

    def total_fence_price_part2(self) -> int:
        return sum([reg.fence_price_part2() for reg in self.regions])

    def traverse_region_borders(self, region: "Region") -> int:
        # border_plots = [plot for region.plots if plot.number_akin_neighbors==4] #doesnt work rn, id have to check all 8 neighbors
        corners = 0
        points_traversed_in_dirs = defaultdict(set)
        # take one of the uppermost plots and move right to trace the external border
        first_plot = sorted(region.plots, key=lambda plot: plot.point[0])[0]
        ext_border_points, ext_border_corners, is_turn_clockwise = self._orbit_border(first_plot.point, start_dir_idx=0)
        
        assert is_turn_clockwise
        interesting_points = set([plot.point for plot in region.plots if not plot.is_plot_below_same_type])
        interesting_points = interesting_points - ext_border_points[2]

        int_border_corners = 0
        while interesting_points:
            random_int_border_point = interesting_points.pop()
            int_border_points, int_border_corners_i, is_turn_clockwise = self._orbit_border(random_int_border_point, start_dir_idx=2)
            assert not is_turn_clockwise
            int_border_corners += int_border_corners_i
            interesting_points = interesting_points - int_border_points[2]

            ## TODO look for points with a non-matching plot below that have not already been traversed in the left direction

        corners = ext_border_corners + int_border_corners
        return corners

    def _orbit_border(self, start_point: Tuple[int, int], start_dir_idx = 0) -> Tuple[Dict[int, Set[Tuple[int, int]]], int, bool]:
        assert start_dir_idx in [0, 1, 2, 3], "Unexpected direction index"
        points_visited_in_directions = defaultdict(set)
        clockwise_dir_cycle = [self.RIGHT, self.DOWN, self.LEFT, self.UP]
        ref_val = self.value_at(start_point)
        current_point = start_point
        corners = 0
        mov_dir_idx = start_dir_idx
        loop = False
        # turn direction counter: pos
        turn_dir_count = [0, 0]
        while not loop:
            direct = mov_dir_idx
            mov_dir_idx = (mov_dir_idx - 1) % 4 # starts by trying to move to relative left
            isolated_point_counter = 0 # if it cant move in any direction, the region is 1 isolated point
            # worst case, it returns to where it came from
            while self.value_at(self.move(current_point, clockwise_dir_cycle[mov_dir_idx])) != ref_val and isolated_point_counter < 4:
                mov_dir_idx = (mov_dir_idx + 1) % 4
                isolated_point_counter += 1
            # here, maybe, mark down the direction of travel in this position
            if isolated_point_counter >= 4:
                loop = True
                corners += 4
                turn_dir_count = [1, 1] # artificial, just so the turn is correctly identified as going clockwise
            elif mov_dir_idx in points_visited_in_directions[current_point]:
                loop = True
            else:
                turn_dir_count = self._turn_direction_counter(turn_dir_count, mov_dir_idx, current_point)
                corners += self._number_of_corners_from_angle((mov_dir_idx - direct) % 4) # count corners
                points_visited_in_directions[current_point].add(mov_dir_idx) # mark as visited
                current_point = self.move(current_point, clockwise_dir_cycle[mov_dir_idx]) # move

        is_turn_clockwise = any([count > 0 for count in turn_dir_count])
        visited_points_with_dirs = {dr: set([pnt for pnt, dirs in points_visited_in_directions.items() if dr in dirs]) for dr in range(4)}
        return tuple((visited_points_with_dirs, corners, is_turn_clockwise))
        

    def _turn_direction_counter(self, turn_dir_count: List[int], movement_direction: int, current_point: Tuple[int, int]) -> List[int]:
        if movement_direction == 0: # right direction motion -> negative
            turn_dir_count[0] -= current_point[0]
        elif movement_direction == 2: # left direction motion -> positive
            turn_dir_count[0] += current_point[0]
        elif movement_direction == 1: # down direction motion -> positive
            turn_dir_count[1] += current_point[1]
        elif movement_direction == 3: # up direction motion -> negative
            turn_dir_count[1] -= current_point[1]
        else:
            raise ValueError("Expected a number between 0 and 3")
        return turn_dir_count


    def _number_of_corners_from_angle(self, number_of_quarter_turns: int):
        if number_of_quarter_turns == 0:
            return 0
        elif number_of_quarter_turns in [1, 3]:
            return 1
        elif number_of_quarter_turns == 2:
            return 2
        else:
            raise ValueError("Expected a number between 0 and 3")


class Plot:
    def __init__(self, point : Tuple[int, int], garden: Garden):
        self.point = point
        self.garden = garden
        self.value = garden.value_at(self.point)
        self.number_akin_neighbors = sum([1 if self.value == garden.value_at(garden.move(self.point, dir)) else 0
                                          for dir in garden.directions])

    def is_plot_below_same_type(self) -> bool:
        return self.value == self.garden.value_at(self.garden.move(self.point, self.garden.DOWN))


class Region:
    def __init__(self, plots: List[Plot], garden: Garden):
        self.plots = plots
        self.garden = garden

    def number_of_sides(self) -> int:
        return self.garden.traverse_region_borders(self)

    def area(self) -> int:
        return len(self.plots)

    def perimeter(self) -> int:
        return sum([(4 - plot.number_akin_neighbors) for plot in self.plots])

    def fence_price(self) -> int:
        return self.area() * self.perimeter()

    def fence_price_part2(self) -> int:
        return self.area() * self.number_of_sides()


class Day12(TestCase):

    def test_day12_part1(self):
        garden = Garden(data)
        print(f"Total price of fence {garden.total_fence_price()}")

    def test_day12_part2(self):
        garden = Garden(data)
        print(f"Total price of fence (counting sides) {garden.total_fence_price_part2()}")