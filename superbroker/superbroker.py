import asyncio
import websockets
import json

# Shared secret (must match the one in superclient.py)
shared_secret = "WpibQRzM25QhsBtb8LXPGQ"

clients = set()
clients_lock = asyncio.Lock()

async def validate_token(token, secret):
    return token == shared_secret

async def handler(websocket, path):
    try:
        print("New connection")  # Debug print
        # Receive the initial message containing the token and secret
        token_message = await websocket.recv()
        print(f"Received token message: {token_message}")  # Debug print
        token_data = json.loads(token_message)
        token = token_data.get('token', None)
        secret = token_data.get('secret', None)

        if not token or not secret or not await validate_token(token, secret):
            await websocket.send(json.dumps({"error": "Invalid token or secret"}))
            print("Invalid token or secret")  # Debug print
            return

        async with clients_lock:
            clients.add(websocket)
        print("Client added")  # Debug print

        async for message in websocket:
            data = json.loads(message)
            print(f"Received message: {data}")  # Debug print
            if data['type'] == 'subscribe':
                response = json.dumps({"type": "subscribe", "topic": data['topic']})
                await websocket.send(response)
            elif data['type'] == 'data':
                async with clients_lock:
                    for client in clients:
                        if client != websocket:
                            await client.send(message)

    except websockets.ConnectionClosedError:
        pass
    finally:
        async with clients_lock:
            if websocket in clients:
                clients.remove(websocket)
        print("Client removed")  # Debug print

async def run_server():
    start_server = websockets.serve(handler, "0.0.0.0", 8889)
    async with start_server as server:
        await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(run_server())

