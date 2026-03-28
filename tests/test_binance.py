import pytest
import json
import asyncio
from unittest.mock import patch, AsyncMock
from app.binance import connect_to_binance
from app.state import latest_prices

@pytest.mark.asyncio
async def test_binance_listener_parses_data():
    # Mocking websockets.connect context manager
    mock_ws = AsyncMock()
    
    # Creating a sample combined stream payload that Binance sends
    sample_payload = {
        "stream": "btcusdt@ticker",
        "data": {
            "e": "24hrTicker",
            "E": 1700000000000,
            "s": "BTCUSDT",
            "p": "100.00",
            "P": "2.500",
            "c": "45000.00",
            "h": "46000.00",
            "l": "44000.00",
            "v": "1000.0"
        }
    }
    
    # Make recv() return our sample once, then raise an exception to break the inner loop
    mock_ws.recv.side_effect = [json.dumps(sample_payload), Exception("Stop inner loop")]
    
    mock_connect_context = AsyncMock()
    mock_connect_context.__aenter__.return_value = mock_ws
    
    with patch("websockets.connect", return_value=mock_connect_context):
        with patch("asyncio.sleep", side_effect=asyncio.CancelledError("Stop outer loop")):
            try:
                await connect_to_binance()
            except asyncio.CancelledError:
                pass
            
    # Check if state was updated
    assert "BTCUSDT" in latest_prices
    assert latest_prices["BTCUSDT"].last_price == "45000.00"
    assert latest_prices["BTCUSDT"].price_change_percent_24h == "2.500"
    assert latest_prices["BTCUSDT"].timestamp == 1700000000000
    
    # Clean up state for other tests
    latest_prices.clear()
