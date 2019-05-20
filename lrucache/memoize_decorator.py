"""Class decorator defined for LRUCache."""

from types import MethodType

from utils.cache_decorator import Decoratorfunc


class MemoizedCache(Decoratorfunc):
    """Class decorator defined.

    NB: Class decorator applied on a function returns an 
    instance of the decorator class instead of a modified
    function as with function decorators.
    """
    
    def __init__(self, fn, cache, timeout = None):
        self.fn = fn
        self.cache = cache
        self.hits = 0
        self.misses = 0
    
    def reset(self):
        self.hits = 0
        self.misses = 0
    
    def cache_info(self):
        cache_info = f'{self.__class__.__name__}(hits={self.hits}, misses={self.misses}, maxsize={self.cache.maxSize}, currsize={self.cache.currentSize})'
        print(cache_info)

    def __call__(self, *args, **kwargs):

        key = self._convert_call_arguments_to_hash(args, kwargs)

        result = self.cache[key]
        if result is None:
            # We have an entry not in the cache
            self.misses += 1
            result = self.fn(*args, **kwargs)
            self.cache[key] = result
        else:
            self.hits += 1

        return result

    def __get__(self, instance, cls):
        # return a method if it is called on an instance
        return self if instance is None else MethodType(self, instance)

    @staticmethod
    def _convert_call_arguments_to_hash(args, kwargs):
        return hash(str(args) + str(kwargs))
