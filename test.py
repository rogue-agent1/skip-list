import random; random.seed(42)
from skip_list import SkipList
sl = SkipList()
for i in range(100):
    sl.insert(i, i*10)
assert len(sl) == 100
assert sl.search(50) == 500
assert sl.search(999) is None
assert 50 in sl
sl.delete(50)
assert 50 not in sl
assert len(sl) == 99
items = sl.to_list()
assert items == sorted(items, key=lambda x: x[0])
sl.insert(50, 555)
assert sl.search(50) == 555
print("skip_list tests passed")
