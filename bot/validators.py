"""
Input and risk management validation helpers.
Ensures trade sizes, leverage, symbol formats, and constraints comply before API transmission.
"""

from loguru import logger
from bot.exceptions import ValidationError


def validate_symbol(symbol: str) -> None:
    """
    Validate if the symbol follows Binance guidelines (e.g., BTCUSDT).

    Args:
        symbol: The trading symbol string.

    Raises:
        ValidationError: If format is invalid.
    """
    if not symbol or not symbol.isupper() or len(symbol) < 5:
        raise ValidationError(f"Invalid symbol format: {symbol}. Must be uppercase, e.g., 'BTCUSDT'.")
    logger.debug(f"Symbol {symbol} validated.")


def validate_leverage(leverage: int) -> None:
    """
    Validate leverage is within the allowed futures range (1 - 125).

    Args:
        leverage: Integer representing the leverage multiplier.

    Raises:
        ValidationError: If leverage exceeds limits.
    """
    if not (1 <= leverage <= 125):
        raise ValidationError(f"Leverage {leverage} out of bounds. Must be between 1 and 125.")
    logger.debug(f"Leverage {leverage} validated.")


def validate_trade_amount(amount: float) -> None:
    """
    Validate amount is positive.

    Args:
        amount: Quantity of asset to trade.

    Raises:
        ValidationError: If quantity is non-positive.
    """
    if amount <= 0:
        raise ValidationError(f"Trade amount must be strictly greater than 0. Got: {amount}")
