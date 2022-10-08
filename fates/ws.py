import asyncio
import time
from fastapi import WebSocket
import orjson
from fates import models
from fates.app import app, mapleshade


class ConnectionManager:
    """
    Represents a connection manager which handles connections of a client and disconnecting unresponsive clients
    """

    def __init__(self):
        self.ws: list[WebSocket] = []

        asyncio.create_task(self._check_ping())

    async def _check_ping(self):
        """Checks the ping of all websockets, and disconnects them if they are unresponsive"""
        while True:
            for ws in self.ws:
                try:
                    if time.time() - ws.state.last_ping > 45:
                        await self.disconnect(ws, "Ping timeout")
                except:
                    pass
            await asyncio.sleep(5)

    async def connect(self, ws: WebSocket):
        """Connects a websocket and adds it to the connection manager list thus adding it to PING checks"""
        await ws.accept()
        self.ws.append(ws)

    async def disconnect(self, ws: WebSocket, reason: str = "Unknown"):
        """Disconnects a websocket and removes it from the connection manager list thus removing it from PING checks"""
        try:
            self.ws.remove(ws)
            await ws.close(4000, reason)
        except:
            pass


manager = ConnectionManager()


@app.websocket("/ws/preview")
async def preview(ws: WebSocket):
    """Preview websocket for live previewing in the site"""

    await manager.connect(ws)

    try:
        while True:
            data = await ws.receive_text()
            if data == "PING":
                ws.state.last_ping = time.time()
                await ws.send_text(f"PONG:{time.time()}")
            else:
                try:
                    data = orjson.loads(data)
                except:
                    await manager.disconnect(ws, "Invalid JSON")

                try:
                    data = models.PreviewData(**data)
                except Exception as exc:
                    print(exc)
                    await manager.disconnect(ws, f"Invalid data in JSON")
                    return

                ret = {"text": mapleshade.sanitize(data.content, data.type)}

                await ws.send_text(orjson.dumps(ret).decode())
    except Exception as exc:
        try:
            print(exc)
            await manager.disconnect(ws, "Unknown error")
        except:
            pass
