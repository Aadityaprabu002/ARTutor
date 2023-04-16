import websockets
import asyncio


async def get_input():
    return input()

async def listen():
    url = 'ws://127.0.0.1:8080'
    async with websockets.connect(url) as ws:
        await ws.send('Hello server!')
        while True:
            task = asyncio.create_task(get_input())
            msg = await ws.recv()
            print(msg)
    

asyncio.get_event_loop(). \
    run_until_complete(listen())
