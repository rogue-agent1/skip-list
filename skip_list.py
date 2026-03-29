#!/usr/bin/env python3
"""Skip list data structure. Zero dependencies."""
import random, sys

class SkipNode:
    def __init__(self, key, value=None, level=0):
        self.key, self.value = key, value
        self.forward = [None] * (level + 1)

class SkipList:
    MAX_LEVEL = 16
    def __init__(self, p=0.5):
        self.p = p
        self.header = SkipNode(None, None, self.MAX_LEVEL)
        self.level = 0
        self.size = 0

    def _random_level(self):
        lvl = 0
        while random.random() < self.p and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def insert(self, key, value=None):
        update = [None] * (self.MAX_LEVEL + 1)
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
        node = SkipNode(key, value, new_level)
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
        update = [None] * (self.MAX_LEVEL + 1)
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

    def __len__(self): return self.size
    def __contains__(self, key): return self.search(key) is not None

if __name__ == "__main__":
    sl = SkipList()
    for i in [3,1,4,1,5,9,2,6]: sl.insert(i, i*10)
    print(sl.to_list())
