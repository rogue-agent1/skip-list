#!/usr/bin/env python3
"""skip_list - Probabilistic skip list with O(log n) search."""
import sys, json, random

class SkipNode:
    def __init__(self, key=None, value=None, level=0):
        self.key = key; self.value = value
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level=16, p=0.5):
        self.max_level = max_level; self.p = p; self.level = 0
        self.header = SkipNode(level=max_level)
        self.size = 0; self._rng = random.Random(42)
    
    def _random_level(self):
        lvl = 0
        while self._rng.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl
    
    def search(self, key):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]
        if current and current.key == key:
            return current.value
        return None
    
    def insert(self, key, value):
        update = [None] * (self.max_level + 1)
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        current = current.forward[0]
        if current and current.key == key:
            current.value = value; return
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
    
    def delete(self, key):
        update = [None] * (self.max_level + 1)
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        target = current.forward[0]
        if target and target.key == key:
            for i in range(self.level + 1):
                if update[i].forward[i] != target: break
                update[i].forward[i] = target.forward[i]
            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1
            self.size -= 1; return True
        return False
    
    def to_list(self):
        result = []; current = self.header.forward[0]
        while current:
            result.append((current.key, current.value)); current = current.forward[0]
        return result

def main():
    sl = SkipList()
    print("Skip list demo\n")
    for i in [5,3,8,1,9,2,7,4,6,10]:
        sl.insert(i, f"val_{i}")
    print(f"  Size: {sl.size}, levels: {sl.level+1}")
    print(f"  Search(5): {sl.search(5)}")
    print(f"  Search(11): {sl.search(11)}")
    sl.delete(5); sl.delete(8)
    print(f"  After delete 5,8: {[k for k,v in sl.to_list()]}")
    # Benchmark insert order
    sl2 = SkipList()
    for i in range(1000): sl2.insert(i, i)
    print(f"  1000 sequential: levels={sl2.level+1}, search(500)={sl2.search(500)}")

if __name__ == "__main__":
    main()
