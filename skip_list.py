#!/usr/bin/env python3
"""skip_list - Skip list implementation."""
import sys, random, math
class Node:
    def __init__(self, key, level):
        self.key = key; self.forward = [None] * (level + 1)
class SkipList:
    def __init__(self, max_level=16, p=0.5):
        self.max_level = max_level; self.p = p; self.level = 0
        self.header = Node(-math.inf, max_level); self.size = 0
    def random_level(self):
        lvl = 0
        while random.random() < self.p and lvl < self.max_level: lvl += 1
        return lvl
    def insert(self, key):
        update = [None] * (self.max_level + 1); current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key: current = current.forward[i]
            update[i] = current
        lvl = self.random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1): update[i] = self.header
            self.level = lvl
        node = Node(key, lvl)
        for i in range(lvl + 1): node.forward[i] = update[i].forward[i]; update[i].forward[i] = node
        self.size += 1
    def search(self, key):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key: current = current.forward[i]
        current = current.forward[0]
        return current and current.key == key
    def display(self):
        for i in range(self.level, -1, -1):
            node = self.header.forward[i]; vals = []
            while node: vals.append(str(node.key)); node = node.forward[i]
            print(f"Level {i}: {' -> '.join(vals)}")
if __name__ == "__main__":
    sl = SkipList()
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        nums = random.sample(range(1, n*3), n)
        for x in nums: sl.insert(x)
        sl.display(); print(f"Size: {sl.size}")
        test = random.choice(nums)
        print(f"Search {test}: {sl.search(test)}")
        print(f"Search {n*3+1}: {sl.search(n*3+1)}")
    else: print("Usage: skip_list demo [n]")
