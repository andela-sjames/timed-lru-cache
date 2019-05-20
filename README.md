# timed-lru-cache
A time constraint LRUCache Implementation

### Summary
The timed LRUCache is a dict-like container that is also size limited.
It uses the prune method when instantiated with time to remove time expired objects.


### Example

#### Simple LRUCache

```python
from lru_cache import LRUCache

lru = LRUCache(maxSize=4)
lru.insert_key_value("a", 99)

lru.insert_key_value("b", 202)
lru["c"] = 203
lru["d"] = 204
lru["e"] = 205

lru.get_value("a")
lru.get("a", None)

print(lru)
print(lru.values())

# LRUCache(timeout=None, size=4, data={'b': 202, 'c': 203, 'd': 204, 'e': 205})
# [202, 203, 204, 205]
```

#### Test memoization: Sample use with the decorator
```Python
from lru_cache import LRUCache
from memoize_decorator import MemoizedCache

@MemoizedCache(cache=LRUCache(maxSize=5))
def get_random(max_value):
    import random
    return random.random() * max_value

print(get_random(1)) # 0.8926141265778564
print(get_random(1)) # 0.89261gs41265778564
print(get_random(3)) # 1.9138579745807172
print(get_random(4)) # 3.5772986693895916
print(get_random(5)) # 0.5001657308606899
print(get_random(5)) # 0.5001657308606899
print(get_random(7)) # 0.7652871914811611
print(get_random(1)) # 0.6811475789638526

print(get_random.misses)
# => 7
print(get_random.hits)
# => 2

# cache info
get_random.cache_info()
# => MemoizedCache(hits=2, misses=7, maxsize=5, currsize=5)

# Simple report on performance
report = f'Hit %: {(float(get_random.hits) / (get_random.hits + get_random.misses))}'
print(report)
# => Hit %: 0.2222222222222222
```

#### Test time constraint
```Python
from time import sleep
from lru_cache import LRUCache

timed_lru = LRUCache(maxSize = 4, timeout=10)

timed_lru["a"] = 202
timed_lru["b"] = 203
timed_lru["c"] = 204
timed_lru["d"] = 205
timed_lru["e"] = 206
print(timed_lru) # LRUCache(timeout=10, size=4, data={'b': 203, 'c': 204, 'd': 205, 'e': 206})

sleep(60)
timed_lru["d"] = 203
timed_lru["e"] = 204
timed_lru["f"] = 205
timed_lru["g"] = 206
timed_lru["h"] = 207
print(timed_lru) # LRUCache(timeout=10, size=4, data={'e': 204, 'f': 205, 'g': 206, 'h': 207})

sleep(30)
print(timed_lru) # LRUCache(timeout=10, size=4, data={})
timed_lru.stop_timer()
```