from unittest import TestCase
from typing import List, Tuple, Union
from data import data
from collections import defaultdict, Counter

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
    blink_5_map = defaultdict(list)
    blink_10_map = defaultdict(list)
    blink_20_map = defaultdict(list)

    def has_even_number_of_digits(self, n) -> bool:
        return len(str(n)) % 2 == 0

    def transform(self, n) -> List[int]:
        if n == 0:
            return list([1])
        if self.has_even_number_of_digits(n):
            # split digits evenly
            n_str = str(n)
            mid_point = int(len(n_str) / 2)
            n1, n2 = int(n_str[:mid_point]), int(n_str[mid_point:])
            return list([n1, n2])
        else:
            return list([n * 2024])

    def blink_5_times(self, n) -> List[int]:
        if n in self.blink_5_map:
            return self.blink_5_map[n]
        new_list = [n]
        for _ in range(5):
            aux = list([])
            for num in new_list:
                aux.extend(self.transform(num))
            new_list = aux
        self.blink_5_map[n] = new_list
        return new_list

    def blink_5n_times(self, numbers: List[int], times: int) -> List[int]:
        assert times % 5 == 0
        cycles = int(times/5)
        # num_list = []
        for x in range(cycles):
            aux = list([])
            for n in numbers:
                aux.extend(self.blink_5_times(n))
            numbers = aux
            #print(f"Blinked {(x+1)*5} times")
        return numbers

    def blink_10_times(self, n: int) -> List[int]:
        if n in self.blink_10_map:
            return self.blink_10_map[n]
        result_list = self.blink_5n_times([n], 10)
        self.blink_10_map[n] = result_list
        return result_list

    def blink_20_times(self, n: int) -> List[int]:
        if n in self.blink_20_map:
            return self.blink_20_map[n]
        result_list = self.blink_5n_times([n], 20)
        self.blink_20_map[n] = result_list
        return result_list

    def blink_25_times(self, numbers: List[int]) -> List[int]:
        aux = list([])
        for n in numbers:
            aux.extend(self.blink_10_times(n))
        numbers = aux
        aux = list([])
        for n in numbers:
            aux.extend(self.blink_10_times(n))
        numbers = aux
        aux = list([])
        for n in numbers:
            aux.extend(self.blink_5_times(n))
        numbers = aux
        
        return numbers

    def blink_50_times(self, numbers: List[int]) -> List[int]:
        aux = list([])
        for n in numbers:
            aux.extend(self.blink_20_times(n))
        numbers = aux
        aux = list([])
        for n in numbers:
            aux.extend(self.blink_20_times(n))
        numbers = aux
        aux = list([])
        for n in numbers:
            aux.extend(self.blink_10_times(n))
        numbers = aux
        
        return numbers


    def _day11_part_1(self):
        initial_numbers =[int(w) for w in data.split(" ")]
        # initial_numbers = [125, 17]
        stone_line = StoneRow(initial_numbers)
        stone_line.blink_n_times(25)
        print(f"Number of stones: {len(stone_line.stones)}")

    def _day11_part_1_ver2(self):
        initial_numbers =[int(w) for w in data.split(" ")]
        result_list = self.blink_5n_times(initial_numbers, 50)
        print(f"Number of stones (version 2): {len(result_list)}")

    def _day11_part_1_ver3(self):
        initial_numbers =[int(w) for w in data.split(" ")]
        result_list = self.blink_50_times(initial_numbers)
        print(f"Number of stones (version 3): {len(result_list)}")

    def _day11_part_2(self):
        initial_numbers = [int(w) for w in data.split(" ")]
        stone_line = StoneRow(initial_numbers)
        stone_line.blink_n_times(75)
        print(f"Number of stones: {len(stone_line.stones)}")

    def _day11_part_2_ver2(self):
        initial_numbers =[int(w) for w in data.split(" ")]
        result_list = self.blink_5n_times(initial_numbers, 75)
        print(f"Number of stones (version 2): {len(result_list)}")

    def _generators(self):
        listn = [1, 2, 3, 4, 5]

        def gen(num, iteration: int):
            if iteration < 5:
                yield from gen(num*2, iteration=iteration+1)
                yield from gen(num*3, iteration=iteration+1)
            else:
                yield num
        
        for x in gen(5, 0):
            print(x)

    def _day11_part2_ver4(self):
        initial_numbers =[int(w) for w in data.split(" ")]
        # max_iteration = 25
        print("*********************")
        print("Using generators")

        def gen(num: int, iteration: int):
            if iteration < 35:
                if num == 0:
                    yield from gen(1, iteration=iteration+1)
                elif len(str(num)) % 2 == 0:
                    n_str = str(num)
                    mid_point = int(len(n_str) / 2)
                    n1, n2 = int(n_str[:mid_point]), int(n_str[mid_point:])
                    yield from gen(n1, iteration=iteration+1)
                    yield from gen(n2, iteration=iteration+1)
                else:
                    yield from gen(num*2024, iteration=iteration+1)
            else:
                yield num
        
        count = 0
        for n in initial_numbers:
            for x in gen(n, 0):
                count += 1
        print(f"total number {count}")

    def test_day11_part2_ver5(self):
        blink_5_map_dict = defaultdict(dict) # cache

        def blink_5_times(n) -> dict[int, int]:
            if n in blink_5_map_dict:
                return blink_5_map_dict[n]
            new_list = [n]
            for _ in range(5):
                aux = list([])
                for num in new_list:
                    aux.extend(self.transform(num))
                new_list = aux
            new_dict = dict(Counter(new_list))
            blink_5_map_dict[n] = new_dict
            return new_dict
        

        def blink_5n_times(numbers: dict[int, int], times: int) -> dict[int, int]:
            cycles = int(times/5)
            # num_list = []
            for _ in range(cycles):
                aux_dict = {}
                for num, times in numbers.items():
                    d = {k:v*times for k, v in blink_5_times(num).items()}
                    for k, v in d.items():
                        if k in aux_dict:
                            aux_dict[k] += v
                        else:
                            aux_dict[k] = v
                numbers = aux_dict

            return numbers
        
        initial_numbers =[int(w) for w in data.split(" ")]
        num_dict = dict(Counter(initial_numbers))
        result = blink_5n_times(num_dict, 75)
        total = sum([v for v in result.values()])
        print(total)

        

# if __name__ == "__main__":
#     day11 = Day11()
#     day11.test_day11_part2_ver4()