"""
Container implementation of https://mostly-adequate.gitbook.io/mostly-adequate-guide/ch08...
"""

from typing import Any, Callable

from src.support import compose

identity = lambda x: x


class Container:

    def __init__(self, value: Any):
        self.value = value

    @staticmethod
    def of(value: Any) -> 'Container':
        return Container(value)

    def map(self, method: Callable) -> 'Container':
        return Container.of(method(self.value))


class Either:
    def __init__(self, value: Any):
        self.value = value

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
        self.unsafe_perform_io = method

    def of(self, value: Any) -> 'IO':
        return IO(lambda _: value)

    def map(self, method: Callable):
        return IO(compose(method, self.unsafe_perform_io))

    def ap(self, f):
        return self.chain(lambda method: f.map(method))

    def chain(self, method: Callable):
        return self.map(method).join()

    def join(self):
        return IO(lambda _: self.unsafe_perform_io().unsafe_perform_io())


class Maybe:

    def __init__(self, value: Any):
        self.value = value

    @staticmethod
    def of(value: Any) -> 'Maybe':
        return Maybe(value)

    def is_nothing(self):
        return not self.value

    def is_just(self):
        return not self.is_nothing()

    def map(self, method: Callable):
        return self if self.is_nothing() else Maybe.of(method(self.value))

    def ap(self, f):
        return self if self.is_nothing() else f.map(self.value)

    def chain(self, method: Callable):
        return self.map(method).join()

    def join(self):
        return self if self.is_nothing() else self.value

    def sequence(self, of):
        return self.traverse(of, identity)

    def traverse(self, of, method: Callable):
        return of(self) if self.is_nothing() else method(self.value).map(Maybe.of)
