#!/usr/bin/env python3
"""Skip list implementation — probabilistic sorted data structure."""
import sys, random, math

class Node:
    def __init__(self, key=None, val=None, level=0):
        self.key, self.val = key, val
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level=16, p=0.5):
        self.max_level = max_level
        self.p = p
        self.header = Node(level=max_level)
        self.level = 0
        self.size = 0
    def _random_level(self):
        lvl = 0
        while random.random() < self.p and lvl < self.max_level: lvl += 1
        return lvl
    def insert(self, key, val=None):
        update = [None] * (self.max_level + 1)
        cur = self.header
        for i in range(self.level, -1, -1):
            while cur.forward[i] and cur.forward[i].key < key: cur = cur.forward[i]
            update[i] = cur
        cur = cur.forward[0]
        if cur and cur.key == key: cur.val = val; return
        lvl = self._random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1): update[i] = self.header
            self.level = lvl
        node = Node(key, val, lvl)
        for i in range(lvl + 1):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node
        self.size += 1
    def search(self, key):
        cur = self.header
        for i in range(self.level, -1, -1):
            while cur.forward[i] and cur.forward[i].key < key: cur = cur.forward[i]
        cur = cur.forward[0]
        return cur.val if cur and cur.key == key else None
    def display(self):
        for i in range(self.level, -1, -1):
            cur = self.header.forward[i]
            row = f"L{i}: "
            while cur: row += f"{cur.key} → "; cur = cur.forward[i]
            print(row + "None")

if __name__ == '__main__':
    sl = SkipList()
    if '--demo' in sys.argv:
        n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 20
        for i in random.sample(range(1, n*10), n): sl.insert(i, f"val_{i}")
        sl.display()
        print(f"\nSize: {sl.size}")
    else:
        print("Skip List. Commands: insert <key> [val], search <key>, show, size, quit")
        while True:
            try: line = input('> ').split()
            except EOFError: break
            if not line: continue
            if line[0] == 'quit': break
            elif line[0] == 'insert': sl.insert(int(line[1]), line[2] if len(line)>2 else None); print("OK")
            elif line[0] == 'search': print(sl.search(int(line[1])))
            elif line[0] == 'show': sl.display()
            elif line[0] == 'size': print(sl.size)
