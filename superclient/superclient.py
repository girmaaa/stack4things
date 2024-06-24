import asyncio
import websockets
import json

async def test_client():
    async with websockets.connect("ws://localhost:8889") as websocket:
        token_message = {"token": "WpibQRzM25QhsBtb8LXPGQ", "secret": "WpibQRzM25QhsBtb8LXPGQ"}
        await websocket.send(json.dumps(token_message))
        print(f"Sent token message: {token_message}")
        
        response = await websocket.recv()
        print(f"Received server response: {response}")
        
        test_message = {"type": "data", "content": "Hello, server!"}
        await websocket.send(json.dumps(test_message))
        print(f"Sent test message: {test_message}")
        
        response = await websocket.recv()
        print(f"Received server response: {response}")

asyncio.get_event_loop().run_until_complete(test_client())

