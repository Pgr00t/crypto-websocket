from pydantic import BaseModel, ConfigDict

class PriceUpdate(BaseModel):
    """
    Data model representing a cryptocurrency price update.
    """
    symbol: str
    last_price: str
    price_change_percent_24h: str
    timestamp: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "symbol": "BTCUSDT",
                "last_price": "43000.50",
                "price_change_percent_24h": "1.25",
                "timestamp": 1700000000000
            }
        }
    )
