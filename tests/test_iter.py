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
    from ziper import Iter

    xs = ['1', '2', 'a', '3', '4', 'b', 'c']
    ys = [6, 7, 8, 9]

    evens: list = (
        Iter(xs)
        .filter(lambda x: x.isdecimal())
        .map(int)
        .chain(ys)
        .filter(lambda x: x % 2 == 0)
        .collect(list)
    )
    assert evens == [2, 4, 6, 8]


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

    assert isinstance(int_iter, Iterator)
    assert isinstance(int_iter, Iterable)

    f: Callable[[int], str] = str
    str_iter: Iter[str] = int_iter.map(f)

    first: Optional[str] = str_iter.next()
    assert first == '1'
    assert str_iter.next() == '2'
    assert str_iter.next() == '3'
    assert str_iter.next() is None


def test_nth() -> None:
    a = [1, 2, 3]
    it = Iter(a)
    assert it.nth(1) == 2
    assert it.nth(1) is None

    assert Iter(a).nth(10) is None

    stop = random.randint(1, 10)
    xs = range(stop)
    n = random.randint(0, stop - 1)
    assert Iter(xs).nth(n) == n


def test_step_by() -> None:
    a = [0, 1, 2, 3, 4, 5]
    it = Iter(a).step_by(2)

    assert it.next() == 0
    assert it.next() == 2
    assert it.next() == 4
    assert it.next() is None


def test_take() -> None:
    a = [1, 2, 3]

    it = Iter(a).take(2)

    assert it.next() == 1
    assert it.next() == 2
    assert it.next() is None


def test_skip() -> None:
    a = [1, 2, 3]

    it = Iter(a).skip(2)

    assert it.next() == 3
    assert it.next() is None


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

    it = Iter(a).skip_while(lambda x: x < 0)

    assert it.next() == 0
    assert it.next() == 1
    assert it.next() is None


def test_take_while() -> None:
    a = [-1, 0, 1]

    it = Iter(a).take_while(lambda x: x < 0)

    assert it.next() == -1
    assert it.next() is None


def test_chunks() -> None:
    data = [1, 1, 2, -2, 6, 0, 3, 1]

    for chunk in Iter(data).chunks(3):
        assert isinstance(chunk, Iter)
        assert sum(chunk) == 4

    chunks = Iter(data).chunks(3)
    assert chunks.next().collect(list) == [1, 1, 2]  # type: ignore
    assert chunks.next().collect(list) == [-2, 6, 0]  # type: ignore
    assert chunks.next().collect(list) == [3, 1]  # type: ignore
    assert chunks.next() is None


def test_find_position() -> None:
    text = 'Ha'
    it = Iter(text).find_position(lambda ch: ch.islower())
    assert it == (1, 'a')


def test_positions() -> None:
    data = [1, 2, 3, 3, 4, 6, 7, 9]
    it = Iter(data).positions(lambda x: x % 2 == 0)
    assert list(it) == [1, 4, 5]

    v: list = Iter(data).positions(lambda x: x % 2 == 1).collect(list)
    assert list(reversed(v)) == [7, 6, 3, 2, 0]


def test_find_positions() -> None:
    data = [1, 2, 3, 3, 4, 6, 7, 9]

    def tuples(indexes):
        return [(i, data[i]) for i in indexes]

    it = Iter(data).find_positions(lambda x: x % 2 == 0)
    assert list(it) == tuples([1, 4, 5])

    v: list = Iter(data).find_positions(lambda x: x % 2 == 1).collect(list)
    assert list(reversed(v)) == tuples([7, 6, 3, 2, 0])


def test_cartesian_product() -> None:
    v: list = Iter(range(2)).cartesian_product('ab').collect(list)
    assert isinstance(v[0], tuple)
    assert v == [(0, 'a'), (0, 'b'), (1, 'a'), (1, 'b')]
