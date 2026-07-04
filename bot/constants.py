"""Global constants and configuration settings for the Trading Bot."""

from typing import Final, Set

# Application Metadata
APP_NAME: Final[str] = "Binance Futures Testnet Trading Bot"
VERSION: Final[str] = "1.0.0"

# Supported Trading Symbols
SUPPORTED_SYMBOLS: Final[Set[str]] = {
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
}

# Supported Order Types
ORDER_TYPE_LIMIT: Final[str] = "LIMIT"
ORDER_TYPE_MARKET: Final[str] = "MARKET"

SUPPORTED_ORDER_TYPES: Final[Set[str]] = {
    ORDER_TYPE_LIMIT,
    ORDER_TYPE_MARKET,
}

# Supported Sides
SIDE_BUY: Final[str] = "BUY"
SIDE_SELL: Final[str] = "SELL"

SUPPORTED_SIDES: Final[Set[str]] = {
    SIDE_BUY,
    SIDE_SELL,
}

# Network and API defaults
DEFAULT_TIMEOUT_SECONDS: Final[float] = 10.0
MAXIMUM_RETRIES: Final[int] = 5
RETRY_DELAY_SECONDS: Final[float] = 2.0
