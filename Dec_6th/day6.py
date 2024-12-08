from typing import Optional, Tuple
from data import data
from unittest import TestCase
from copy import deepcopy

class CharMatrix:
    def __init__(self, data: str):
        lines = data.split('\n')
        self.n, self.m = len(lines), len(lines[0])
        self.matrix = [list(line) for line in lines]

    def deep_copy(self):
        new_char_matrix = CharMatrix("")
        new_char_matrix.matrix = deepcopy(self.matrix)
        new_char_matrix.n, new_char_matrix.m = self.n, self.m
        return new_char_matrix

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
        return ([point[0] + dir[0], point[1] + dir[1]])

    def find_first_value(self, val: str) -> Optional[Tuple[int, int]]:
        for i in range(self.n):
            for j in range(self.m):
                if self.get_value((i, j)) == val:
                    return (i, j)
        return None
    
    def print(self):
        for row in self.matrix:
            print("\t".join(row))

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
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)] # up, right, down, left
        dir_names = ["u", "r", "d", "l"]

        def simulate_guard_path_from_point_in_dir(matrix_copy: CharMatrix, starting_point: Tuple[int, int], idx_dir: int) -> bool:
            current_pos = starting_point
            while matrix_copy.get_value(current_pos) != "$":
                current_val = matrix_copy.get_value(current_pos)
                if dir_names[idx_dir] in current_val: 
                    # if this position has already been traversed in this direction, we found a loop
                    matrix_copy.print()
                    print("")
                    print("*****************************************************************************")
                    print("")
                    return True
                else:
                    # mark the position with the direction in which it's just been traversed
                    matrix_copy.set_value(current_pos, current_val + dir_names[idx_dir]) 

                if matrix_copy.get_value(matrix_copy.move_from(current_pos, directions[idx_dir])) == "#":
                    idx_dir = (idx_dir + 1) % 4 # change direction to relative right

                current_pos = matrix_copy.move_from(current_pos, directions[idx_dir])
            # while-loop ended because the guard exited the matrix, then there's no loop
            return False

        M = CharMatrix(data)
        start = M.find_first_value("^")
        assert start is not None
        obstacle_positions = []
        idx_dir = 0

        current_pos = start
        while M.get_value(current_pos) != "$":
            next_val = M.get_value(M.move_from(current_pos, directions[idx_dir]))
            if next_val == "#":
                idx_dir = (idx_dir + 1) % 4 # change direction to relative right
            elif next_val != "$":
                # if the next position is not an obstacle, check if adding one would create a loop
                M_copy = M.deep_copy()
                new_obstacle_position = M_copy.move_from(current_pos, directions[idx_dir])
                M_copy.set_value(new_obstacle_position, "#")
                if simulate_guard_path_from_point_in_dir(M_copy, current_pos, idx_dir):
                    obstacle_positions.append(tuple(new_obstacle_position))

            M.set_value(current_pos, M.get_value(current_pos) + dir_names[idx_dir]) # mark

            current_pos = M.move_from(current_pos, directions[idx_dir])


        print(f"number of possible obstacles that lead to loops = {len(set(obstacle_positions))}")

if __name__ == "__main__":
    day6 = Day6()
    day6.test_day6_part2()