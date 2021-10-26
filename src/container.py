"""
Container implementation of https://mostly-adequate.gitbook.io/mostly-adequate-guide/ch08...
"""

from typing import Any, Callable


class Container:

    def __init__(self, value: Any):
        self.value = value

    @staticmethod
    def of(value: Any) -> 'Container':
        return Container(value)

    def map(self, method: Callable) -> 'Container':
        return Container.of(method(self.value))
