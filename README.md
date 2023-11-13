# ziper
[![github]](https://github.com/cospectrum/ziper)

[github]: https://img.shields.io/badge/github-cospectrum/ziper-8da0cb?logo=github

Rust-like iterator for Python

## Install

```sh
pip install ziper
```

## Usage

```py
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
```
