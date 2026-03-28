import asyncio
import json
import logging
import websockets
from websockets.exceptions import ConnectionClosed
from .state import latest_prices
from .models import PriceUpdate
from .connection_manager import manager
from .config import settings

logger = logging.getLogger(__name__)

async def connect_to_binance():
    """
    Establishes a WebSocket connection to Binance, receives ticker streams,
    parses the JSON payload, and updates the global cache.
    """
    while True:
        try:
            logger.info(f"Connecting to Binance WebSocket: {settings.binance_ws_url}")
            async with websockets.connect(settings.binance_ws_url) as ws:
                logger.info("Connected to Binance WebSocket.")
                while True:
                    message_str = await ws.recv()
                    message = json.loads(message_str)
                    
                    if "data" in message:
                        data = message["data"]
                        symbol = data.get("s")
                        last_price = data.get("c")
                        price_change = data.get("P")
                        timestamp = data.get("E")
                        
                        if symbol and last_price and price_change and timestamp:
                            update = PriceUpdate(
                                symbol=symbol,
                                last_price=last_price,
                                price_change_percent_24h=price_change,
                                timestamp=timestamp
                            )
                            latest_prices[symbol] = update
                            await manager.broadcast(update.model_dump())
                    
        except ConnectionClosed:
            logger.warning("Binance WebSocket connection closed. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            logger.error(f"Error in Binance WebSocket listener: {e}")
            await asyncio.sleep(5)

async def start_binance_listener():
    """
    Creates an asyncio background task for the Binance WebSocket listener.
    """
    asyncio.create_task(connect_to_binance())
