import asyncio
import websockets
import json
import os
from pathlib import Path

PORT = int(os.environ.get("PORT", 10000))
CLIENTS = set()

STATIC_DIR = Path("static")


# ---------- Serve HTTP files ----------
async def process_request(path, request_headers):
    if path == "/":
        path = "/index.html"

    file_path = STATIC_DIR / path.lstrip("/")

    if not file_path.exists() or not file_path.is_file():
        return 404, [], b"Not Found"

    content = file_path.read_bytes()

    headers = [
        ("Content-Type", "text/html")
    ]

    if file_path.suffix == ".js":
        headers = [("Content-Type", "application/javascript")]
    elif file_path.suffix == ".css":
        headers = [("Content-Type", "text/css")]

    return 200, headers, content


# ---------- WebSocket handler ----------
async def chat_handler(websocket):
    CLIENTS.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)

            for client in CLIENTS:
                if client.open:
                    await client.send(json.dumps(data))

    except:
        pass
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
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
