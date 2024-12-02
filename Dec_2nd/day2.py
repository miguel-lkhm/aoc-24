from typing import List
from unittest import TestCase
from data import data


class Day2(TestCase):

    def test_day2_part1(self):
        def is_report_safe(list: List[int]) -> bool:
            max_abs = 3
            min_abs = 1

            for i, _ in enumerate(list[1:], start=1):
                diff_b = list[i] - list[i - 1]
                if abs(diff_b) > max_abs or abs(diff_b) < min_abs:
                    return False
                if i >= 2:
                    diff_a = list[i - 1] - list[i - 2]
                    if diff_a * diff_b < 0:
                        return False

            return True
        num_safe_reports = 0
        for line in data.split("\n"):
            report = [int(x) for x in line.split(" ")]
            if is_report_safe(report):
                num_safe_reports += 1


        print(f"Number of safe reports {num_safe_reports}")

    def test_day2_part2(self):
        def is_report_safe(list: List[int]) -> bool:
            max_abs = 3
            min_abs = 1
            for i, _ in enumerate(list[1:], start=1):
                diff_b = list[i] - list[i - 1]
                if abs(diff_b) > max_abs or abs(diff_b) < min_abs:
                    return False
                if i >= 2:
                    diff_a = list[i - 1] - list[i - 2]
                    if diff_a * diff_b < 0:
                        return False
            return True

        def is_report_safe_with_prob_dampener(list: List[int]) -> bool:
            new_list = list[:]
            for i, _ in enumerate(list):
                new_list.pop(i)
                if is_report_safe(new_list):
                    return True
                new_list = list[:]
            return False

        num_safe_reports = 0
        for line in data.split("\n"):
            report = [int(x) for x in line.split(" ")]
            if is_report_safe_with_prob_dampener(report):
                num_safe_reports += 1

        print(f"Number of safe reports with problem dampener {num_safe_reports}")