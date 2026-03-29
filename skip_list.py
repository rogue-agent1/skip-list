#!/usr/bin/env python3
"""skip_list - Probabilistic sorted data structure."""
import sys, argparse, json, random

class SkipNode:
    def __init__(self, key, value=None, level=0):
        self.key = key
        self.value = value
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level=16, p=0.5):
        self.max_level = max_level
        self.p = p
        self.header = SkipNode(-float("inf"), None, max_level)
        self.level = 0
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
        lvl = self._random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.header
            self.level = lvl
        node = SkipNode(key, value, lvl)
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
        return current.value if current and current.key == key else None
    def to_list(self):
        result = []
        node = self.header.forward[0]
        while node:
            result.append({"key": node.key, "value": node.value})
            node = node.forward[0]
        return result

def main():
    p = argparse.ArgumentParser(description="Skip list CLI")
    p.add_argument("action", choices=["demo", "bench"])
    p.add_argument("-n", type=int, default=100)
    args = p.parse_args()
    sl = SkipList()
    if args.action == "demo":
        for i in range(args.n):
            sl.insert(i, f"val_{i}")
        print(json.dumps({"size": sl.size, "levels": sl.level, "sample": sl.to_list()[:10]}, indent=2))
    elif args.action == "bench":
        import time
        t0 = time.time()
        for i in range(args.n):
            sl.insert(random.randint(0, args.n * 10), i)
        t1 = time.time()
        found = sum(1 for i in range(args.n) if sl.search(i) is not None)
        t2 = time.time()
        print(json.dumps({"inserts": args.n, "insert_ms": round((t1-t0)*1000,2), "search_ms": round((t2-t1)*1000,2), "found": found}))

if __name__ == "__main__":
    main()
