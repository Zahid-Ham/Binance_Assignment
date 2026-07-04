import pytest
from bot.exceptions import ValidationException
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    validate_trade_inputs,
)


def test_validate_symbol_valid():
    assert validate_symbol("BTCUSDT") == "BTCUSDT"
    assert validate_symbol("ETHUSDT") == "ETHUSDT"


def test_validate_symbol_invalid_case():
    with pytest.raises(ValidationException, match="Symbol must be uppercase only"):
        validate_symbol("btcusdt")


def test_validate_symbol_unsupported():
    with pytest.raises(ValidationException, match="Unsupported symbol"):
        validate_symbol("DOGEUSDT")


def test_validate_side_valid():
    assert validate_side("BUY") == "BUY"
    assert validate_side(" buy ") == "BUY"
    assert validate_side("SELL") == "SELL"


def test_validate_side_invalid():
    with pytest.raises(ValidationException, match="Invalid order side"):
        validate_side("HOLD")


def test_validate_order_type_valid():
    assert validate_order_type("LIMIT") == "LIMIT"
    assert validate_order_type(" market ") == "MARKET"


def test_validate_order_type_invalid():
    with pytest.raises(ValidationException, match="Invalid order type"):
        validate_order_type("STOP")


def test_validate_quantity_valid():
    assert validate_quantity("0.5") == 0.5
    assert validate_quantity(10.0, max_quantity=20) == 10.0


def test_validate_quantity_non_numeric():
    with pytest.raises(ValidationException, match="Quantity must be numeric"):
        validate_quantity("abc")


def test_validate_quantity_negative():
    with pytest.raises(ValidationException, match="Quantity must be positive"):
        validate_quantity(-1.5)


def test_validate_quantity_limit_exceeded():
    with pytest.raises(ValidationException, match="exceeds configured maximum limit"):
        validate_quantity(15.0, max_quantity=10.0)


def test_validate_price_valid():
    assert validate_price("1800.5", "LIMIT") == 1800.5
    assert validate_price(None, "MARKET") is None


def test_validate_price_missing_for_limit():
    with pytest.raises(ValidationException, match="Price is required for LIMIT orders"):
        validate_price(None, "LIMIT")


def test_validate_price_negative():
    with pytest.raises(ValidationException, match="Price must be positive"):
        validate_price("-5.0", "LIMIT")


def test_validate_trade_inputs_success():
    res = validate_trade_inputs(
        symbol="BTCUSDT",
        side="BUY",
        order_type="LIMIT",
        quantity=0.1,
        price=30000,
    )
    assert res.is_valid is True
    assert res.symbol == "BTCUSDT"
    assert res.side == "BUY"
    assert res.order_type == "LIMIT"
    assert res.quantity == 0.1
    assert res.price == 30000.0


def test_validate_trade_inputs_failure():
    res = validate_trade_inputs(
        symbol="BTCUSDT",
        side="BUY",
        order_type="LIMIT",
        quantity=-0.1,
        price=30000,
    )
    assert res.is_valid is False
    assert "Quantity must be positive" in res.error_message
