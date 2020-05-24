from typing import Callable, TypeVar
from concurrent.futures import ThreadPoolExecutor
import asyncio

T = TypeVar('T')
R = TypeVar('R')


def make_sync(fn: Callable[..., R]) -> Callable[..., R]:
    '''
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
    '''
    # Define the function we will return that will do the work
    def sync_version_of_function(*args, **kwargs):
        loop = asyncio.get_event_loop()
        if not loop.is_running():
            # Call the function directly
            r = fn(*args, *kwargs)
            return loop.run_until_complete(r)
        else:
            def get_data_wrapper(*args, **kwargs):
                # New thread - get the loop.
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                assert not loop.is_running()
                return loop.run_until_complete(fn(*args, **kwargs))

            exector = ThreadPoolExecutor(max_workers=1)
            future = exector.submit(get_data_wrapper, *args, *kwargs)

            return future.result()

    return sync_version_of_function
