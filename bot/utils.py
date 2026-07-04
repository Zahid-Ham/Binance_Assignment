"""General helper functions and utility utilities for formatting, conversions, and string processing."""

import time
import uuid
from typing import Any, Union


def get_current_timestamp() -> int:
    """Get the current epoch time in milliseconds.

    Returns:
        int: Current timestamp in milliseconds.
    """
    return int(time.time() * 1000)


def pretty_divider(char: str = "=", length: int = 50) -> str:
    """Generate a clean divider string of a specified character and length.

    Args:
        char: The character to repeat. Defaults to "=".
        length: The length of the divider. Defaults to 50.

    Returns:
        str: Repeated character string.
    """
    return char * length


def format_currency(value: Union[float, int], symbol: str = "$") -> str:
    """Format a numeric value as a currency string.

    Args:
        value: Numeric value to format.
        symbol: The currency symbol to prepend. Defaults to "$".

    Returns:
        str: Currency formatted string (e.g. "$1,234.56").
    """
    try:
        return f"{symbol}{float(value):,.2f}"
    except (ValueError, TypeError):
        return f"{symbol}0.00"


def format_quantity(value: Union[float, int], precision: int = 3) -> str:
    """Format a numeric quantity value with fixed precision.

    Args:
        value: Numeric value to format.
        precision: Number of decimal places. Defaults to 3.

    Returns:
        str: Precision formatted string.
    """
    try:
        return f"{float(value):.{precision}f}"
    except (ValueError, TypeError):
        return f"{0.0:.{precision}f}"


def safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert a value to a float, falling back to a default value.

    Args:
        value: Input value to convert.
        default: Default float value on failure. Defaults to 0.0.

    Returns:
        float: Converted float value.
    """
    try:
        if value is None:
            return default
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    """Safely convert a value to an integer, falling back to a default value.

    Args:
        value: Input value to convert.
        default: Default integer value on failure. Defaults to 0.

    Returns:
        int: Converted integer value.
    """
    try:
        if value is None:
            return default
        return int(float(value))
    except (ValueError, TypeError):
        return default


def generate_request_id() -> str:
    """Generate a unique request ID for tracing API requests.

    Returns:
        str: Unique UUID string.
    """
    return str(uuid.uuid4())


def print_section_title(title: str, char: str = "=") -> None:
    """Print a visually prominent section title to console.

    Args:
        title: The title message to print.
        char: The character to use for the borders. Defaults to "=".
    """
    border = pretty_divider(char, len(title) + 8)
    print(f"\n{border}")
    print(f"{char}   {title}   {char}")
    print(f"{border}\n")


def mask_api_key(key: str, visible_chars: int = 4) -> str:
    """Mask sensitive API keys, displaying only a limited set of characters.

    Args:
        key: The key string to mask.
        visible_chars: Number of visible characters at start/end. Defaults to 4.

    Returns:
        str: Masked string (e.g. "ABCD...WXYZ" or "********" if short).
    """
    if not key:
        return "Not Set"
    key_len = len(key)
    if key_len <= visible_chars * 2:
        return "*" * key_len
    return f"{key[:visible_chars]}...{key[-visible_chars:]}"
