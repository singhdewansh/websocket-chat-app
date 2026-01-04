import asyncio
import websockets
import json
import os
from pathlib import Path

PORT = int(os.environ.get("PORT", 10000))
CLIENTS = set()
STATIC_DIR = Path("static")


# -------- Serve frontend files (HTTP) --------
async def process_request(path, request_headers):
    # IMPORTANT: allow WebSocket handshake to pass through
    if request_headers.get("Upgrade", "").lower() == "websocket":
        return None

    if path == "/":
        path = "/index.html"

    file_path = STATIC_DIR / path.lstrip("/")

    if not file_path.exists():
        return 404, [], b"Not Found"

    content = file_path.read_bytes()

    content_type = "text/html"
    if file_path.suffix == ".js":
        content_type = "application/javascript"
    elif file_path.suffix == ".css":
        content_type = "text/css"

    headers = [("Content-Type", content_type)]
    return 200, headers, content


# -------- WebSocket chat logic --------
async def chat_handler(websocket):
    CLIENTS.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)

            # broadcast to all connected clients
            for client in CLIENTS:
                if client.open:
                    await client.send(json.dumps(data))

    finally:
        CLIENTS.remove(websocket)


# -------- Main server --------
async def main():
    async with websockets.serve(
        chat_handler,
        "0.0.0.0",
        PORT,
        process_request=process_request
    ):
        print("Server running...")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
