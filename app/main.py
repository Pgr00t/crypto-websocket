from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import logging
from .binance import start_binance_listener
from .connection_manager import manager
from .state import latest_prices

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the lifecycle events of the FastAPI application.
    Starts the Binance WebSocket listener upon startup.
    """
    logger.info("Starting Binance WebSocket listener...")
    await start_binance_listener()
    yield
    logger.info("Shutting down...")

app = FastAPI(lifespan=lifespan, title="Crypto Price WebSocket API")

@app.get("/")
async def root():
    """
    Health check endpoint to verify the API server status.
    """
    return {"message": "Crypto Price WebSocket App is running"}

@app.get("/price")
async def get_price():
    """
    Retrieves the most recent cryptocurrency prices from the local cache.
    """
    return {
        "prices": {
            symbol: price_data.model_dump() 
            for symbol, price_data in latest_prices.items()
        }
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Establishes and maintains a WebSocket connection with a client.
    Listens for disconnect events to properly manage active connections.
    """
    await manager.connect(websocket)
    try:
        while True:
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
        await manager.disconnect(websocket)
