#!/usr/bin/env python3
"""Skip List — probabilistic sorted data structure."""
import random
class Node:
    def __init__(self,key=None,level=0):
        self.key=key; self.forward=[None]*(level+1)
class SkipList:
    def __init__(self,max_level=16,p=0.5):
        self.max_level=max_level; self.p=p; self.header=Node(level=max_level); self.level=0
    def _random_level(self):
        lvl=0
        while random.random()<self.p and lvl<self.max_level: lvl+=1
        return lvl
    def insert(self,key):
        update=[None]*(self.max_level+1); curr=self.header
        for i in range(self.level,-1,-1):
            while curr.forward[i] and curr.forward[i].key<key: curr=curr.forward[i]
            update[i]=curr
        lvl=self._random_level()
        if lvl>self.level:
            for i in range(self.level+1,lvl+1): update[i]=self.header
            self.level=lvl
        node=Node(key,lvl)
        for i in range(lvl+1): node.forward[i]=update[i].forward[i]; update[i].forward[i]=node
    def search(self,key):
        curr=self.header
        for i in range(self.level,-1,-1):
            while curr.forward[i] and curr.forward[i].key<key: curr=curr.forward[i]
        curr=curr.forward[0]
        return curr is not None and curr.key==key
    def delete(self,key):
        update=[None]*(self.max_level+1); curr=self.header
        for i in range(self.level,-1,-1):
            while curr.forward[i] and curr.forward[i].key<key: curr=curr.forward[i]
            update[i]=curr
        curr=curr.forward[0]
        if curr and curr.key==key:
            for i in range(self.level+1):
                if update[i].forward[i]!=curr: break
                update[i].forward[i]=curr.forward[i]
            while self.level>0 and self.header.forward[self.level] is None: self.level-=1
    def to_list(self):
        result=[]; curr=self.header.forward[0]
        while curr: result.append(curr.key); curr=curr.forward[0]
        return result
if __name__=="__main__":
    sl=SkipList()
    for x in [3,6,7,9,12,19,17,26,21,25]: sl.insert(x)
    assert sl.search(19); assert not sl.search(20)
    sl.delete(19); assert not sl.search(19)
    print(f"Skip list: {sl.to_list()}"); print("Skip List OK")
