from typing import Any, Callable, Union


def named_as(val: Any, fn: Callable):
    setattr(fn, '__name__', val)
    return fn


def curry(fn: Callable) -> Callable:
    """
    The concept is simple: You can call a function with fewer arguments than it expects.
    It returns a function that takes the remaining arguments.

    Reference: https://www.python-course.eu/currying_in_python.php

    :param fn: The method to curry...
    :return: Curried [given] method...
    """

    # To keep the name of the curried function...
    curry.__curried_func_name__ = fn.__name__
    amount = fn.__code__.co_argcount

    def f(*args, **kwargs):
        if args or kwargs:

            def inner(_fn):
                return lambda *_args, **_kwargs: _fn(*[*args, *_args], **{**kwargs, **_kwargs})

            if amount == 0 and len(args) > 0:
                return lambda *_args, **_kwargs: inner(f if len(_args) > 0 else fn)(*_args, **_kwargs)

            if len(args) >= amount:
                return fn(*args, **kwargs)

            return inner(f)

        return fn(*args, **kwargs)

    return f


def compose(*functions):
    def inner(arg):
        for f in reversed(functions):
            arg = f(arg)
        return arg
    return inner


def pipe(*functions):
    """Works as `compose()` but with direct order..."""
    def inner(arg):
        for f in functions:
            arg = f(arg)
        return arg
    return inner


def g(property_name: Union[str, int], obj: Any) -> Any:
    try:
        if property_name in obj:
            return obj[property_name]

        if isinstance(obj, list) and len(obj) > property_name:
            return obj[property_name]
    except TypeError:
        ...

    # return None
    return getattr(obj, property_name)


prop = curry(g)

# def prop(name: str) -> Callable:
#     def inner(obj: object) -> Any:
#         return getattr(obj, name)
#     return inner
