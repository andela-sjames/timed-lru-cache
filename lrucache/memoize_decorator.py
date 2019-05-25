"""Class decorator defined for LRUCache."""

from types import MethodType

from .utils.cache_decorator import Decoratorfunc


class memoized_cache(Decoratorfunc):
    """Class decorator defined.

    NB: Callable class decorator applied on a function returns an
    instance of the decorator class instead of a modified
    function as with function decorators.

    Attributes:
        func: The decorated function.
        cache: An instance of the LRUCache.
        hits: The number of times a cache value is used.
        misses: The number of times a cache value is not used.
    """

    def __init__(self, func, cache):
        self.func = func
        self.cache = cache
        self.hits = 0
        self.misses = 0

    def reset(self):
        """Set the counts to zero."""
        self.hits = 0
        self.misses = 0

    def cache_info(self):
        """Return the basic cache info."""
        class_name = self.__class__.__name__
        hits = f'hits={self.hits}'
        misses = f'misses={self.misses}'
        maxsize = f'maxsize={self.cache.maxSize}'
        currsize = f'currsize={self.cache.currentSize}'
        cache_info = f'{class_name}({hits}, {misses}, {maxsize}, {currsize})'
        print(cache_info)

    def __call__(self, *args, **kwargs):

        key = self._convert_call_arguments_to_hash(args, kwargs)

        result = self.cache[key]
        if result is None:
            # We have an entry not in the cache
            self.misses += 1
            result = self.func(*args, **kwargs)
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
