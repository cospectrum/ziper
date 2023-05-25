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


def test_types() -> None:
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
    stop = random.randint(1, 10)
    xs = range(stop)
    n = random.randint(0, stop - 1)
    assert Iter(xs).nth(n) == n


def test_step_by() -> None:
    a = [0, 1, 2, 3, 4, 5]
    iter = Iter(a).step_by(2)

    assert iter.next() == 0
    assert iter.next() == 2
    assert iter.next() == 4
    assert iter.next() is None


def test_take() -> None:
    a = [1, 2, 3]

    iter = Iter(a).take(2)

    assert iter.next() == 1
    assert iter.next() == 2
    assert iter.next() is None


def test_skip() -> None:
    a = [1, 2, 3]

    iter = Iter(a).skip(2)

    assert iter.next() == 3
    assert iter.next() is None


def test_reduce() -> None:
    reduced = Iter(range(1, 10)).reduce(lambda acc, e: acc + e)
    assert reduced == 45

    folded = Iter(range(1, 10)).fold(0, lambda acc, e: acc + e)
    assert reduced == folded


def test_fold() -> None:
    numbers = [1, 2, 3, 4, 5]

    result = Iter(numbers).fold('0', lambda acc, x: (
        f'({acc} + {x})'
    ))

    assert result == '(((((0 + 1) + 2) + 3) + 4) + 5)'


def test_all() -> None:
    a = [1, 2, 3]

    assert Iter(a).all(lambda x: x > 0)
    assert not Iter(a).all(lambda x: x > 2)


def test_any() -> None:
    a = [1, 2, 3]

    assert Iter(a).any(lambda x: x > 0)
    assert not Iter(a).any(lambda x: x > 5)


def test_skip_while() -> None:
    a = [-1, 0, 1]

    iter = Iter(a).skip_while(lambda x: x < 0)

    assert iter.next() == 0
    assert iter.next() == 1
    assert iter.next() is None


def test_take_while() -> None:
    a = [-1, 0, 1]

    iter = Iter(a).take_while(lambda x: x < 0)

    assert iter.next() == -1
    assert iter.next() is None
