# wrapper‑utils

A tiny collection of useful Python decorators:

* **`repeat`** – run a function *n* times.
* **`threaded_repeat`** – run a function *n* times in a thread pool.
* **`catch`** – catch selected exceptions and optionally handle them.
* **`timeit`** – measure execution time and optionally forward the result to a handler.
* **`decorator`** – turn a regular function with extra parameters into a full-featured decorator, preserving metadata automatically.

The library has **no external runtime dependencies** except for the standard library and **NumPy** (used only for the fast `np.arange` loop).

---

## 📦 Installation

```bash
pip install git+https://github.com/ProdDanny03/wrapper-utils.git
```

> The package is not published on PyPI yet, so the above *editable* install pulls the latest code directly from GitHub.

---

## 🚀 Quick start

```python
from wrapper_utils import repeat, threaded_repeat, catch, timeit
import numpy as np
```

### 2️⃣ `decorator`

```python
from wrapper_utils import decorator

@decorator
def something(func, x=3, y="hello", z=[1, 2, 3]):
    print(f"x={x}, y={y}, z={z}")
    result = func()
    print("done")
    return result

@something                    # uses default parameters
def greet1():
    print("hi1")

@something(x=10, y="world")   # overrides defaults
def greet2():
    print("hi2")

greet1()
# Output:
# x=3, y=hello, z=[1, 2, 3]
# hi1
# done

greet2()
# Output:
# x=10, y=world, z=[1, 2, 3]
# hi2
# done
```

*If using mutable defaults like lists, consider using None and initializing inside the function to avoid shared state:*

```python
@decorator
def something(func, z=None):
    if z is None:
        z = [1, 2, 3]
```

---

### 1️⃣ `repeat`

```python
@repeat(n=3)                     # will call `greet` three times
def greet(name: str):
    print(f"Hello, {name}!")

greet("Alice")
# Output:
# Hello, Alice!
# Hello, Alice!
# Hello, Alice!
```

*If `n` is omitted, the default is `1`.*

---

### 2️⃣ `threaded_repeat`

```python
@threaded_repeatn(n=5)           # 5 executions, spread out between threads
def heavy_computation(x):
    return np.sqrt(x)

future = heavy_computation(16)   # returns a `concurrent.futures.Future`
print(future.result())           # -> 4.0 (the result of the *last* call)
```

*You can provide your own executor:*

```python
from concurrent.futures import ProcessPoolExecutor

my_pool = ProcessPoolExecutor(max_workers=4)

@threaded_repeat(n=2, executor=my_pool)
def cpu_bound(y):
    return sum(range(y))

future = cpu_bound(1_000_000)
print(future.result())
```

---

### 3️⃣ `catch`

```python
@catch(exception=ZeroDivisionError, silent=True)
def divide(a, b):
    return a / b

print(divide(1, 0))   # silently returns None instead of raising
```

*Custom handler example:*

```python
def log_error(exc):
    print(f"[ERROR] {exc}")

@catch(exception=ValueError, handler=log_error)
def parse_int(s):
    return int(s)

parse_int("not-an-int")
# Output: [ERROR] invalid literal for int() with base 10: 'not-an-int'
```

---

### 4️⃣ `timeit`

```python
@timeit
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

fib(20)
# Example output:
# fib executed in 0.00123456789 seconds
```

*Using a custom timer and handler:*

```python
import time

def my_handler(name, secs):
    print(f"[{name}] took {secs:.4f}s")

@timeit(timer=time.process_time, handler=my_handler)
def busy_wait():
    sum(i*i for i in range(10_000_0))

busy_wait()
# Example output:
# [busy_wait] took 0.1234s
```

---

### 4️⃣ `timing threaded_repeat`
```python
from wrapper_utils import threaded_repeat, repeat, timeit

counter1 = 0
@timeit
@threaded_repeat(n=1000000000)		# 1 Billion
def test1():
    global counter1
    counter1 = counter1 + 1
    # print(counter1)

counter2 = 0
@timeit
@repeat(n=100000000)				# 1 Million
def test2():
    global counter2
    counter2 = counter2 + 1
    # print(counter2)

test1()
test2()

# Quick Test Result:
# test1 executed in 0.0014185999752953649 seconds
# test2 executed in 71.43829840002581 seconds
```

## 📜 License

MIT License – see the `LICENSE` file for details.

---

## 🙋‍♂️ Contributing

Feel free to open issues or submit pull requests.  
When adding a new decorator, please:

1. Write a docstring that follows the existing style.
2. Add a small usage example to this README.
3. Include unit tests covering typical and edge cases.

Happy decorating! 🎉