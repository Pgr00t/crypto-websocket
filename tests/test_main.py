import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.state import latest_prices
from app.models import PriceUpdate

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Crypto Price WebSocket App is running"}

def test_read_price_empty():
    # Clear the state to test empty case
    latest_prices.clear()
    
    response = client.get("/price")
    assert response.status_code == 200
    assert response.json() == {"prices": {}}

def test_read_price_populated():
    # Populate state
    latest_prices["BTCUSDT"] = PriceUpdate(
        symbol="BTCUSDT",
        last_price="50000.00",
        price_change_percent_24h="2.5",
        timestamp=1700000000000
    )
    
    response = client.get("/price")
    assert response.status_code == 200
    data = response.json()
    assert "BTCUSDT" in data["prices"]
    assert data["prices"]["BTCUSDT"]["last_price"] == "50000.00"

def test_websocket():
    with client.websocket_connect("/ws") as websocket:
        # Since the server just keeps connection open, we check it stays open
        # We can send a message and it shouldn't close the connection immediately
        websocket.send_text("ping")
        # We don't expect a reply for the ping, but the connection being open means success so far.
