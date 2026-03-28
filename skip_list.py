#!/usr/bin/env python3
"""skip_list - Probabilistic skip list data structure."""
import sys, random, json, time

class Node:
    def __init__(self, key=None, val=None, level=0):
        self.key, self.val = key, val
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level=16, p=0.5):
        self.max_level, self.p = max_level, p
        self.header = Node(level=max_level)
        self.level = 0; self.size = 0
    def _random_level(self):
        lvl = 0
        while random.random() < self.p and lvl < self.max_level: lvl += 1
        return lvl
    def insert(self, key, val=None):
        update = [None] * (self.max_level + 1)
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        current = current.forward[0]
        if current and current.key == key:
            current.val = val; return
        lvl = self._random_level()
        if lvl > self.level:
            for i in range(self.level+1, lvl+1): update[i] = self.header
            self.level = lvl
        node = Node(key, val, lvl)
        for i in range(lvl+1):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node
        self.size += 1
    def search(self, key):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]
        return current.val if current and current.key == key else None
    def display(self):
        for i in range(self.level, -1, -1):
            node = self.header.forward[i]
            line = f"L{i}: "
            while node: line += f"{node.key} -> "; node = node.forward[i]
            print(line + "None")

def demo(n=20):
    sl = SkipList()
    for i in random.sample(range(1, n*3), n): sl.insert(i, f"v{i}")
    sl.display()
    print(f"\nSize: {sl.size}, Levels: {sl.level+1}")
    k = random.randint(1, n*3)
    print(f"Search({k}): {sl.search(k)}")

def bench(n=100000):
    sl = SkipList()
    start = time.time()
    for i in range(n): sl.insert(i, i)
    ins = time.time() - start
    start = time.time()
    for i in range(n): sl.search(random.randint(0, n))
    srch = time.time() - start
    print(f"  {n:,} inserts: {ins*1000:.0f}ms\n  {n:,} searches: {srch*1000:.0f}ms")

def main():
    args = sys.argv[1:]
    if not args or args[0] == 'demo': demo(int(args[1]) if len(args)>1 else 20)
    elif args[0] == 'bench': bench(int(args[1]) if len(args)>1 else 100000)

if __name__ == '__main__': main()
