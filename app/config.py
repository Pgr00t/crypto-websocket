from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Centralized configuration for the FastAPI application.
    """
    binance_ws_url: str = (
        "wss://stream.binance.com:9443/stream?"
        "streams=btcusdt@ticker/ethusdt@ticker/bnbusdt@ticker"
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
