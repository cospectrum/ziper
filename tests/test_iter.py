import random

from ziper import Iter

from typing import (
    Callable,
    Iterable,
    Iterator,
    List,
    Optional,
)


def test_readme() -> None:
    xs = ['1', '2', 'a', '3', '4', 'b', 'c']
    ys = [6, 7, 8, 9]

    result = list(
        Iter(xs)
        .filter(lambda x: x.isdecimal())
        .map(int)
        .chain(ys)
        .filter(lambda x: x % 2 == 0)
    )
    assert result == [2, 4, 6, 8]


def test_loop() -> None:

    def for_loop(it: Iterable[int]) -> List[int]:
        result = []
        for x in it:
            result.append(x)
        return result

    xs = [1, 2, 3]
    it = Iter(xs)
    result = for_loop(it)
    assert result == xs
    assert it.next() is None

    it = Iter(xs)
    iterator = iter(it)
    result = for_loop(iterator)
    assert result == xs
    assert it.next() is None


def test_map() -> None:
    iterable: List[int] = [1, 2, 3]
    it: Iterator[int] = iter(iterable)
    int_iter: Iter[int] = Iter(it)

    f: Callable[[int], str] = str
    str_iter: Iter[str] = int_iter.map(f)

    first: Optional[str] = str_iter.next()
    assert first == '1'
    assert str_iter.next() == '2'
    assert str_iter.next() == '3'
    assert str_iter.next() is None


def test_nth() -> None:
    stop = random.randint(0, 10)
    xs = range(stop)
    n = random.randint(0, stop)
    assert Iter(xs).nth(n) == n
