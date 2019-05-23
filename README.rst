timed-lru-cache
===============

A time constraint LRUCache Implementation

Summary
~~~~~~~

The timed LRUCache is a dict-like container that is also size limited.
It uses the prune method when instantiated with time to remove time
expired objects.

Example
~~~~~~~

Simple LRUCache
^^^^^^^^^^^^^^^

.. code:: python

   from lrucache.lru_cache import LRUCache

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

   # insert into lrucache
   lru.insert_key_value("j", 302)
   # or
   lru["k"] = 403

   # retrieve from the lrucache
   lru.get_value("z")
   # or
   lru.get("z", None)

   # delete from the lrucache
   lru.delete_key("z")
   # or
   lru.pop("z", None)

Test memoization: Sample use with the decorator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from lrucache.lru_cache import LRUCache
   from lrucache.memoize_decorator import MemoizedCache

   @MemoizedCache(cache=LRUCache(maxSize=5))
   def get_random(max_value):
       import random
       return random.random() * max_value

   print(get_random(1)) # 0.6869437097681024
   print(get_random(1)) # 0.6869437097681024
   print(get_random(3)) # 1.2792457326076399
   print(get_random(4)) # 1.9216226691107239
   print(get_random(5)) # 3.442601057826532
   print(get_random(5)) # 3.442601057826532
   print(get_random(7)) # 0.6831533160972438
   print(get_random(8)) # 7.40200570325546
   print(get_random(1)) # 0.37636284785825047


   print(get_random.misses)
   # => 7
   print(get_random.hits)
   # => 2

   # cache info
   get_random.cache_info()
   # => MemoizedCache(hits=2, misses=7, maxsize=5, currsize=5)

   # reset  hits and misses count.
   get_random.reset()

   # Simple report on performance
   report = f'Hit %: {(float(get_random.hits) / (get_random.hits + get_random.misses))}'
   print(report)
   # => Hit %: 0.2222222222222222

   # check the cache stored key, value, items pairs
   print(get_random.cache.keys())
   # => dict_keys([-5205072475343462643, 8575776084210548143, -2238842041537299568, -8811688270097994377, 2613783748954017437])

   print(get_random.cache.values())
   # => [1.9216226691107239, 3.442601057826532, 0.6831533160972438, 7.40200570325546, 0.37636284785825047]

   print(get_random.cache.items())
   # => [
   #     (-5205072475343462643, 1.9216226691107239), (8575776084210548143, 3.442601057826532), 
   #     (-2238842041537299568, 0.6831533160972438), (-8811688270097994377, 7.40200570325546), 
   #     (2613783748954017437, 0.37636284785825047)
   # ]

Test time constraint
^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from time import sleep
   from lrucache.lru_cache import LRUCache

   timed_lru = LRUCache(maxSize=4, timeout=10)

   timed_lru["a"] = 202
   timed_lru["b"] = 203
   timed_lru["c"] = 204
   timed_lru["d"] = 205
   timed_lru["e"] = 206

   # cache size remains 4, after inserting 5 items into cache.
   print(timed_lru) # LRUCache(timeout=10, size=4, data={'b': 203, 'c': 204, 'd': 205, 'e': 206})

   sleep(60)
   # cache should be empty after 60s as it clears its entry after 10s (timeout)
   timed_lru["d"] = 203
   timed_lru["e"] = 204
   timed_lru["f"] = 205
   timed_lru["g"] = 206
   timed_lru["h"] = 207

   # cache now has new entries
   print(timed_lru) # LRUCache(timeout=10, size=4, data={'e': 204, 'f': 205, 'g': 206, 'h': 207})

   sleep(30)
   # cache entry expires after 10s and as a result we have nothing in the cache (data = {}).
   print(timed_lru) # LRUCache(timeout=10, size=4, data={})
   timed_lru.stop_timer()
