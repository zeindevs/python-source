import asyncio
import datetime as dt
from scheduler.asyncio import Scheduler


async def foo():
    print("foo")


async def bar():
    print("bar")


async def main():
    loop = asyncio.get_running_loop()
    schedule = Scheduler(loop=loop)

    schedule.cyclic(dt.timedelta(seconds=5), foo)
    schedule.cyclic(dt.timedelta(seconds=10), bar)

    print(schedule)

    while True:
        await asyncio.sleep(1)


asyncio.run(main())
