# Crypto Price WebSocket Project

This project connects to Binance's public WebSocket API to stream live crypto prices (BTC/USDT, ETH/USDT, BNB/USDT) and broadcasts them through its own local WebSocket server.

## Features
- Connects to Binance live tickers (`wss://stream.binance.com:9443/stream`).
- Exposes a local WebSocket endpoint `ws://localhost:8000/ws` that broadcasts all updates to connected clients.
- Exposes a REST API `GET /price` returning the latest snapshot of the tracked symbols.
- Handles connections gracefully using a custom `ConnectionManager` and background listener task.
- Fully tested using Pytest.

## Running Locally

### Prerequisites
- Python 3.10+
- `pip`

### Setup
1. Clone the repository and navigate into the project directory.
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```
3. Copy the example environment variables file and configure it:
   ```bash
   cp .env.example .env
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Running with Docker
1. Build and start the container:
   ```bash
   docker-compose up --build
   ```

## Testing the API
- **REST API:** 
  Open your browser or use `curl`: `http://localhost:8000/price`

- **WebSocket API:**
  You can connect to `ws://localhost:8000/ws` using a WebSocket testing tool (like Postman or a simple HTML/JS widget) to observe live broadcast messages.

## Running Unit Tests
1. Make sure `pytest` is installed (`pip install -r requirements.txt`).
2. Run standard tests:
   ```bash
   pytest tests/
   ```
