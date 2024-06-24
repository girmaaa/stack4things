import asyncio
import websockets
import json

async def handle_client(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        if "token" in data and "secret" in data:
            print(f"Received token message: {data}")
            response = {"status": "authenticated"}
            await websocket.send(json.dumps(response))
        elif "type" in data and data["type"] == "data":
            print(f"Received test message: {data}")
            response = {"status": "message_received"}
            await websocket.send(json.dumps(response))
        else:
            response = {"status": "error", "message": "Invalid message"}
            await websocket.send(json.dumps(response))

start_server = websockets.serve(handle_client, "localhost", 8889)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

