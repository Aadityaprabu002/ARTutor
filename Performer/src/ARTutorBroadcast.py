import websockets
import asyncio

PORT = 8080
print(f'Server is listening on port: {PORT}')
connected = set()


async def echo(ws_client, path):
    print('A Client just connected!')
    connected.add(ws_client)
    try:
        async for message in ws_client:
            print('A message received from client')
            # for conn in connected:
            #     if conn != ws_client:
            #         await conn.send(message)

    except websockets.exceptions.ConnectionClosed as e:
        print('A Client just disconnected!')
    finally:
        connected.remove(ws_client)


server = websockets.serve(echo, 'localhost', PORT)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
