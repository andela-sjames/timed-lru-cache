import threading

from collections import MutableMapping
from time import time

from utils.cache_doublylinkedlist import DoublylinkedList
from utils.cache_node import DoublylinkedListNode
from utils.cache_thread import RLock


class LRUCache(MutableMapping):
    """Timed Least Recently Used (LRU) cache implementation.

    TL;DR:
    The timed LRUCache is a dict-like container that is also size limited.
    It uses the prune method when instantiated with time to remove
    time expired objects.

    Timed LRUCache:
    All objects on creation have a timestamp on it, this timestamp is used
    to check for expired objects when a timeout is given,
    the prune method is called and runs periodically in a thread
    to do cleanups.

    Items are kept in a dict but are also mutually linked to
    each other in sequence of their last access time.

    Access to single items, deletion, and update is done in constant time O(1)

    The size limit, when exceeded will cause the oldest among the
    not yet expired items to be kicked out of the cache.
    """

    def __init__(self, maxSize, timeout=None):
        self.cache = {}
        self.lock = RLock()
        self.timeout = timeout
        self.maxSize = maxSize or 1
        self.currentSize = 0
        self.list_of_most_recent = DoublylinkedList()
        self.timer = None

        if self.timeout:
            self._cleanup()

    def __getitem__(self, key):
        return self.get_value(key)

    def __setitem__(self, key, value):
        self.insert_key_value(key, value)

    def __delitem__(self, key):
        return self.delete_key(key)

    # O(1) time | 0(1) space
    def insert_key_value(self, key, value):
        try:
            self.lock.acquire()
            if key not in self.cache:
                if self.currentSize == self.maxSize:
                    self._evict_least_recent()
                else:
                    self.currentSize += 1
                self.cache[key] = DoublylinkedListNode(key, value)
            else:
                self._update_key(key, value)
            self._update_most_recent(self.cache[key])
        finally:
            self.lock.release()

    # O(1) time | 0(1) space
    def get_value(self, key):
        try:
            self.lock.acquire()
            if key not in self.cache:
                return None
            self._update_most_recent(self.cache[key])
            return self.cache[key].value
        finally:
            self.lock.release()

    # O(1) time | 0(1) space
    def get_most_recent_key(self):
        return self.list_of_most_recent.head.key

    # O(1) time | 0(1) space
    def delete_key(self, key):
        try:
            self.lock.acquire()
            if key not in self.cache:
                return None
            else:
                node = self.cache[key]
                node.remove_bindings()
                del self.cache[key]
                self.currentSize -= 1
                head = self.list_of_most_recent.head
                tail = self.list_of_most_recent.tail
                if head == tail:
                    self.list_of_most_recent.remove_tail()
        finally:
            self.lock.release()

    # O(n) time | O(1) space
    def _prune(self):
        if not len(self.cache):
            return
        try:
            self.lock.acquire()
            outtime = time() - self.timeout
            tail = self.list_of_most_recent.tail
            while tail and tail.time_created < outtime:
                self._evict_least_recent()
                self.currentSize -= 1
                tail = self.list_of_most_recent.tail
        finally:
            self.lock.release()

    def _evict_least_recent(self):
        key_to_remove = self.list_of_most_recent.tail.key
        self.list_of_most_recent.remove_tail()
        del self.cache[key_to_remove]

    def _update_most_recent(self, node):
        self.list_of_most_recent.set_head_to(node)

    def _update_key(self, key, value):
        if key not in self.cache:
            raise Exception("The provided key is not in cache")
        self.cache[key].value = value

    def _cleanup(self):
        self._prune()
        timer = threading.Timer(self.timeout, self._cleanup)
        timer.start()
        self.timer = timer

    def stop_timer(self):
        self.timer.cancel()

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
        classname = self.__class__.__name__
        timeout = f'timeout={self.timeout}'
        size = f'size={self.maxSize}'
        data = f'data={repr(d)}'
        return f'{classname}({timeout}, {size}, {data})'
