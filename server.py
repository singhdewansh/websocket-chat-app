import asyncio
import json
import os
import websockets

# Store all connected clients
connected_clients = set()

async def chat_handler(websocket):
    # Add new client
    connected_clients.add(websocket)
    print("New client connected")

    try:
        async for message in websocket:
            data = json.loads(message)

            # Create message to broadcast
            response = {
                "user": "User",
                "message": data["message"]
            }

            # Send message to all connected clients
            for client in connected_clients:
                if client.open:
                    await client.send(json.dumps(response))

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

    finally:
        # Remove client when disconnected
        connected_clients.remove(websocket)


async def main():
    # Render gives PORT automatically
    port = int(os.environ.get("PORT", 8765))

    print(f"Server running on port {port}")

    async with websockets.serve(
        chat_handler,
        "0.0.0.0",
        port,
        ping_interval=20,
        ping_timeout=20
    ):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
