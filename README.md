# make-it-sync

This very simple library helps provide a synchronous interface for your python `async` functions and class methods.

## Introduction

```python
from asyncio import sleep
from make_it_sync import make_sync

async def simple_func(a: int) -> int:
    'Simple sleeper function to test calling mechanics'
    await sleep(0.01)
    return a + 1


t_wrap = make_sync(simple_func)
print (t_wrap(4))

# Prints out 5
```

It works by running an `async` event loop and executing the function. It will use the current thread if no loop is running, otherwise it will create a new thread and run the function there.

Features:

1. Will wrap a stand-alone function
1. All arguments (keyword and positional) are passed
1. Instance methods on classes may be wrapped
1. Abstract methods are correctly handled.

## Usage

To install `pip install make-it-async`.

The `make_sync` function creates a new function that will call the function you pass to it:

```python
async def simple_func(a: int) -> int:
    'Simple sleeper function to test calling mechanics'
    await sleep(0.01)
    return a + 1


t_wrap = make_sync(simple_func)
```

You may treat `t_wrap` as a python function. You could use `make_sync` as a function decorator, though that isn't the normal usage as that would hid the `async` version of the function. Normally, `make_sync` is used to provide a non-async, alternate, version of the function.

It is also possible to use `make_sync` with abstract functions:

```python
class abc_base(ABC):
    @abstractmethod
    async def doit_async(self):
        raise NotImplementedError()

    doit = make_sync(doit_async)

class abc_derived(abc_base):
    async def doit_async(self):
        return 42

a = abs_derived()
print(a.doit())
# Will print out 42
```

The abstract dispatch will occur at runtime and the call to `doit_async` will be pulled from the the sub-class. This allows you to define the asynchronous API in an `ABC`, and build a common set of synchronous methods.
