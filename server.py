
import asyncio
import websockets
import json
import os
from pathlib import Path
from http import HTTPStatus

PORT = int(os.environ.get("PORT", 10000))
CLIENTS = set()
STATIC_DIR = Path("static")

# HTTP request handler
async def process_request(path, request_headers):
    # Only handle HTTP for files
    if request_headers.get("Upgrade", "").lower() == "websocket":
        return None  # Let WebSocket handshake pass

    # Health check HEAD request (from Render) → ignore
    if request_headers.get("Method") == "HEAD":
        return HTTPStatus.OK, [], b""

    if path == "/":
        path = "/index.html"

    file_path = STATIC_DIR / path.lstrip("/")

    if not file_path.exists():
        return HTTPStatus.NOT_FOUND, [], b"Not Found"

    content = file_path.read_bytes()

    # Content type
    content_type = "text/html"
    if file_path.suffix == ".js":
        content_type = "application/javascript"
    elif file_path.suffix == ".css":
        content_type = "text/css"

    headers = [("Content-Type", content_type)]
    return HTTPStatus.OK, headers, content


# WebSocket handler
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


# Main server
async def main():
    async with websockets.serve(
        chat_handler,
        "0.0.0.0",
        PORT,
        process_request=process_request
    ):
        print(f"Server running on port {PORT}")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
