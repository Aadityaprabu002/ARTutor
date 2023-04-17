import websockets
import asyncio

async def listen():
    url = 'ws://3.110.225.126:8080'
    async with websockets.connect(url) as ws:
        while True:
            landmarks = await ws.recv()
            print(landmarks.decode())

asyncio.get_event_loop(). \
    run_until_complete(listen())
