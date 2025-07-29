import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from typing import Callable, TypeVar, Awaitable

R = TypeVar("R")


def _sync_version_of_function(fn: Callable[..., Awaitable[R]], *args, **kwargs) -> R:
    # Determine what environment we are currently in.
    loop_exists = False
    try:
        loop = asyncio.get_running_loop()
        loop_exists = True
        loop_is_running = loop.is_running()
    except RuntimeError:
        loop_is_running = False

    # Next, depending on the environment, we will either run the function directly
    # or create a new thread to run it in.
    if loop_exists and not loop_is_running:
        # Call the function directly
        r = fn(*args, **kwargs)
        return loop.run_until_complete(r)
    else:
        # Forced to create a new event loop.

        def get_data_wrapper(*args, **kwargs):
            # New thread - get the loop.
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            assert not loop.is_running()
            return loop.run_until_complete(fn(*args, **kwargs))

        exector = ThreadPoolExecutor(max_workers=1)
        future = exector.submit(get_data_wrapper, *args, **kwargs)

        return future.result()


def make_sync(fn: Callable[..., Awaitable[R]]) -> Callable[..., R]:
    """
    Wraps an async function to make it synchronous. The function will will try to run it
    on the current thread if it can fine an event loop that isn't running, otherwise it will
    create a new thread and execute it there - one thread per async method call - and block
    until it has completed.

    Arguments:
        fn              The async function you want to call synchronously

    Returns:
        sync_fn         A function that has the same signature as `fn`, but can be called
                        synchronously.

    Note:
      If you call this 10 times with long running async methods, they will run on 10 different
      threads.
    """
    # Define the function we will return that will do the work
    if _check_is_abstract(fn):
        func_name = fn.__name__

        @wraps(fn)
        def wrapped_call(*args, **kwargs):  # type: ignore
            v = getattr(args[0], func_name, None)
            if v is None:
                raise NotImplementedError(
                    f"Function {func_name} is not implemented by {args[0].__name__}"
                )
            return _sync_version_of_function(v, *(args[1:]), **kwargs)

        del wrapped_call.__isabstractmethod__  # type: ignore
        return wrapped_call
    else:

        @wraps(fn)
        def wrapped_call(*args, **kwargs):
            return _sync_version_of_function(fn, *args, **kwargs)

        return wrapped_call


def _check_is_abstract(f: Callable):
    "Check to see if the function is callable"
    return hasattr(f, "__isabstractmethod__") and f.__isabstractmethod__
