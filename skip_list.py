#!/usr/bin/env python3
"""skip_list — Probabilistic sorted data structure with O(log n) search. Zero deps."""
import sys, random

class Node:
    def __init__(self, key=None, value=None, level=0):
        self.key = key
        self.value = value
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level=16, p=0.5):
        self.max_level = max_level
        self.p = p
        self.level = 0
        self.header = Node(level=max_level)
        self.size = 0

    def _random_level(self):
        lvl = 0
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def insert(self, key, value=None):
        update = [None] * (self.max_level + 1)
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        current = current.forward[0]
        if current and current.key == key:
            current.value = value
            return
        new_level = self._random_level()
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level
        node = Node(key, value, new_level)
        for i in range(new_level + 1):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node
        self.size += 1

    def search(self, key):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]
        if current and current.key == key:
            return current.value
        return None

    def delete(self, key):
        update = [None] * (self.max_level + 1)
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        current = current.forward[0]
        if not current or current.key != key:
            return False
        for i in range(self.level + 1):
            if update[i].forward[i] != current:
                break
            update[i].forward[i] = current.forward[i]
        while self.level > 0 and self.header.forward[self.level] is None:
            self.level -= 1
        self.size -= 1
        return True

    def __iter__(self):
        node = self.header.forward[0]
        while node:
            yield node.key, node.value
            node = node.forward[0]

def main():
    sl = SkipList()
    data = [3, 6, 7, 9, 12, 19, 17, 26, 21, 25]
    for x in data:
        sl.insert(x, x * 10)
    print(f"Skip list ({sl.size} items, {sl.level} levels):")
    for k, v in sl:
        print(f"  {k} -> {v}")
    print(f"\nSearch 19: {sl.search(19)}")
    print(f"Search 20: {sl.search(20)}")
    sl.delete(19)
    print(f"After deleting 19, search 19: {sl.search(19)}")
    print(f"Size: {sl.size}")

if __name__ == "__main__":
    main()
