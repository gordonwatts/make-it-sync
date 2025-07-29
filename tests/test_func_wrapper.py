from asyncio import new_event_loop, set_event_loop, sleep
import inspect
from typing import Tuple
from abc import ABC, abstractmethod

import pytest


from make_it_sync import make_sync


@pytest.fixture
def event_loop_fixture():
    loop = new_event_loop()
    set_event_loop(loop)
    yield loop
    loop.close()
    set_event_loop(None)


async def simple_func(a: int) -> int:
    "Simple sleeper function to test calling mechanics"
    await sleep(0.01)
    return a + 1


def test_wrap_normal():
    t_wrap = make_sync(simple_func)
    assert t_wrap(4) == 5


def test_wrap_with_loop(event_loop_fixture):
    t_wrap = make_sync(simple_func)
    assert t_wrap(4) == 5


def test_wrap_with_running_loop(event_loop_fixture):
    t_wrap = make_sync(simple_func)

    async def doit():
        assert t_wrap(5) == 6

    event_loop_fixture.run_until_complete(doit())


async def simple_raise(a: int) -> int:
    "See if we can cause an exception correctly"
    await sleep(0.01)
    raise Exception("hi there")


def test_wrap_exception():
    t_wrap = make_sync(simple_raise)
    with pytest.raises(Exception) as e:
        t_wrap(5)

    assert "hi there" in str(e.value)


async def simple_kwargs(a: int, me: int = 10):
    await sleep(0.01)
    return a + me


def test_wrap_kwargs_default():
    t_wrap = make_sync(simple_kwargs)
    assert t_wrap(1) == 11


def test_wrap_kwargs_given():
    t_wrap = make_sync(simple_kwargs)
    assert t_wrap(1, me=11) == 12


async def simple_no_wait(a: int):
    return a + 1


def test_wrap_no_await():
    t_wrap = make_sync(simple_no_wait)
    assert t_wrap(1) == 2


def test_wrap_signature():
    s_orig = inspect.signature(simple_func)
    t_wrap = make_sync(simple_func)
    s_new = inspect.signature(t_wrap)

    assert str(s_orig) == str(s_new)


def test_wrap_docstring():
    s_orig = simple_func.__doc__
    s_new = make_sync(simple_func).__doc__

    assert s_orig == s_new


class tester:
    def __init__(self, b: int):
        self._b = b

    async def my_async(self, a: int) -> int:
        await sleep(0.01)
        return a + self._b

    my = make_sync(my_async)


def test_wrap_class_method():
    o = tester(10)
    assert o.my(1) == 11


async def func_with_kwargs(bins: int = 10, range: Tuple[int, int] = (4, 10)) -> int:
    await sleep(0.01)
    return bins + range[0]


def test_wrap_kwargs_defaults():
    wrap_it = make_sync(func_with_kwargs)
    assert wrap_it() == 14


def test_wrap_kwargs_specified():
    wrap_it = make_sync(func_with_kwargs)
    assert wrap_it(bins=5, range=(5, 10)) == 10


def test_wrap_kwargs_specified_loop(event_loop_fixture):
    t_wrap = make_sync(func_with_kwargs)

    async def doit():
        assert t_wrap(bins=5, range=(5, 10)) == 10

    event_loop_fixture.run_until_complete(doit())


def test_abstract_method_created():
    class abc_base(ABC):
        @abstractmethod
        async def doit_async(self):
            raise NotImplementedError()

        doit = make_sync(doit_async)

    class abs_derived(abc_base):
        async def doit_async(self):
            return 42

    abs_derived()


def test_abstract_method_invoked():
    class abc_base(ABC):
        @abstractmethod
        async def doit_async(self):
            raise NotImplementedError()

        doit = make_sync(doit_async)

    class abs_derived(abc_base):
        async def doit_async(self):
            return 42

    a = abs_derived()
    assert a.doit() == 42


def test_abstract_two_methods_invoked():
    "Checking to make sure lambda capture is working as expected"

    class abc_base_2(ABC):
        @abstractmethod
        async def doit_async_1(self):
            raise NotImplementedError()

        @abstractmethod
        async def doit_async_2(self):
            raise NotImplementedError()

        doit_1 = make_sync(doit_async_1)
        doit_2 = make_sync(doit_async_2)

    class abs_derived_2(abc_base_2):
        async def doit_async_1(self):
            return 42

        async def doit_async_2(self):
            return 43

    a = abs_derived_2()
    assert a.doit_1() == 42
    assert a.doit_2() == 43


def test_abstract_method_arguments():
    class abc_base(ABC):
        @abstractmethod
        async def doit_async(self, a1: int, a2: int = 20, a3: int = 30):
            raise NotImplementedError()

        doit = make_sync(doit_async)

    class abs_derived(abc_base):
        async def doit_async(self, a1: int, a2: int = 20, a3: int = 30):
            return a1 + a2 + a3

    a = abs_derived()
    assert a.doit(1, a3=40) == (1 + 20 + 40)
