"""Test LRUCache Implementation."""

from time import sleep

from lru_cache import LRUCache
from memoize_decorator import MemoizedCache

from utils.cache_thread import StoppableThread


lru = LRUCache(maxSize=4)
lru.insert_key_value("a", 99)

lru["b"] = 202
lru["c"] = 203
lru["d"] = 204
lru["e"] = 205

lru.get_value("a")
lru.get("a", None)

print(lru)
print(lru.values())

# LRUCache(timeout=None, size=4, data={'b': 202, 'c': 203, 'd': 204, 'e': 205})
# [202, 203, 204, 205]


# Test memoization
# Sample Usage with the decorator
@MemoizedCache(cache=LRUCache(maxSize=5))
def get_random(max_value):
    import random
    return random.random() * max_value

print(get_random(1)) # 0.8926141265778564
print(get_random(1)) # 0.8926141265778564
print(get_random(3)) # 1.9138579745807172
print(get_random(4)) # 3.5772986693895916
print(get_random(5)) # 0.5001657308606899
print(get_random(5)) # 0.5001657308606899
print(get_random(7)) # 0.7652871914811611
print(get_random(8)) # 0.4366852743803227

print(get_random.misses)
# => 6
print(get_random.hits)
# => 2

# cache info
get_random.cache_info()
# => MemoizedCache(hits=2, misses=6, maxsize=5, currsize=5)

# Simple report on performance
report = f'Hit %: {(float(get_random.hits) / (get_random.hits + get_random.misses))}'
print(report)
# => Hit %: 0.25


# Test time constraint, this is still buggy :sweat smile:
timed_lru = LRUCache(maxSize = 5, timeout=1)
lruThread = StoppableThread(timed_lru)

timed_lru["a"] = 202
timed_lru["b"] = 203
timed_lru["c"] = 204
timed_lru["d"] = 205
timed_lru["e"] = 206
print(timed_lru)

# calling start on the thread makes a call to the lru.prune() method
# that clears out expired cache after. 
lruThread.start()
# lruThread.join()
sleep(1)
print(timed_lru)

sleep(1)
print(timed_lru)
lruThread.stop()

sleep(1)
print(timed_lru)

sleep(1)
print(timed_lru)
