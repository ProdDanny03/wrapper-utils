import functools
import traceback
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor

_DEFAULT_POOL = ThreadPoolExecutor()

def repeat(n=1):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in np.arange(n, dtype=np.int32):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat
    return decorator_repeat

def threaded_repeat(n=1, executor=None):
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

def silent_catch(_func=None, *, exception=None):
    return catch(_func=_func, exception=exception, silent=True)

def catch(_func=None, *, exception=None, handler=None, silent=False):
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
