from data import rules, updates
from unittest import TestCase 
from collections import defaultdict
from typing import List

class Day5(TestCase):
    
    def test_day5_part1(self):
        rules_list = rules.splitlines()
        rules_dict = defaultdict(list)

        for rule in rules_list:
            a, b = rule.split("|")
            rules_dict[int(b)].append(int(a))
        
        def does_update_obey_rules(upd: List[int]) -> bool:
            # a|b means that a must appear before b, if at all -> equivalent to: a can not appear after b
            # a growing list stores the forbidden numbers: number at idx i must obey rules for numbers at 0, ..., i-1
            not_allowed_numbers = []
            for n in upd:
                if n in not_allowed_numbers:
                    return False
                not_allowed_numbers.extend(rules_dict[n])
            return True
        
        total = 0
        for upd in updates.splitlines():
            update_numbers = [int(x) for x in upd.split(",")]
            if does_update_obey_rules(update_numbers):
                total += update_numbers[int((len(update_numbers) - 1)/2)]

        print(f"sum = {total}")

    def test_day5_part2(self):
        pass