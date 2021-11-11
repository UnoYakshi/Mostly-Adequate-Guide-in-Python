"""
The base algebraic structures defined in https://github.com/fantasyland/fantasy-land.

Scheme: https://raw.githubusercontent.com/fantasyland/fantasy-land/master/figures/dependencies.png.
"""

from __future__ import annotations

from typing import Any, Callable


class Base:
    """The base class for all algebraic structures..."""

    def __init__(self, value: Any):
        self.value = value

    @property
    def name(self):
        return self.__class__.__name__

    def __repr__(self):
        return f'{self.name}({self.value})'

    def __str__(self):
        return f'{self.name}({self.value})'


class Functor(Base):
    """Properties: identity, composition."""

    def map(self, method: Callable) -> Functor:
        return Functor(method(self.value))


class Contravariant(Base):
    def contramap(self, method: Callable) -> Contravariant:
        ...


class Apply(Functor):
    def ap(self, f: Functor):
        return f.map(self.value)


class Applicative(Apply):
    def of(self, value: Any):
        return self.__init__(value)


class Chain(Apply):
    def chain(self, method: Callable) -> Chain:
        return method(self.value)


class Foldable(Base):
    def reduce(self, f, x):
        raise NotImplementedError


class Traversable(Foldable):
    def traverse(self, obj: Applicative, method: Traversable) -> Applicative:
        return method(self.value).map(obj.of)


class Alt(Functor):
    def alt(self, f: Functor) -> Alt:
        raise NotImplementedError


class Plus(Alt):
    def zero(self) -> Plus:
        raise NotImplementedError


class Alternative(Plus, Applicative):
    def ap(self, f: Functor):
        ...


class Monad(Applicative, Chain):
    """Left identity, right identity."""
    pass


class Extend(Functor):
    def extend(self, method: Callable) -> Extend:
        """

        :param method: Should return `type(self.value)`...
        :return:
        """
        raise NotImplementedError


class Comonad(Extend):
    def extract(self) -> Any:
        return self.value
