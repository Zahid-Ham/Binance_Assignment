"""Validation module for Binance Futures trading inputs.

Defines validation rules, normalization logic, and exception handlers for symbols,
sides, order types, quantities, and prices.
"""

from dataclasses import dataclass
from typing import Any, Optional, Union
from loguru import logger
from bot.constants import SUPPORTED_ORDER_TYPES, SUPPORTED_SIDES, SUPPORTED_SYMBOLS, ORDER_TYPE_LIMIT
from bot.exceptions import ValidationException


@dataclass(frozen=True)
class ValidationResult:
    """Dataclass holding validation outcome and normalized parameters."""
    is_valid: bool
    error_message: str = ""
    symbol: str = ""
    side: str = ""
    order_type: str = ""
    quantity: float = 0.0
    price: Optional[float] = None


def normalize_input(value: Any) -> str:
    """Normalize input strings by removing whitespace and converting to uppercase.

    Args:
        value: Any stringable input value.

    Returns:
        str: Normalized, trimmed uppercase string.
    """
    if value is None:
        return ""
    return str(value).strip().upper()


def validate_symbol(symbol: str) -> str:
    """Validate and normalize the trading symbol.

    Args:
        symbol: The currency pair symbol (e.g. BTCUSDT).

    Returns:
        str: The validated and normalized symbol.

    Raises:
        ValidationException: If symbol is invalid or unsupported.
    """
    normalized = normalize_input(symbol)

    # Check case rule: Reject if the input symbol itself was not already uppercase
    if symbol != symbol.strip().upper():
        logger.warning(f"Symbol validation failed: '{symbol}' contains lowercase characters.")
        raise ValidationException("Symbol must be uppercase only.")

    if normalized not in SUPPORTED_SYMBOLS:
        logger.warning(f"Symbol validation failed: '{normalized}' is not supported.")
        raise ValidationException(
            f"Unsupported symbol: {normalized}. Allowed symbols: {', '.join(SUPPORTED_SYMBOLS)}"
        )

    return normalized


def validate_side(side: str) -> str:
    """Validate and normalize the order side.

    Args:
        side: The trade side (e.g. BUY or SELL).

    Returns:
        str: Validated side string.

    Raises:
        ValidationException: If side is invalid.
    """
    normalized = normalize_input(side)
    if normalized not in SUPPORTED_SIDES:
        logger.warning(f"Side validation failed: '{side}' is invalid.")
        raise ValidationException(
            f"Invalid order side: {normalized}. Allowed: {', '.join(SUPPORTED_SIDES)}"
        )
    return normalized


def validate_order_type(order_type: str) -> str:
    """Validate and normalize the order type.

    Args:
        order_type: The type of the order (e.g. LIMIT or MARKET).

    Returns:
        str: Validated order type.

    Raises:
        ValidationException: If order type is invalid.
    """
    normalized = normalize_input(order_type)
    if normalized not in SUPPORTED_ORDER_TYPES:
        logger.warning(f"Order type validation failed: '{order_type}' is invalid.")
        raise ValidationException(
            f"Invalid order type: {normalized}. Allowed: {', '.join(SUPPORTED_ORDER_TYPES)}"
        )
    return normalized


def validate_quantity(quantity: Any, max_quantity: float = 100.0) -> float:
    """Validate and normalize the order quantity.

    Args:
        quantity: The size or amount of currency to trade.
        max_quantity: Maximum allowable quantity limit.

    Returns:
        float: Validated float quantity.

    Raises:
        ValidationException: If quantity is non-numeric, negative, or exceeds maximum.
    """
    try:
        val = float(quantity)
    except (ValueError, TypeError) as e:
        logger.warning(f"Quantity validation failed: '{quantity}' is not numeric.")
        raise ValidationException("Quantity must be numeric.") from e

    if val <= 0:
        logger.warning(f"Quantity validation failed: {val} is not positive.")
        raise ValidationException("Quantity must be positive.")

    if val > max_quantity:
        logger.warning(f"Quantity validation failed: {val} exceeds limit of {max_quantity}.")
        raise ValidationException(f"Quantity {val} exceeds configured maximum limit of {max_quantity}.")

    return val


def validate_price(price: Any, order_type: str) -> Optional[float]:
    """Validate and normalize the order price.

    Args:
        price: Price of the asset. Only required for LIMIT orders.
        order_type: Normalized order type string.

    Returns:
        Optional[float]: Validated price or None if not applicable.

    Raises:
        ValidationException: If price is missing for LIMIT or is invalid.
    """
    norm_type = normalize_input(order_type)

    if norm_type == ORDER_TYPE_LIMIT:
        if price is None:
            logger.warning("Price validation failed: Price is required for LIMIT orders.")
            raise ValidationException("Price is required for LIMIT orders.")
        try:
            val = float(price)
        except (ValueError, TypeError) as e:
            logger.warning(f"Price validation failed: '{price}' is not numeric.")
            raise ValidationException("Price must be numeric.") from e

        if val <= 0:
            logger.warning(f"Price validation failed: {val} is not positive.")
            raise ValidationException("Price must be positive.")
        return val

    # For MARKET orders, price is not required
    return None


def validate_trade_inputs(
    symbol: str,
    side: str,
    order_type: str,
    quantity: Any,
    price: Any = None,
    max_quantity: float = 100.0,
) -> ValidationResult:
    """Orchestrate and validate all trade inputs, returning a unified ValidationResult.

    Args:
        symbol: The currency pair.
        side: BUY or SELL.
        order_type: LIMIT or MARKET.
        quantity: Order quantity.
        price: Order price.
        max_quantity: Max quantity constraint.

    Returns:
        ValidationResult: The result containing status and normalized data.
    """
    try:
        norm_symbol = validate_symbol(symbol)
        norm_side = validate_side(side)
        norm_type = validate_order_type(order_type)
        norm_qty = validate_quantity(quantity, max_quantity)
        norm_price = validate_price(price, norm_type)

        return ValidationResult(
            is_valid=True,
            symbol=norm_symbol,
            side=norm_side,
            order_type=norm_type,
            quantity=norm_qty,
            price=norm_price,
        )
    except ValidationException as e:
        return ValidationResult(is_valid=False, error_message=e.message)


if __name__ == "__main__":
    # Examples showing validators in action
    print("=== Validation System Examples ===")

    # 1. Validating symbol
    try:
        print(f"Normalizing 'BTCUSDT': {validate_symbol('BTCUSDT')}")
        validate_symbol("btcusdt")  # Will fail case check
    except ValidationException as ex:
        print(f"Expected failure for 'btcusdt': {ex}")

    # 2. Validating side
    try:
        print(f"Normalizing ' buy ': {validate_side(' buy ')}")
    except ValidationException as ex:
        print(f"Failed to validate side: {ex}")

    # 3. Validating quantity limits
    try:
        validate_quantity(150.0, max_quantity=100.0)
    except ValidationException as ex:
        print(f"Expected quantity limit failure: {ex}")

    # 4. Full trade input orchestrator
    res = validate_trade_inputs(
        symbol="ETHUSDT",
        side="SELL",
        order_type="LIMIT",
        quantity="1.25",
        price="1850.50",
    )
    print(f"Orchestrator Result: {res}")
