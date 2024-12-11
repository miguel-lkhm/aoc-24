from unittest import TestCase
from typing import List, Tuple, Union
from data import data

class Stone:
    def __init__(self, n: int):
        self.n = n

    def has_even_number_of_digits(self) -> bool:
        return len(str(self.n)) % 2 == 0

    def transform(self) -> List['Stone']:
        if self.n == 0:
            return list([Stone(1)])
        if self.has_even_number_of_digits():
            # split digits evenly
            n_str = str(self.n)
            mid_point = int(len(n_str) / 2)
            n1, n2 = int(n_str[:mid_point]), int(n_str[mid_point:])
            return list([Stone(n1), Stone(n2)])
        else:
            return list([Stone(self.n * 2024)])

class StoneRow:
    def __init__(self, numbers: List[int]):
        self.stones = [Stone(num) for num in numbers]

    def transform_stone_at_index(self, idx: int, tmp_stone_row:'StoneRow'):
        assert 0 <= idx < len(self.stones)
        transformation_result = self.stones[idx].transform()
        for stone in reversed(transformation_result):
            tmp_stone_row.stones.insert(idx, stone)

    def blink_once(self):
        tmp_stone_row = StoneRow([])
        for i in range(len(self.stones)):
            self.transform_stone_at_index(i,tmp_stone_row)
        self.stones = tmp_stone_row.stones

    def blink_n_times(self, n):
        for i in range(n):
            self.blink_once()
            print(f"Blinked {i+1} times")



class Day11(TestCase):

    def test_day11_part_1(self):
        initial_numbers =[int(w) for w in data.split(" ")]
        # initial_numbers = [125, 17]
        stone_line = StoneRow(initial_numbers)
        stone_line.blink_n_times(25)
        print(f"Number of stones: {len(stone_line.stones)}")

    def test_day11_part_2(self):
        initial_numbers = [int(w) for w in data.split(" ")]
        stone_line = StoneRow(initial_numbers)
        stone_line.blink_n_times(75)
        print(f"Number of stones: {len(stone_line.stones)}")