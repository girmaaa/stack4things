import asyncio
import websockets
import json

uris = [
    "ws://localhost:8888",
    "ws://localhost:8889",
    "ws://localhost:8890"
]

async def subscribe_and_send_data(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"type": "subscribe", "topic": "temperature_updates"}))
        print(f"Subscribed to {uri}")

        while True:
            # Simulate sending data
            data = {"type": "data", "topic": "temperature_updates", "payload": {"temperature": 23.5, "unit": "C"}}
            await websocket.send(json.dumps(data))
            print(f"Sent: {json.dumps(data)}")

            await asyncio.sleep(5)

async def main():
    await asyncio.gather(*(subscribe_and_send_data(uri) for uri in uris))

if __name__ == "__main__":
    asyncio.run(main())






