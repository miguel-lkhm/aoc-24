from unittest import TestCase
from data import data

class Day1(TestCase):

    def test_day1_part1(self):
        entries = data.split('\n')
        list_1, list_2 = [], []
        for entry in entries:
            e1, e2 = entry.split('-')
            list_1.append(int(e1))
            list_2.append(int(e2))

        # list_1 = [3, 4, 2, 1, 3, 3]
        # list_2 = [4, 3, 5, 3, 9, 3]

        sorted_list_1 = sorted(list_1)
        sorted_list_2 = sorted(list_2)

        distance = sum([abs(a-b) for a,b in zip(sorted_list_1, sorted_list_2) ])
        print(distance)

    def test_day1_part2(self):
        entries = data.split('\n')
        list_1, list_2 = [], []
        for entry in entries:
            e1, e2 = entry.split('-')
            list_1.append(int(e1))
            list_2.append(int(e2))

        # sorted_list_1 = sorted(list_1)
        # sorted_list_2 = sorted(list_2)
        seen, sim = [], []
        for le in list_1:
            if le in seen:
                continue
            sim.append(int(le)*list_2.count(le))
            seen.append(le)

        total_sim = sum(sim)

        print(total_sim)
