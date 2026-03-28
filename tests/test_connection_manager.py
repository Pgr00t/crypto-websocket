import pytest
import asyncio
from unittest.mock import AsyncMock
from app.connection_manager import ConnectionManager

@pytest.fixture
def manager():
    return ConnectionManager()

@pytest.fixture
def mock_websocket():
    ws = AsyncMock()
    # Mock simple state if needed, but not strictly required by manager
    return ws

@pytest.mark.asyncio
async def test_connect(manager, mock_websocket):
    await manager.connect(mock_websocket)
    mock_websocket.accept.assert_awaited_once()
    assert len(manager.active_connections) == 1
    assert mock_websocket in manager.active_connections

@pytest.mark.asyncio
async def test_disconnect(manager, mock_websocket):
    await manager.connect(mock_websocket)
    assert len(manager.active_connections) == 1
    
    await manager.disconnect(mock_websocket)
    assert len(manager.active_connections) == 0

@pytest.mark.asyncio
async def test_broadcast(manager, mock_websocket):
    await manager.connect(mock_websocket)
    
    message = {"test": "data"}
    await manager.broadcast(message)
    
    mock_websocket.send_json.assert_awaited_once_with(message)

@pytest.mark.asyncio
async def test_broadcast_removes_dead_connections(manager, mock_websocket):
    # Setup mock to raise exception when sending
    mock_websocket.send_json.side_effect = Exception("Connection closed")
    
    await manager.connect(mock_websocket)
    assert len(manager.active_connections) == 1
    
    message = {"test": "data"}
    await manager.broadcast(message)
    
    # It should have failed and removed the connection
    assert len(manager.active_connections) == 0
