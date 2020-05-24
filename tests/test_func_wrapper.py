from make_it_sync import make_sync
from asyncio import sleep, get_event_loop


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


# Test documentations (help)
# Test wrapping a method
# exceptions
# kwargs
