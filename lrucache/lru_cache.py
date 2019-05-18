from collections import MutableMapping
from time import time, sleep

from utils.cache_thread import RLock, StoppableThread
from utils.cache_node import DoublylinkedListNode
from utils.cache_doublylinkedlist import DoublylinkedList


class LRUCache(MutableMapping):
    """Least Recently Used (LRU) cache implementation."""

    def __init__(self, maxSize, timeout = None):
        self.cache = {}
        self.lock = RLock()
        self.timeout = timeout
        self.maxSize = maxSize or 1
        self.currentSize = 0
        self.listOfMostRecent = DoublylinkedList()

    def __getitem__(self, key):
        return self.getValueFromKey(key)
    
    def __setitem__(self, key, value):
        self.insertKeyValuePair(key, value)
    
    def __delitem__(self, key):
        return self.deleteKey(key)

    # O(1) time | 0(1) space
    def insertKeyValuePair(self, key, value):
        try:
            self.lock.acquire()
            if key not in self.cache:
                if self.currentSize == self.maxSize:
                    self.evictLeastRecent()
                else:
                    self.currentSize += 1
                self.cache[key] = DoublylinkedListNode(key, value)
            else:
                self.updateKey(key, value)
            self.updateMostRecent(self.cache[key])
        finally:
            self.lock.release()

    # O(1) time | 0(1) space
    def getValueFromKey(self, key):
        try:
            self.lock.acquire()
            if key not in self.cache:
                return None
            self.updateMostRecent(self.cache[key])
            return self.cache[key].value
        finally:
            self.lock.release()

    # O(1) time | 0(1) space
    def getMostRecentKey(self):
        return self.listOfMostRecent.head.key

    # O(1) time | 0(1) space
    def deleteKey(self, key):
        try:
            self.lock.acquire()
            if key not in self.cache:
                return None
            else:
                node = self.cache[key]
                node.removeBindings()
                del self.cache[key]
                self.currentSize -= 1
                if self.listOfMostRecent.head == self.listOfMostRecent.tail:
                    self.listOfMostRecent.removeTail()
        finally:
            self.lock.release()

    # O(n) time | O(1) space
    def prune(self):
        if not len(self.cache):
            return
        try:
            self.lock.acquire()
            outtime = time() - self.timeout
            tail = self.listOfMostRecent.tail
            while tail and tail.time_created < outtime:
                self.evictLeastRecent()
                tail = self.listOfMostRecent.tail
        finally:
            self.lock.release()

    def evictLeastRecent(self):
        keyToRemove = self.listOfMostRecent.tail.key
        self.listOfMostRecent.removeTail()
        del self.cache[keyToRemove]

    def updateMostRecent(self, node):
        self.listOfMostRecent.setHeadTo(node)

    def updateKey(self, key, value):
        if key not in self.cache:
            raise Exception("The provided key is not in cache")
        self.cache[key].value = value

    def _contents(self, method, *args):
        '''
        common backend for methods:
        keys, values, items, __len__, __contains__, __iter__
        '''
        try:
            self.lock.acquire()
            data = getattr(self.cache, method)(*args)
            return data
        finally:
            self.lock.release()

    def __contains__(self, key):
        return self._contents('__contains__', key)

    has_key = __contains__

    def __len__(self):
        return self._contents('__len__')
    
    def __iter__(self):
        return self._contents('__iter__')

    def keys(self):
        return self._contents('keys')

    def values(self):
        data = self._contents('values')
        return [v.value for v in data]

    def items(self):
        data = self._contents('items')
        return [(k, v.value) for k, v in data]

    def __repr__(self):
        d = dict(self.items())
        return f'{self.__class__.__name__}(timeout={self.timeout}, size={self.maxSize}, data={repr(d)})'


# test implementation
lru = LRUCache(maxSize=4)
lru.insertKeyValuePair("a", 99)

lru["b"] = 202
lru["c"] = 203
lru["d"] = 204
lru["e"] = 205

lru.getValueFromKey("a")
lru.get("a", None)

print(lru)
print(lru.values())

# LRUCache(timeout=None, size=4, data={'b': 202, 'c': 203, 'd': 204, 'e': 205})
# [202, 203, 204, 205]