import asyncio
import websockets
import json
import http.server
import socketserver

# Global set of WebSocket servers
servers = set()

async def handler(websocket, path):
    servers.add(websocket)  # Add WebSocket server to the set
    try:
        async for message in websocket:
            data = json.loads(message)
            if data['type'] == 'subscribe':
                # Manage subscriptions
                response = json.dumps({"type": "subscribe", "topic": data['topic']})
                await websocket.send(response)
            elif data['type'] == 'data':
                # Handle and forward data messages to all servers
                for server in servers:
                    if server != websocket:
                        await server.send(message)
    except websockets.ConnectionClosedError:
        pass  # Handle connection closed errors if needed
    finally:
        servers.remove(websocket)  # Remove WebSocket server when disconnected

async def run_server(port):
    start_server = websockets.serve(handler, "0.0.0.0", port)
    async with start_server as server:
        await server.wait_closed()

if __name__ == "__main__":
    # Start multiple instances on different ports
    loop = asyncio.get_event_loop()
    tasks = [run_server(8888), run_server(8889), run_server(8890)]
    loop.run_until_complete(asyncio.gather(*tasks))


