import asyncio
import time

import websockets


async def handle_client(websocket, path):
    while True:
        message = await websocket.recv()
        print(f"Received message: {message}")
        await websocket.send(f"{message}")
        print(f"Sent message: {message}")


async def main():
    start_server = await websockets.serve(handle_client, "localhost", 8888)
    await start_server.wait_closed()


asyncio.run(main())
