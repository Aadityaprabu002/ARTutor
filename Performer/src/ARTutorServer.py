import websockets
import asyncio

PORT = 8080
print(f'Server is listening on port: {PORT}')
connected = set()


async def echo(ws_client, path):
    print('A Client just connected!')
    try:
        async for message in ws_client:
            print('Received message from client:' + message)
            await ws_client.send('Pong:'+message)
    except websockets.exceptions.ConnectionClosed as e:
        print('A Client just disconnected!')

server = websockets.serve(echo,'localhost',PORT)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()