"""Decorator class defined for class init."""


class Decoratorfunc(object):
    """Give decoration function precedence.
    
    Allow decorator function to be first the argument to
    class constructor, this argument will be passed to the
    __call__() method implicitly.

    https://docs.python.org/3/reference/datamodel.html#basic-customization
    """
    def __new__(cls, *attr_args, **attr_kwargs):
        def decorator(decorator_func):
            instance = object.__new__(cls)
            instance.__init__(decorator_func, *attr_args, **attr_kwargs)
            return instance
        
        return decorator
