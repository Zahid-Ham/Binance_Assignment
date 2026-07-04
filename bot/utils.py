"""
General helper and utility functions for formatting and calculations.
"""

from typing import Union


def format_symbol(base: str, quote: str) -> str:
    """
    Format base and quote assets to a standard Binance symbol representation.

    Args:
        base: The base asset (e.g., 'btc').
        quote: The quote asset (e.g., 'usdt').

    Returns:
        Formatted uppercase string (e.g., 'BTCUSDT').
    """
    return f"{base.strip().upper()}{quote.strip().upper()}"


def calculate_profit_loss(
    entry_price: float, exit_price: float, quantity: float, is_long: bool
) -> float:
    """
    Calculate the profit or loss of a trade.

    Args:
        entry_price: Price at position entry.
        exit_price: Price at position exit.
        quantity: Size of the position.
        is_long: True if trade is long, False for short.

    Returns:
        Float value representing PnL.
    """
    if is_long:
        return (exit_price - entry_price) * quantity
    else:
        return (entry_price - exit_price) * quantity


def format_precision(value: Union[float, int], decimals: int = 2) -> str:
    """
    Format a number to a fixed string decimal precision.

    Args:
        value: Float or int value.
        decimals: Decimal places.

    Returns:
        String representation with correct decimal precision.
    """
    return f"{value:.{decimals}f}"
