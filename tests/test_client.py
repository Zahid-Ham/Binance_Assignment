import pytest
from unittest.mock import MagicMock, patch
from requests.exceptions import ReadTimeout

from bot.config import Settings
from bot.client import BinanceClient, AccountInfoResponse, OrderResponse
from bot.exceptions import (
    APIException,
    AuthenticationException,
    NetworkException,
    RateLimitException,
)
from binance.exceptions import BinanceAPIException


@pytest.fixture
def mock_settings():
    return Settings(
        BINANCE_API_KEY="test_api_key_1234567890",
        BINANCE_SECRET_KEY="test_secret_key_1234567890",
        BASE_URL="https://testnet.binancefuture.com",
    )


@patch("bot.client.Client")
def test_connect_success(mock_binance_client_class, mock_settings):
    # Setup mock Client instance
    mock_instance = MagicMock()
    mock_binance_client_class.return_value = mock_instance
    mock_instance.futures_ping.return_value = {}

    client = BinanceClient(mock_settings)
    client.connect()

    assert client._client is not None
    mock_instance.futures_ping.assert_called_once()


@patch("bot.client.Client")
def test_connect_failure(mock_binance_client_class, mock_settings):
    mock_instance = MagicMock()
    mock_binance_client_class.return_value = mock_instance
    mock_instance.futures_ping.side_effect = BinanceAPIException(
        MagicMock(status_code=401), -2015, "Invalid API-key, IP, or permissions."
    )

    client = BinanceClient(mock_settings)
    with pytest.raises(AuthenticationException):
        client.connect()


@patch("bot.client.Client")
def test_ping_success(mock_binance_client_class, mock_settings):
    mock_instance = MagicMock()
    mock_binance_client_class.return_value = mock_instance
    mock_instance.futures_ping.return_value = {}

    client = BinanceClient(mock_settings)
    client.connect()
    assert client.ping() is True


@patch("bot.client.Client")
def test_server_time(mock_binance_client_class, mock_settings):
    mock_instance = MagicMock()
    mock_binance_client_class.return_value = mock_instance
    mock_instance.futures_time.return_value = {"serverTime": 1600000000000}

    client = BinanceClient(mock_settings)
    client.connect()
    assert client.server_time() == 1600000000000


@patch("bot.client.Client")
def test_account_info(mock_binance_client_class, mock_settings):
    mock_instance = MagicMock()
    mock_binance_client_class.return_value = mock_instance
    mock_instance.futures_account.return_value = {
        "canTrade": True,
        "totalWalletBalance": "5000.50",
        "assets": [
            {"asset": "USDT", "walletBalance": "5000.50", "unrealizedProfit": "10.00"},
            {"asset": "BUSD", "walletBalance": "0.00", "unrealizedProfit": "0.00"},
        ],
        "positions": [
            {
                "symbol": "BTCUSDT",
                "positionAmt": "0.25",
                "entryPrice": "30000.00",
                "unrealizedProfit": "15.00",
                "leverage": "5",
            },
            {
                "symbol": "ETHUSDT",
                "positionAmt": "0.00",
                "entryPrice": "0.00",
                "unrealizedProfit": "0.00",
                "leverage": "10",
            },
        ],
    }

    client = BinanceClient(mock_settings)
    client.connect()
    info = client.account_info()

    assert isinstance(info, AccountInfoResponse)
    assert info.can_trade is True
    assert info.total_wallet_balance == 5000.50
    assert len(info.assets) == 1
    assert info.assets[0].asset == "USDT"
    assert info.assets[0].wallet_balance == 5000.50
    assert len(info.positions) == 1
    assert info.positions[0].symbol == "BTCUSDT"
    assert info.positions[0].position_amt == 0.25


@patch("bot.client.Client")
def test_place_market_order(mock_binance_client_class, mock_settings):
    mock_instance = MagicMock()
    mock_binance_client_class.return_value = mock_instance
    mock_instance.futures_create_order.return_value = {
        "orderId": 98765,
        "symbol": "BTCUSDT",
        "status": "FILLED",
        "clientOrderId": "custom_id",
        "price": "0.0",
        "avgPrice": "31000.0",
        "origQty": "0.1",
        "executedQty": "0.1",
        "side": "BUY",
        "type": "MARKET",
        "updateTime": 1600000005000,
    }

    client = BinanceClient(mock_settings)
    client.connect()
    order = client.place_market_order("BTCUSDT", "BUY", 0.1)

    assert isinstance(order, OrderResponse)
    assert order.order_id == 98765
    assert order.status == "FILLED"
    assert order.avg_price == 31000.0


@patch("bot.client.Client")
def test_network_failure_retry_exhausted(mock_binance_client_class, mock_settings):
    mock_instance = MagicMock()
    mock_binance_client_class.return_value = mock_instance
    # Simulate network failures continuously
    mock_instance.futures_ping.side_effect = ReadTimeout("Timeout reached")

    client = BinanceClient(mock_settings)
    client._client = mock_instance

    # Mock sleeping so tests run instantly
    with patch("time.sleep", return_value=None):
        with pytest.raises(NetworkException):
            client.ping()

    # Verify futures_ping was called up to MAXIMUM_RETRIES (5 times)
    assert mock_instance.futures_ping.call_count == 5
