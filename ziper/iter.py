from __future__ import annotations
import itertools

from typing import (
    Iterable,
    Iterator,
    Generic,
    Optional,
    TypeVar,
    Tuple,
    Callable,
)


T = TypeVar('T')
U = TypeVar('U')

Fn = Callable[[T], U]


class Iter(Generic[T]):
    it: Iterator[T]

    def __init__(self, iterable: Iterable[T]) -> None:
        self.it = iter(iterable)

    def __iter__(self) -> Iterator[T]:
        return self.it

    def __next__(self) -> T:
        return next(self.it)

    def next(self) -> Optional[T]:
        try:
            return next(self)
        except StopIteration:
            return None

    def map(self, f: Fn[T, U]) -> Iter[U]:
        return Iter(map(f, self))

    def filter(self, f: Fn[T, bool]) -> Iter[T]:
        return Iter(filter(f, self))

    def zip(self, other: Iterable[U]) -> Iter[Tuple[T, U]]:
        return Iter(zip(self, other))

    def chain(self, other: Iterable[T]) -> Iter[T]:
        return Iter(itertools.chain(self, other))

    def fold(self, init: U, f: Callable[[U, T], U]) -> U:
        accum = init
        for x in self:
            accum = f(accum, x)
        return accum

    def reduce(self, f: Callable[[T, T], T]) -> Optional[T]:
        first: T
        try:
            first = next(self)
        except StopIteration:
            return None
        return self.fold(first, f)

    def cycle(self) -> Iter[T]:
        return Iter(itertools.cycle(self))

    def take(self, n: int) -> Iter[T]:
        return Iter(itertools.islice(self, n))

    def skip(self, n: int) -> Iter[T]:
        return Iter(itertools.islice(self, n, None))

    def enumerate(self) -> Iter[Tuple[int, T]]:
        return Iter(enumerate(self))

    def count(self) -> int:
        accum = 0
        for _ in self:
            accum += 1
        return accum

    def position(self, predicate: Fn[T, bool]) -> Optional[int]:
        for index, x in self.enumerate():
            if predicate(x):
                return index
        return None

    def find(self, predicate: Fn[T, bool]) -> Optional[T]:
        for x in self:
            if predicate(x):
                return x
        return None

    def all(self, predicate: Fn[T, bool]) -> bool:
        for x in self:
            if not predicate(x):
                return False
        return True

    def any(self, predicate: Fn[T, bool]) -> bool:
        for x in self:
            if predicate(x):
                return True
        return False

    def last(self) -> Optional[T]:
        accum = None
        for x in self:
            accum = x
        return accum

    def nth(self, n: int) -> Optional[T]:
        return self.skip(n).next()

    def for_each(self, f: Fn[T, None]) -> None:
        for x in self:
            f(x)
