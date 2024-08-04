# Pattern Matching

Pattern matching is a new feature in Python 3.10
https://peps.python.org/pep-0636/

Example:

```python
def length(items):
    match items:
        case []: return 0
        case [x, *xs]: return 1 + length(xs)
```

I don't have a specific use case for pattern matching in Copr, this is just a
general research document.


## Exhaustive Pattern Matching

### Prerequisites

Create a `pyproject.toml` file with this minimal configuration

```
[tool.pyright]
typeCheckingMode = "strict"
```

Install `pyright`. You will have to use `pip` because it is not available in
Fedora.

```
pip install --user pyright
```

#### Code

```python
from enum import Enum

class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2

def print_color(color: Color):
    match color:
        case Color.RED:
            print("I see red!")
        case Color.GREEN:
            print("Grass is green")
```

Run:

```
$ ~/.local/bin/pyright
/home/jkadlcik/python-pattern-matching/pattern-matching.py
  /home/jkadlcik/python-pattern-matching/pattern-matching.py:9:11 - error: Cases within match statement do not exhaustively handle all values
    Unhandled type: "Literal[Color.BLUE]"
    If exhaustive handling is not intended, add "case _: pass" (reportMatchNotExhaustive)
1 error, 0 warnings, 0 informations
```

Unfortunatelly, there is not yet support for exhaustiveness check in `mypy`
and `ruff`.


## Matching Enums

See the code above


## Matching type unions

```python
def hello(username: str | None):
    match username:
        case str(x): print(f"Hello {x}")
        case None: print("Hello anonymous")
```


## Matching custom types

```python
from dataclasses import dataclass
from typing import TypeAlias


@dataclass
class Createrepo:
    fullname: str


@dataclass
class DeleteBuild:
    fullname: str
    build_id: int


@dataclass
class Fork:
    src: str
    dst: str


Action: TypeAlias = Createrepo | DeleteBuild | Fork


def run(action: Action):
    match action:
        case Createrepo(fullname):
            print(f"Regenerating repository for {fullname}")

        case DeleteBuild(fullname, build_id):
            print(f"Deleting #{build_id} in {fullname}")

        case Fork(src, dst):
            print(f"Forking {src} into {dst}")


action = Createrepo("frostyx/foo")
run(action)

action = DeleteBuild("frostyx/foo", 123456)
run(action)

action = Fork("frostyx/foo", "frostyx/bar")
run(action)
```

## Matching typed dicts

TODO https://typing.readthedocs.io/en/latest/spec/typeddict.html#typeddict


## Resources

- https://dogweather.dev/2022/10/03/i-discovered-that-python-now-can-do-true-match-exhaustiveness-checking/
- https://github.com/dogweather/python-exhaustiveness-adts-monads/tree/master
- https://guide.elm-lang.org/types/custom_types
