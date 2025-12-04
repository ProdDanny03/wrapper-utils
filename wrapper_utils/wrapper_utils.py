import functools
import traceback
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor

_DEFAULT_POOL = ThreadPoolExecutor()

def repeat(n=1):
    """
    The `repeat` function is a Python decorator that allows a function to be executed multiple times
    based on the specified number `n`.
    @param n () - The `n` parameter in the `repeat` function is a default parameter with a default value
    of 1. This parameter is used to specify the number of times a decorated function should be repeated
    when it is called. If `n` is not provided when calling the `repeat` decorator, it
    @returns The `repeat` function is returning a decorator function `decorator_repeat`. This decorator
    function takes another function `func` as an argument and returns a wrapped function
    `wrapper_repeat` that will repeat the execution of `func` `n` times.
    Danny - 12/04/2025
    """
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in np.arange(n, dtype=np.int32):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat
    return decorator_repeat

def threaded_repeat(n=1, executor=None):
    """
    The `threaded_repeat` function is a decorator in Python that allows a specified function to be
    executed repeatedly in a threaded manner using a specified executor.
    @param n () - The `n` parameter in the `threaded_repeat` function specifies the number of times a
    given function should be repeated in a threaded manner. By default, if no value is provided for `n`,
    it will be set to 1, meaning the function will be executed once.
    @param executor () - The `executor` parameter in the `threaded_repeat` function is used to specify
    the executor (thread pool or process pool) that will be used to submit the repeated function calls
    for execution. If no executor is provided, it defaults to `_DEFAULT_POOL`. This allows you to
    control the execution environment
    @returns The `threaded_repeat` function returns a decorator function `decorator_threaded_repeat`.
    Danny - 12/04/2025
    """
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
    The `catch` function is a decorator in Python that allows for catching specified exceptions and
    handling them with optional custom handlers.
    @param _func () - The `_func` parameter is a function that can be passed as an argument to the
    `catch` decorator. It is used to specify the function that you want to wrap with the error handling
    logic provided by the `catch` decorator.
    @param exception () - The `exception` parameter in the `catch` function is used to specify the type
    of exception that should be caught. If no specific exception type is provided, it defaults to
    catching all exceptions of type `Exception`. If a list of exception types is provided, they are
    converted to a tuple for handling
    @param handler () - The `handler` parameter in the `catch` function is used to specify a custom
    function that will be called when an exception is caught. If a `handler` function is provided, it
    will be called with the exception object as its argument instead of printing the traceback. This
    allows you to define your
    @param silent () - The `silent` parameter in the `catch` function is a boolean flag that determines
    whether the exception should be handled silently without printing any traceback information. If
    `silent` is set to `True`, the exception will be caught and handled without any output to the
    console. If `silent` is `
    @returns The `catch` function is returning a decorator function called `decorator_catch` if `_func`
    is None, or it is returning the result of calling `decorator_catch` with `_func` as an argument.
    Danny - 12/04/2025
    """
    if not exception:
        exception = Exception
    if type(exception) is list:
        exception = tuple(exception)
    
    def decorator_catch(func):
        @functools.wraps(func)
        def wrapper_catch(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception as e:
                if not silent:
                    if not handler:
                        traceback.print_exc()
                    else:
                        handler(e)
            return wrapper_catch
        if _func is None:
            return decorator_catch
        else:
            return decorator_catch(_func)

def timeit(_func=None, *, timer=time.perf_counter, handler=None):
    """
    The `timeit` function is a decorator in Python that measures the execution time of a function and
    optionally calls a handler function with the timing information.
    @param _func () - The `_func` parameter in the `timeit` function is used to optionally pass a
    function to be timed. If `_func` is provided, the decorator `decorator_timeit` is applied directly
    to that function. If `_func` is not provided (i.e., it is `None
    @param timer () - The `timer` parameter in the `timeit` function is used to specify the timer
    function that will be used to measure the execution time of the decorated function. By default, it
    is set to `time.perf_counter`, which is a high-resolution timer function in the `time` module of
    @param handler () - The `handler` parameter in the `timeit` function is used to specify a callback
    function that will be called after the execution of the decorated function. This callback function
    can be used to perform custom actions with the timing information of the function execution, such as
    logging the timing data to a file,
    @returns The `timeit` function returns either the `decorator_timeit` function or the result of
    calling `decorator_timeit` with the provided function `_func`, depending on whether `_func` is
    `None` or not.
    Danny - 12/04/2025
    """
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
