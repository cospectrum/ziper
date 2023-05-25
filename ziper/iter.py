from __future__ import annotations
import itertools
import more_itertools as mitertools

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
V = TypeVar('V')

Fn = Callable[[T], U]


class Iter(Generic[T]):
    _it: Iterator[T]

    def __init__(self, iterable: Iterable[T]) -> None:
        self._it = iter(iterable)

    def __iter__(self) -> Iterator[T]:
        return self._it

    def __next__(self) -> T:
        return next(self._it)

    def next(self) -> Optional[T]:
        try:
            return next(self)
        except StopIteration:
            return None

    def collect(self, f: Fn[Iterable[T], V]) -> V:
        return f(self)

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

    def step_by(self, step: int) -> Iter[T]:
        return Iter(itertools.islice(self, 0, None, step))

    def take_while(self, predicate: Fn[T, bool]) -> Iter[T]:
        return Iter(itertools.takewhile(predicate, self))

    def skip_while(self, predicate: Fn[T, bool]) -> Iter[T]:
        return Iter(itertools.dropwhile(predicate, self))

    def inspect(self, f: Fn[T, None]) -> Iter[T]:

        def inspector(x: T) -> T:
            f(x)
            return x

        return self.map(inspector)

    def chunks(self, size: int) -> Iter[Iter[T]]:
        it = mitertools.ichunked(self, size)
        return Iter(it).map(lambda chunk: Iter(chunk))
