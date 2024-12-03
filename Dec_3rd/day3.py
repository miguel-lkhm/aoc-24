import operator
import re
from unittest import TestCase

from data import data


class Day3(TestCase):

    def test_day3_part1(self):
        pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
        matches = re.findall(pattern, data)
        total = sum([int(tuple[0]) * int(tuple[1]) for tuple in matches])
        print(total)

    def test_day3_part2(self):
        pattern_mul = r"mul\((\d{1,3}),(\d{1,3})\)"
        pattern_do = r"do\(\)"
        pattern_dont = r"don't\(\)"

        dos = [do.end() for do in re.finditer(pattern_do, data)]
        donts = [dont.end() for dont in re.finditer(pattern_dont, data)]
        total = sum([int(match.group(1)) * int(match.group(2)) for match in re.finditer(pattern_mul, data) if
                     max([0] + [do for do in dos if do < match.start()]) >
                     max([-1] + [dont for dont in donts if dont < match.start()])])
        print(total) # not correct

    def test_day3_part2_2ndtry(self):
        pattern_mul = r"mul\((\d{1,3}),(\d{1,3})\)"
        pattern_do = r"do\(\)"
        pattern_dont = r"don't\(\)"

        complete_pattern = r"(?P<do>do\(\))|(?P<dont>don't\(\))|(mul\((?P<a>\d{1,3}),(?P<b>\d{1,3})\))"
        flag = True
        total = 0
        for match in re.finditer(complete_pattern, data):
            do = match.group("do")
            dont = match.group("dont")
            a = match.group("a")
            b = match.group("b")
            # idk how to do xor with n truthy/falsy variables in python
            if (do and dont) or (do and a) or (dont and a):
                continue
            if match.group("dont"):
                flag = False
                continue
            if match.group("do"):
                flag = True
                continue
            if flag:
                total += int(a) * int(b)

        print(total)