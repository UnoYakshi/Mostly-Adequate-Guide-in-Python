"""
Implementation reference: https://github.com/fantasyland/fantasy-land
"""

from typing import Any, Callable
from src.support import compose


def identity(x):
    return x


class Monad:
    @property
    def name(self):
        return self.__class__.__name__

    def __init__(self, value: Any):
        self.value = value

    def __repr__(self):
        return f'{self.name}({self.value})'

    def __str__(self):
        return f'{self.name}({self.value})'


class Container(Monad):

    @staticmethod
    def of(value: Any) -> 'Container':
        return Container(value)

    def map(self, method: Callable) -> 'Container':
        return Container.of(method(self.value))


class Either(Monad):

    @staticmethod
    def of(value: Any) -> 'Correct':
        return Correct(value)


class Correct(Either):
    def is_correct(self):
        return True

    @staticmethod
    def of(value: Any):
        raise Exception(f'`of` called on class Correct({value}) instead of Either(type)...')

    def map(self, fn: Callable):
        return Either.of(fn(self.value))

    def ap(self, f: 'Functor'):
        return f.map(self.value)

    def chain(self, fn: Callable):
        return fn(self.value)

    def join(self):
        return self.value

    def sequence(self, of):
        return self.traverse(of, identity)

    # TODO: What's `of` here?
    def traverse(self, of, fn):
        fn(self.value).map(Either.of)


class Incorrect(Either):

    def is_correct(self):
        return False

    def of(self, value: Any):
        raise Exception(f'`of` called on class Incorrect({value}) instead of Either(type)')

    def map(self):
        return self

    def ap(self):
        return self

    def chain(self):
        return self

    def join(self):
        return self

    def sequence(self, of):
        return of(self)


class Identity:

    def __init__(self, value: Any):
        self.value = value

    @staticmethod
    def of(value: Any) -> 'Identity':
        return Identity(value)

    def map(self, method: Callable) -> 'Identity':
        return Identity.of(method(self.value))

    def ap(self, f):
        return f.map(self.value)

    def chain(self, method: Callable):
        return self.map(method).join()

    def join(self):
        return self.value

    def sequence(self, of):
        return self.traverse(of, identity)

    # TODO: What's `of` here?
    def traverse(self, of, method: Callable):
        return method(self.value).map(Identity.of)


class IO:

    def __init__(self, method: Callable):
        self.__unsafe_perform_io = method

    def of(self, value: Any) -> 'IO':
        return IO(lambda _: value)

    def map(self, method: Callable):
        return IO(compose(method, self.__unsafe_perform_io))

    def ap(self, f):
        return self.chain(lambda method: f.map(method))

    def chain(self, method: Callable):
        return self.map(method).join()

    def join(self):
        return IO(lambda _: self.__unsafe_perform_io().__unsafe_perform_io())

    def execute_effect(self, *args, **kwargs):
        self.__unsafe_perform_io(*args, **kwargs)


class Maybe(Monad):
    @staticmethod
    def of(value: Any) -> 'Maybe':
        return Maybe(value)

    @property
    def name(self):
        return 'Nothing' if self.is_nothing else 'Just'

    @property
    def is_nothing(self):
        return self.value is None

    @property
    def is_just(self):
        return not self.is_nothing

    def map(self, method: Callable):
        return self if self.is_nothing else Maybe.of(method(self.value))

    def ap(self, f):
        return self if self.is_nothing else f.map(self.value)

    def chain(self, method: Callable):
        return self.map(method).join()

    def join(self):
        return self if self.is_nothing else self.value

    def sequence(self, of):
        return self.traverse(of, identity)

    def traverse(self, of, method: Callable):
        return of(self) if self.is_nothing else method(self.value).map(Maybe.of)
