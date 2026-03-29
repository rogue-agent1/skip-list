#!/usr/bin/env python3
"""skip_list - Probabilistic skip list data structure."""
import sys, random

class Node:
    def __init__(self, key, value, level):
        self.key = key
        self.value = value
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level=16, p=0.5):
        self.max_level = max_level
        self.p = p
        self.level = 0
        self.header = Node(None, None, max_level)
        self.size = 0
    def _random_level(self):
        lvl = 0
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl
    def insert(self, key, value):
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
        lvl = self._random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.header
            self.level = lvl
        node = Node(key, value, lvl)
        for i in range(lvl + 1):
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
    def to_list(self):
        result = []
        node = self.header.forward[0]
        while node:
            result.append((node.key, node.value))
            node = node.forward[0]
        return result

def test():
    random.seed(42)
    sl = SkipList()
    for i in [5, 3, 7, 1, 9, 2, 8]:
        sl.insert(i, i * 10)
    assert sl.size == 7
    assert sl.search(3) == 30
    assert sl.search(99) is None
    keys = [k for k, v in sl.to_list()]
    assert keys == sorted(keys)
    sl.delete(3)
    assert sl.search(3) is None
    assert sl.size == 6
    print("OK: skip_list")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: skip_list.py test")
