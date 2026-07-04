import pytest
from unittest.mock import MagicMock

from bot.client import BinanceClient, OrderResponse
from bot.orders import OrderService, OrderResult
from bot.exceptions import APIException, ValidationException


@pytest.fixture
def mock_client():
    return MagicMock(spec=BinanceClient)


def test_place_market_order_success(mock_client):
    # Setup mock response
    mock_order_response = OrderResponse(
        order_id=12345,
        symbol="BTCUSDT",
        status="NEW",
        client_order_id="test_id",
        price=0.0,
        avg_price=0.0,
        orig_qty=0.5,
        executed_qty=0.0,
        side="BUY",
        type="MARKET",
        update_time_ms=1600000000000,
    )
    mock_client.place_market_order.return_value = mock_order_response

    service = OrderService(mock_client)
    res = service.place_market_order("BTCUSDT", "BUY", 0.5)

    assert isinstance(res, OrderResult)
    assert res.is_success is True
    assert "SUCCESS" in res.message
    assert "Order Request: MARKET BUY - Symbol: BTCUSDT, Qty: 0.5" in res.order_summary
    assert "ID: 12345" in res.execution_summary
    assert res.order_details == mock_order_response
    mock_client.place_market_order.assert_called_once_with(
        symbol="BTCUSDT", side="BUY", quantity=0.5
    )


def test_place_market_order_validation_failure(mock_client):
    service = OrderService(mock_client)
    # Using negative quantity
    res = service.place_market_order("BTCUSDT", "BUY", -0.5)

    assert isinstance(res, OrderResult)
    assert res.is_success is False
    assert "FAILED" in res.message
    assert "Quantity must be positive" in res.message
    # Verify the client was NEVER called
    mock_client.place_market_order.assert_not_called()


def test_place_limit_order_success(mock_client):
    mock_order_response = OrderResponse(
        order_id=54321,
        symbol="ETHUSDT",
        status="NEW",
        client_order_id="limit_id",
        price=1800.0,
        avg_price=0.0,
        orig_qty=2.0,
        executed_qty=0.0,
        side="SELL",
        type="LIMIT",
        update_time_ms=1600000000000,
    )
    mock_client.place_limit_order.return_value = mock_order_response

    service = OrderService(mock_client)
    res = service.place_limit_order("ETHUSDT", "SELL", 2.0, 1800.0)

    assert isinstance(res, OrderResult)
    assert res.is_success is True
    assert "SUCCESS" in res.message
    assert "Order Request: LIMIT SELL - Symbol: ETHUSDT, Qty: 2.0 @ Price: 1800.0" in res.order_summary
    mock_client.place_limit_order.assert_called_once_with(
        symbol="ETHUSDT", side="SELL", quantity=2.0, price=1800.0
    )


def test_place_limit_order_api_failure(mock_client):
    mock_client.place_limit_order.side_effect = APIException("Binance order placement rejected.")

    service = OrderService(mock_client)
    res = service.place_limit_order("BTCUSDT", "BUY", 0.1, 30000.0)

    assert isinstance(res, OrderResult)
    assert res.is_success is False
    assert "FAILED" in res.message
    assert "Binance order placement rejected." in res.message
    assert "API Exception:" in res.execution_summary
