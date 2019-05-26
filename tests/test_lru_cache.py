import os
import sys
import unittest

from time import sleep

sys.path.insert(0, os.pardir)

from lrucache.lru_cache import LRUCache
from lrucache.memoize_decorator import memoized_cache


alphabetMaps = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "i": 8,
    "j": 9,
}

alphabets = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

def test_lru_of_size(size, testContext):
    
    # Instantiate cache and insert first key.
    lru = LRUCache(size)
    testContext.assertEqual(lru.get_value("a"), None)

    lru.insert_key_value("a", 99)
    testContext.assertEqual(lru.get_most_recent_key(), "a")
    testContext.assertEqual(lru.get_value("a"), 99)

    # Delete a key
    lru.delete_key("a")
    testContext.assertEqual(lru.get_value("a"), None)
    
    # Insert the key back into the cache
    lru.insert_key_value("a", 99)

    # Add existing key when cache isn't full.
    lru.insert_key_value("a", 0)
    testContext.assertEqual(lru.get_most_recent_key(), "a")
    testContext.assertEqual(lru.get_value("a"), 0)

    # Add keys until cache reaches maximum capacity.
    for i in range(1, size):
        mostRecentLetter = alphabets[i - 1]
        testContext.assertEqual(lru.get_most_recent_key(), mostRecentLetter)

        # Test key retrieval when cache isn't full.
        for j in range(0, i):
            letter = alphabets[j]
            testContext.assertEqual(lru.get_value(letter), alphabetMaps[letter])
            testContext.assertEqual(lru.get_most_recent_key(), letter)
        currentLetter = alphabets[i]

        testContext.assertEqual(lru.get_value(currentLetter), None)
        lru.insert_key_value(currentLetter, alphabetMaps[currentLetter])

        testContext.assertEqual(lru.get_most_recent_key(), currentLetter)
        testContext.assertEqual(lru.get_value(currentLetter), alphabetMaps[currentLetter])
    
    # Add keys now that cache is at maximum capacity.
    for i in range(size, len(alphabets)):
        mostRecentLetter = alphabets[i - 1]
        testContext.assertEqual(lru.get_most_recent_key(), mostRecentLetter)

        # Test key retrieval when cache is full.
        for j in range(i - size, i):
            letter = alphabets[j]
            testContext.assertEqual(lru.get_value(letter), alphabetMaps[letter])
            testContext.assertEqual(lru.get_most_recent_key(), letter)

        leastRecentLetter = alphabets[i - size]
        currentLetter = alphabets[i]
        testContext.assertEqual(lru.get_value(currentLetter), None)

        lru.insert_key_value(currentLetter, alphabetMaps[currentLetter])
        testContext.assertEqual(lru.get_most_recent_key(), currentLetter)
        testContext.assertEqual(lru.get_value(currentLetter), alphabetMaps[currentLetter])
        testContext.assertEqual(lru.get_value(leastRecentLetter), None)

    # Add existing keys when cache is full.
    for i in range(len(alphabets) - size, len(alphabets)):
        currentLetter = alphabets[i]
        testContext.assertEqual(lru.get_value(currentLetter), alphabetMaps[currentLetter])

        lru.insert_key_value(currentLetter, (alphabetMaps[currentLetter] + 1) * 100)
        testContext.assertEqual(lru.get_value(currentLetter), (alphabetMaps[currentLetter] + 1) * 100)

def test_lru_with_time_constraint(size, timeout, testContext):
    timed_lru = LRUCache(size, timeout)

    for i in range(0, size):
        alphabet = alphabets[i]
        timed_lru.insert_key_value(alphabet, alphabetMaps[alphabet])

    testContext.assertEqual(len(timed_lru.keys()), size)
    sleep(2)

    testContext.assertEqual(len(timed_lru.keys()), 0)
    timed_lru.stop_timer()

def test_lru_with_memoized_cache(size, testContext):

    @memoized_cache(cache=LRUCache(maxSize=size))
    def get_random(max_value):
        import random
        return random.random() * max_value

    # generate 8 random values
    for idx in range(1, 9):
        get_random(idx)

    testContext.assertEqual(len(get_random.cache), size)


class LRUCacheSizeTestCase(unittest.TestCase):

    def test_size_1(self):
        test_lru_of_size(1, self)

    def test_size_2(self):
        test_lru_of_size(2, self)

    def test_size_3(self):
        test_lru_of_size(3, self)

    def test_size_4(self):
        test_lru_of_size(4, self)

    def test_size_5(self):
        test_lru_of_size(5, self)

    def test_size_6(self):
        test_lru_of_size(6, self)

    def test_size_7(self):
        test_lru_of_size(7, self)

    def test_size_8(self):
        test_lru_of_size(8, self)

    def test_size_9(self):
        test_lru_of_size(9, self)

    def test_size_10(self):
        test_lru_of_size(10, self)


class LRUTimeConstraintTestCase(unittest.TestCase):

    def test_time_constraint_1_sec_size_5(self):
        test_lru_with_time_constraint(5, 1, self)

    def test_time_constraint_1_sec_size_10(self):
        test_lru_with_time_constraint(10, 1, self)


class LRUMemoizationTestCase(unittest.TestCase):
    def test_memoization(self):
        test_lru_with_memoized_cache(5, self)


if __name__ == "__main__":
    unittest.main()
