import asyncio
import websockets
import json
import os

connected_clients = set()

async def handler(websocket):
    connected_clients.add(websocket)
    username = "Unknown"

    try:
        async for message in websocket:
            data = json.loads(message)

            if data["type"] == "join":
                username = data["user"]
                join_msg = json.dumps({
                    "type": "system",
                    "text": f"{username} joined the chat"
                })
                await broadcast(join_msg)

            elif data["type"] == "message":
                chat_msg = json.dumps({
                    "type": "message",
                    "user": data["user"],
                    "text": data["text"]
                })
                await broadcast(chat_msg)

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)
        leave_msg = json.dumps({
            "type": "system",
            "text": f"{username} left the chat"
        })
        await broadcast(leave_msg)

async def broadcast(message):
    for client in connected_clients:
        await client.send(message)

async def main():
    port = int(os.environ.get("PORT", 8765))
    async with websockets.serve(
        handler,
        "0.0.0.0",
        port,
        ping_interval=None
    ):
        print(f"Server running on port {port}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
