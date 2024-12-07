from data import rules, updates
from unittest import TestCase 
from collections import defaultdict
from typing import List, Tuple

class Day5(TestCase):
    
    def test_day5_part1(self):
        rules_list = rules.splitlines()
        rules_dict = defaultdict(list)

        for rule in rules_list:
            # a|b means that a must appear before b, if at all -> equivalent to: a can not appear after b
            # a growing list stores the forbidden numbers: number at idx i must obey rules for numbers at 0, ..., i-1
            a, b = rule.split("|")
            rules_dict[int(b)].append(int(a))
        
        def does_update_obey_rules(upd: List[int]) -> bool:
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

        print(f"sum mid of valid updates = {total}")

    def test_day5_part2(self):
        rules_list = rules.splitlines()
        rules_dict = defaultdict(list)

        for rule in rules_list:
            # a|b means that a must appear before b, if at all -> equivalent to: a can not appear after b
            # a growing list stores the forbidden numbers: number at idx i must obey rules for numbers at 0, ..., i-1
            a, b = rule.split("|")
            rules_dict[int(b)].append(int(a))

        def correct_update_if_necessary(upd: List[int]) -> Tuple[List[int], bool]:
            corrected = False
            upd_reversed = list(reversed(upd)) # starting from the end
            for num in upd_reversed:
                i = upd.index(num)
                # dictionary of not allowed numbers, for numbers before num
                not_allowed_numbers = dict(filter(lambda item: item[0] in upd[0:i], rules_dict.items()))
                # first number after which num can't appear
                idx = min([upd.index(n) for n, listn in not_allowed_numbers.items() if upd[i] in listn], default=None)
                if idx is not None:
                    # insert num before that number
                    upd.insert(idx, upd.pop(i))
                    corrected = True
            return (upd, corrected)
        
        total = 0
        for upd in updates.splitlines():
            update_numbers = [int(x) for x in upd.split(",")]
            corrected_update, corrected = correct_update_if_necessary(update_numbers)
            if corrected:
                total += corrected_update[int((len(corrected_update) - 1)/2)]

        print(f"sum mid of corrected updates = {total}")

