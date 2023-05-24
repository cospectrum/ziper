# ziper

Rust-like iterator for Python


## Install

From PyPI:
```sh
pip install ziper
```

From git:
```sh
pip install git+https://github.com/cospectrum/ziper.git
```

## Usage

```py
from ziper import Iter

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
```
