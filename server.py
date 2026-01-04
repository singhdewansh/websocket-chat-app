import asyncio
import websockets
import json
import os
import threading
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

# Ports
HTTP_PORT = int(os.environ.get("PORT", 8000))
WS_PORT = HTTP_PORT  # WebSocket uses same Render port

# Connected clients
clients = set()


# ---------------- WebSocket Server ----------------
async def chat_handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)

            # Broadcast message to all clients
            for client in clients:
                if client.open:
                    await client.send(json.dumps(data))

    except:
        pass
    finally:
        clients.remove(websocket)


async def start_websocket():
    async with websockets.serve(chat_handler, "0.0.0.0", WS_PORT):
        await asyncio.Future()  # run forever


# ---------------- HTTP Server ----------------
def start_http():
    os.chdir("static")  # serve index.html from static/
    handler = SimpleHTTPRequestHandler
    with TCPServer(("", HTTP_PORT), handler) as httpd:
        httpd.serve_forever()


# ---------------- MAIN ----------------
def main():
    # Start HTTP server in background
    threading.Thread(target=start_http, daemon=True).start()

    # Start WebSocket server
    asyncio.run(start_websocket())


if __name__ == "__main__":
    main()
