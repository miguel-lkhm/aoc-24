from typing import Tuple
from unittest import TestCase
from data import data


class FileBlock:
    def __init__(self, size: int, id: int, is_blank=False):
        self.size = size
        self.is_blank = is_blank
        if self.is_blank:
            self.id = None
        else:
            self.id = id
    def get_blocks(self):
        return [Block(is_blank=self.is_blank, id=self.id) for _ in range(self.size)]


class Block:
    def __init__(self, is_blank=False, id=None):
        self.is_blank = is_blank
        if not self.is_blank and id is not None:
            self.id = id
        else:
            self.id = None


class Day9(TestCase):

    def test_day9_part_1(self):
        disk_in_fileblocks = [
            FileBlock(size=int(char), id=int(i / 2)) if i % 2 == 0 else FileBlock(size=int(char), id=-1, is_blank=True)
            for i, char in enumerate(data)]
        disk_in_blocks = []
        for fb in disk_in_fileblocks:
            disk_in_blocks.extend(fb.get_blocks())

        def last_non_empty_block() -> Tuple[int, Block]:
            for idx, block in enumerate(reversed(disk_in_blocks)):
                if not block.is_blank:
                    return len(disk_in_blocks) - idx - 1, block

        def first_empty_block() -> Tuple[int, Block]:
            for idx, block in enumerate(disk_in_blocks):
                if block.is_blank:
                    return idx, block

        idx_last_non_empty, idx_first_empty = last_non_empty_block()[0], first_empty_block()[0]

        while idx_last_non_empty > idx_first_empty:
            tmp = disk_in_blocks[idx_last_non_empty]
            disk_in_blocks[idx_last_non_empty] = disk_in_blocks[idx_first_empty]
            disk_in_blocks[idx_first_empty] = tmp
            # disk_in_blocks[idx_last_non_empty] , disk_in_blocks[idx_first_empty] = disk_in_blocks[idx_first_empty], disk_in_blocks[idx_last_non_empty]

            idx_last_non_empty, idx_first_empty = last_non_empty_block()[0], first_empty_block()[0]

        checksum = sum([idx*block.id for idx, block in enumerate(disk_in_blocks)])

        print(f"checksum {checksum}")


    def test_day9_part_2(self):
        pass
