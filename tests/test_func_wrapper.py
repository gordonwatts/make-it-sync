from make_it_sync import make_sync
from asyncio import sleep, get_event_loop
import pytest
import inspect


async def simple_func(a: int) -> int:
    'Simple sleeper function to test calling mechanics'
    await sleep(0.01)
    return a + 1


def test_wrap_normal():
    t_wrap = make_sync(simple_func)
    assert t_wrap(4) == 5


def test_wrap_with_loop():
    t_wrap = make_sync(simple_func)
    _ = get_event_loop()
    assert t_wrap(4) == 5


def test_wrap_with_running_loop():
    t_wrap = make_sync(simple_func)

    async def doit():
        assert t_wrap(5) == 6

    loop = get_event_loop()
    loop.run_until_complete(doit())


async def simple_raise(a: int) -> int:
    'See if we can cause an exception correctly'
    await sleep(0.01)
    raise Exception('hi there')


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
