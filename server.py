import asyncio
import websockets
import json
import os
from pathlib import Path

PORT = int(os.environ.get("PORT", 10000))
CLIENTS = set()
STATIC_DIR = Path("static")


# ---------- HTTP handler ----------
async def process_request(path, request_headers):
    # Only allow websocket on /ws
    if path == "/ws":
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

    return 200, [("Content-Type", content_type)], content


# ---------- WebSocket handler ----------
async def chat_handler(websocket):
    CLIENTS.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            for client in CLIENTS:
                if client.open:
                    await client.send(json.dumps(data))
    finally:
        CLIENTS.remove(websocket)


# ---------- MAIN ----------
async def main():
    async with websockets.serve(
        chat_handler,
        "0.0.0.0",
        PORT,
        process_request=process_request
    ):
        print("Server running")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
