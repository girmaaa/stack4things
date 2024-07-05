import asyncio
import websockets
import json
import message_pb2

async def test_client():
    async with websockets.connect("ws://localhost:8889") as websocket:
        # Sending authentication message
        token_message = message_pb2.TokenMessage()
        token_message.token = "WpibQRzM25QhsBtb8LXPGQ"
        token_message.secret = "WpibQRzM25QhsBtb8LXPGQ"
        await websocket.send(token_message.SerializeToString())
        print(f"Sent authentication message: token: \"{token_message.token}\" secret: \"{token_message.secret}\"")

        # Receiving authentication response
        response = await websocket.recv()
        response_message = message_pb2.ResponseMessage()
        response_message.ParseFromString(response)
        print(f"Received server response: status: \"{response_message.status}\"")

        # Sending a data message
        data_message = message_pb2.DataMessage()
        data_message.type = "data"
        data_message.content = "Hello, server!"
        await websocket.send(data_message.SerializeToString())
        print(f"Sent data message: type: \"{data_message.type}\" content: \"{data_message.content}\"")

        # Receiving data response
        response = await websocket.recv()
        response_message.ParseFromString(response)
        if response_message.status == "data_received":
            print("Received server response: status: \"data_received\"")
            for data_entry in response_message.data:
                print(f"data: {{ id: {data_entry.id}, data: \"{data_entry.data}\" }}")
        else:
            print(f"Received server response: status: \"{response_message.status}\"")

        # Sending a request for data message
        request_message = message_pb2.DataMessage()
        request_message.type = "request_data"
        await websocket.send(request_message.SerializeToString())
        print(f"Sent request message: type: \"{request_message.type}\"")

        # Receiving data response
        response = await websocket.recv()
        response_message.ParseFromString(response)
        if response_message.status == "data_received":
            print("Received server response: status: \"data_received\"")
            for data_entry in response_message.data:
                print(f"data: {{ id: {data_entry.id}, data: \"{data_entry.data}\" }}")
        else:
            print(f"Received server response: status: \"{response_message.status}\"")

        # Sending an error message
        error_message = message_pb2.ErrorMessage()
        error_message.type = "error"
        error_message.content = "Sample error message"
        await websocket.send(error_message.SerializeToString())
        print(f"Sent error message: type: \"{error_message.type}\" content: \"{error_message.content}\"")

        # Receiving error logged response
        response = await websocket.recv()
        response_message.ParseFromString(response)
        print(f"Received server response: status: \"{response_message.status}\"")

asyncio.get_event_loop().run_until_complete(test_client())

