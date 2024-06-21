import asyncio
import websockets
import json

# Shared secret (must match the one in superbroker.py)
shared_secret = "WpibQRzM25QhsBtb8LXPGQ"

async def connect():
    uri = "ws://localhost:8889"  # Changed port to 8889
    async with websockets.connect(uri) as websocket:
        # Send token and secret
        token_data = json.dumps({
            "token": "WpibQRzM25QhsBtb8LXPGQ",
            "secret": shared_secret
        })
        await websocket.send(token_data)
        print(f"Sent token message: {token_data}")  # Debug print

        # Send a test message
        test_message = json.dumps({"type": "data", "content": "Hello, server!"})
        await websocket.send(test_message)
        print(f"Sent test message: {test_message}")  # Debug print

        # Listen for messages
        async for message in websocket:
            print(f"Received message: {message}")

if __name__ == "__main__":
    asyncio.run(connect())

