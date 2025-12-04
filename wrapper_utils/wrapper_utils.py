# wrapper_utils/wrapper_utils.py
import functools
import traceback
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor

_DEFAULT_POOL = ThreadPoolExecutor()


def repeat(n=1):
    """Decorator that repeats a call *n* times and returns the last result."""
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in np.arange(n, dtype=np.int32):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat
    return decorator_repeat


def threaded_repeat(n=1, executor=None):
    """Decorator that repeats a call *n* times in a thread pool."""
    def decorator_threaded_repeat(func):
        @functools.wraps(func)
        def wrapper_threaded_repeat(*args, **kwargs):
            def run_repeated():
                for _ in np.arange(n, dtype=np.int32):
                    value = func(*args, **kwargs)
                return value
            return (executor or _DEFAULT_POOL).submit(run_repeated)
        return wrapper_threaded_repeat
    return decorator_threaded_repeat


def catch(_func=None, *, exception=None, handler=None, silent=False):
    """
    Decorator that catches *exception* (or ``Exception`` by default) and
    optionally forwards it to *handler*.  The exception is **swallowed**;
    the wrapped function returns ``None`` when an exception is caught.

    It works both as ``@catch`` and ``@catch(exception=..., handler=..., silent=...)``.
    """
    # Default to catching any Exception
    if exception is None:
        exception = Exception
    # Allow a list of exception types
    if isinstance(exception, list):
        exception = tuple(exception)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception as e:
                # If silent is False we either print the traceback or call the handler
                if not silent:
                    if handler:
                        handler(e)
                    else:
                        traceback.print_exc()
                # Swallow the exception – caller gets ``None``
                return None
        return wrapper

    # If the decorator is used without parentheses, ``_func`` is the target function.
    if _func is None:
        return decorator
    else:
        return decorator(_func)


def timeit(_func=None, *, timer=time.perf_counter, handler=None):
    """Decorator that measures execution time and optionally calls *handler*."""
    def decorator_timeit(func):
        @functools.wraps(func)
        def wrapper_timeit(*args, **kwargs):
            start = timer()
            ret = func(*args, **kwargs)
            end = timer()
            run_time = end - start
            if handler:
                handler(func.__name__, run_time)
            print(f"{func.__name__} executed in {run_time} seconds")
            return ret
        return wrapper_timeit

    if _func is None:
        return decorator_timeit
    else:
        return decorator_timeit(_func)


def decorator(func):
    """Higher‑order decorator that supports both ``@decorator`` and ``@decorator(arg…)``."""
    @functools.wraps(func)
    def wrapper(*dargs, **dkwargs):
        # Simple usage: @something
        if len(dargs) == 1 and callable(dargs[0]) and not dkwargs:
            target = dargs[0]

            @functools.wraps(target)
            def wrapped(*a, **k):
                return func(target, *a, **k)
            return wrapped
        else:
            # Usage with arguments: @something(x=5)
            def actual_decorator(target):
                @functools.wraps(target)
                def wrapped(*a, **k):
                    # Merge positional args: decorator args first, then function call args
                    all_args = dargs + a
                    # Merge keyword args: decorator kwargs first, then function call kwargs
                    all_kwargs = {**dkwargs, **k}
                    return func(target, *all_args, **all_kwargs)
                return wrapped
            return actual_decorator
    return wrapper
