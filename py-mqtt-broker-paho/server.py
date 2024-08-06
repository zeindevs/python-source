import asyncio
from amqtt.broker import Broker

config = {
    "listeners": {
        "default": {"type": "tcp", "bind": "0.0.0.0:1883"},
        "ws-mqtt": {"bind": "127.0.0.1:8080", "type": "ws", "max_connections": 10},
    },
    "sys_interval": 10,
    "auth": {
        "allow-anonymous": True,
    },
    "topic-check": {"enabled": True},
}

broker = Broker(config)


async def test_coro():
    await broker.start()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(test_coro())
    asyncio.get_event_loop().run_forever()
