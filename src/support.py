from functools import partial, wraps
from typing import Any, Callable


def named_as(val: Any, fn: Callable):
    setattr(fn, '__name__', val)
    return fn


# def curry(fn: Callable):
#     arity = len(fn)
#     return named_as(fn.__name__, lambda x: curry(*args))


def curry_man(method: Callable) -> Callable:
    ...


def curry(fn: Callable) -> Callable:
    """
    The concept is simple: You can call a function with fewer arguments than it expects.
    It returns a function that takes the remaining arguments.

    Reference: https://www.python-course.eu/currying_in_python.php

    :param fn:
    :return:
    """

    # To keep the name of the curried function...
    curry.__curried_func_name__ = fn.__name__
    f_args, f_kwargs = [], {}
    amount = fn.__code__.co_argcount
    real_amount = 0

    @wraps(fn)
    def f(*args, **kwargs):
        nonlocal f_args, f_kwargs, real_amount
        if args or kwargs:
            f_args += args
            f_kwargs.update(kwargs)
            real_amount += len(args)

            if real_amount >= amount:
              return fn(*f_args, *f_kwargs)
            else:
              return f
        else:
            result = fn(*f_args, *f_kwargs)
            f_args, f_kwargs = [], {}
            return result

    return f


def curry2(func):
    """Curries func into a chain of one argument functions."""
    n = func.__code__.co_argcount

    if n <= 1:
        return func
    elif n == 2:
        return lambda x: lambda y: func(x, y)
    else:
        return lambda x: curry(partial(func, x), n - 1)


def compose(*functions):
    def inner(arg):
        for f in reversed(functions):
            arg = f(arg)
        return arg
    return inner


prop = curry(lambda p, obj:  getattr(obj, p))
# prop = lambda p: curry(lambda obj:  getattr(obj, p))


# def prop(name: str) -> Callable:
#     def inner(obj: object) -> Any:
#         return getattr(obj, name)
#     return inner
