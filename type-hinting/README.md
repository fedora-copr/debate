# Type Hinting

Author: [@FrostyX](https://github.com/frostyx)

This is not a case against type hinting (static types), this is a case
against over-using them.

## Good motivations

- Type hints nicely complement docstrings. Docstrings are great for
  describing the purpose of a function (or class, file) but they suck
  for describing their arguments and return value types because they
  can be untrue. Type hints nicely complement this.
- Type hints can reveal some errors


## Bad motivations

### A bulletproof solution

Static types are not a bulletproof solution for revealing type-related
bugs. IIRC some study found that ~80% of type-related errors are
caused by `None` and Mypy won't save us there - it can find many
issues, but I can still introduce tracebacks or unexpected bugs that
Mypy doesn't warn about:

Produces traceback:

```python
def hello(user: Optional[User]) -> str:
    return "Hello " + getattr(user, "name")

print(hello(None))
```

Returns `Hello None`:

```python
def hello(user: Optional[User]) -> str:
    return "Hello {0}".format(user)

print(hello(None))
```

Produces traceback:

```python
def hello(user: dict) -> str:
    return "Hello {0}".format(user["name"])

print(hello({}))
```

### Performance

Type hinting in python
[doesn't bring any performance improvements][mypy-performance],
it is used merely for linting.


## Disadvantages

### One does not simply know the type

_Insert the Boromir meme_

Duck typing is IMHO one of the best Python features ...
Normally, we are not required to know and say exactly what type is
expected but rather how it is supposed to behave.

I may intend to write a function that filters a list somehow:

```python
def odd(numbers: list):
    return [x for x in numbers if x%2 == 0]
```

And expect the following usage

```python
print(odd([1, 2, 3, 4]))
```

Later, somebody want to use

```python
print(odd(range(1, 5)))
print(odd(reversed([1, 2, 3, 4])))
```

and Mypy complains.


### Too much clutter

Consider the following code (simplified version from `copr-common`)

```python
SLEEP_INCREMENT_TIME = 1

def send_request_repeatedly(url, method=None, data=None, timeout=3):
    sleep = SLEEP_INCREMENT_TIME
    start = time.time()
    stop = start + timeout

    i = 0
    while True:
        i += 1
        if time.time() > stop:
            return

        # Sending the request, and failing
        print("Attempt #{0} to {1}: {2}".format(i, method or "GET", url))

        time.sleep(sleep)
        sleep += SLEEP_INCREMENT_TIME

send_request_repeatedly("http://example.foo")
```

Now the same code with 100% adherence to static typing

```python
SLEEP_INCREMENT_TIME: int = 1

def send_request_repeatedly(url: str, method: Optional[str] = None,
                            data: Optional[dict] = None, timeout: int = 3,
                            ) -> None:
    sleep: int = SLEEP_INCREMENT_TIME
    start: float = time.time()
    stop: float = start + timeout

    i: int = 0
    while True:
        i += 1
        if time.time() > stop:
            return

        # Sending the request, and failing
        print("Attempt #{0} to {1}: {2}".format(i, method or "GET", url))

        time.sleep(sleep)
        sleep += SLEEP_INCREMENT_TIME

send_request_repeatedly("http://example.foo")
```

I would argue that the code readability is **much** worse.


## My proposal

Let's use static types only when it makes sense.

- Optionally for public functions, public methods, and class
  constructors, but not require them

And avoid using them for:

- Private functions and private methods (starting with and underscore)
- Local variables
- Inside tests
- When types are already defined by something else (`argparse`,
  `click`, SQLAlchemy models, etc)




[mypy-performance]: https://mypy.readthedocs.io/en/stable/faq.html#will-static-typing-make-my-programs-run-faster
