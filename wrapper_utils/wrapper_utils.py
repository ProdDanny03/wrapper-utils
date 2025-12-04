# wrapper_utils/wrapper_utils.py
import functools
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

_DEFAULT_POOL = ThreadPoolExecutor()


def repeat(n=1):
    """
    The function `repeat` is a decorator that repeats the decorated function a specified number of
    times.
    @param n () - The `n` parameter in the `repeat` function is used to specify how many times a
    decorated function should be repeated when called. If `n` is set to 1, the function will not be
    repeated and will be executed only once. If `n` is greater than 1,
    @returns The `repeat` function is a decorator factory that returns a decorator based on the value of
    `n`. If `n` is equal to 1, it returns the original function without any wrapping. If `n` is greater
    than 1, it returns a wrapper function that calls the original function `n-1` times before calling it
    once more and returning the result.
    Danny - 12/04/2025
    """
    def decorator_repeat(func):
        if n == 1:
            return func  # skip wrapper entirely for n=1

        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(n - 1):
                func(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper_repeat

    return decorator_repeat


def threaded_repeat(n=1, executor=None):
    """
    The `threaded_repeat` function is a decorator that allows a specified function to be executed
    concurrently multiple times using a thread pool.
    @param n () - The `n` parameter in the `threaded_repeat` function specifies the number of times the
    decorated function will be called concurrently. By default, it is set to 1, meaning the function
    will be called once. If you provide a different value for `n`, the function will be executed that
    @param executor () - The `executor` parameter in the `threaded_repeat` function is used to specify
    the concurrent executor to be used for running the decorated function multiple times concurrently.
    If no executor is provided, it defaults to `_DEFAULT_POOL`. This allows you to control how the
    function calls are executed in a concurrent manner
    @returns The `threaded_repeat` function returns a decorator function that can be used to
    concurrently execute a given function `n` times using a specified executor (or a default one if not
    provided). The decorator submits `n` calls of the function concurrently to the executor, waits for
    all tasks to complete, and returns the result of the last call.
    Danny - 12/04/2025
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            pool = executor or _DEFAULT_POOL
            # Submit all n calls concurrently
            futures = [pool.submit(func, *args, **kwargs) for _ in range(n)]
            
            # Wait for all tasks to complete and return the last one
            last_result = None
            for future in as_completed(futures):
                last_result = future.result()
            return last_result
        
        return wrapper
    return decorator


def catch(_func=None, *, exception=None, handler=None, silent=False):
    """
    The `catch` function in Python is a decorator that allows catching specified exceptions and either
    printing the traceback or calling a custom handler while optionally suppressing the exception.
    @param _func () - The `_func` parameter in the `catch` function is used to pass the target function
    that you want to decorate with the exception handling logic. If `_func` is provided, it means you
    are using the decorator with parentheses, and `_func` will be the target function to which the
    exception handling
    @param exception () - The `exception` parameter in the `catch` function is used to specify the type
    of exception that should be caught. If no specific exception type is provided, it defaults to
    catching any `Exception`. You can also pass a list of exception types, which will be converted to a
    tuple for catching multiple
    @param handler () - The `handler` parameter in the `catch` function is used to specify a custom
    function that will be called when an exception is caught. If a `handler` function is provided, it
    will be called with the caught exception as its argument instead of printing the traceback. This
    allows you to define custom
    @param silent () - The `silent` parameter in the `catch` function is a boolean flag that determines
    whether the exception should be handled silently or not. If `silent` is set to `True`, the exception
    will be caught and no traceback will be printed or handler called. If `silent` is set to `
    @returns The `catch` function returns a decorator function if called with parentheses, or a
    decorator function applied to a target function if called without parentheses.
    Danny - 12/04/2025
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
    """
    The `timeit` function is a decorator in Python that measures the execution time of a function and
    optionally calls a handler function with the timing information.
    @param _func () - The `_func` parameter in the `timeit` function is used to optionally pass a
    function to be timed. If `_func` is provided, the decorator `decorator_timeit` is applied directly
    to that function. If `_func` is not provided, the `decorator_timeit`
    @param timer () - The `timer` parameter in the `timeit` function is used to specify the timer
    function that will be used to measure the execution time of the decorated function. By default, it
    is set to `time.perf_counter`, which is a high-resolution timer function in the `time` module that
    @param handler () - The `handler` parameter in the `timeit` function is used to specify a callback
    function that will be called after the execution of the decorated function. This callback function
    can be used to perform custom actions with the timing information of the function execution, such as
    logging the timing data to a file,
    @returns The `timeit` function is a decorator that can be used to measure the execution time of
    another function. When called without any arguments, it returns the `decorator_timeit` function
    which is used as a decorator to measure the execution time of a function. When called with a
    function as an argument, it applies the `decorator_timeit` decorator to that function and returns
    the decorated function
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


def decorator(func):
    """
    The `decorator` function is a versatile decorator that can be used with or without arguments to wrap
    other functions.
    @param func () - The `func` parameter in the `decorator` function is a function that will be
    decorated by the decorator function.
    @returns The `decorator` function returns a wrapper function that can be used as a decorator. The
    wrapper function checks if the decorator is being used with or without arguments, and then applies
    the appropriate behavior based on the usage. If the decorator is used without arguments, it
    decorates the target function directly. If the decorator is used with arguments, it returns an
    actual decorator function that can be used to decorate
    Danny - 12/04/2025
    """
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
