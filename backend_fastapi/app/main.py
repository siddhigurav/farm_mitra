from fastapi import FastAPI, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from app.core.config import settings
from app.api import routes, ws
from app.mqtt_worker import MQTTIngestor
from app.db import session
from app.db.base import Base
from sqlalchemy import create_engine


def create_app() -> FastAPI:
    app = FastAPI(title="IoT Agriculture Backend")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    app.include_router(routes.router, prefix="/api/v1")

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await ws.manager.connect(websocket)
        try:
            while True:
                _ = await websocket.receive_text()
        except Exception:
            ws.manager.disconnect(websocket)

    return app


app = create_app()


def start_mqtt():
    ingestor = MQTTIngestor()
    ingestor.start()


if __name__ == "__main__":
    # ensure DB tables exist (in production use alembic migrations)
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    logging.info("Starting MQTT ingestor")
    start_mqtt()
    uvicorn.run(app, host="0.0.0.0", port=8000)
