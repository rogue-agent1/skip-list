import argparse, random

class Node:
    def __init__(self, key, level):
        self.key = key
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level=16, p=0.5):
        self.max_level = max_level
        self.p = p
        self.header = Node(-1, max_level)
        self.level = 0
        self.size = 0

    def random_level(self):
        lvl = 0
        while random.random() < self.p and lvl < self.max_level: lvl += 1
        return lvl

    def insert(self, key):
        update = [None] * (self.max_level + 1)
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        lvl = self.random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1): update[i] = self.header
            self.level = lvl
        node = Node(key, lvl)
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
        return current and current.key == key

    def display(self):
        for i in range(self.level + 1):
            node = self.header.forward[i]
            keys = []
            while node:
                keys.append(str(node.key))
                node = node.forward[i]
            print(f"Level {i}: {' -> '.join(keys)}")

def main():
    p = argparse.ArgumentParser(description="Skip list")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--insert", nargs="+", type=int)
    p.add_argument("--search", type=int)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()
    random.seed(args.seed)
    sl = SkipList()
    if args.demo:
        for v in [3, 6, 7, 9, 12, 19, 17, 26, 21, 25]:
            sl.insert(v)
        sl.display()
        print(f"\nSearch 19: {sl.search(19)}")
        print(f"Search 15: {sl.search(15)}")
        print(f"Size: {sl.size}")
    elif args.insert:
        for v in args.insert: sl.insert(v)
        sl.display()
        if args.search is not None:
            print(f"Search {args.search}: {sl.search(args.search)}")
    else: p.print_help()

if __name__ == "__main__":
    main()
