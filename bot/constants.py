from enum import Enum


class OrderSide(str, Enum):
    """Buy or Sell side of a trade."""
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    """Supported Binance Futures order types."""
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP_LOSS = "STOP"
    STOP_LOSS_LIMIT = "STOP_MARKET"
    TAKE_PROFIT = "TAKE_PROFIT"
    TAKE_PROFIT_LIMIT = "TAKE_PROFIT_MARKET"


class PositionSide(str, Enum):
    """Position side for hedge mode vs one-way mode."""
    BOTH = "BOTH"
    LONG = "LONG"
    SHORT = "SHORT"


class TimeInForce(str, Enum):
    """Order time in force configurations."""
    GTC = "GTC"  # Good Till Cancelled
    IOC = "IOC"  # Immediate Or Cancel
    FOK = "FOK"  # Fill Or Kill
    GTX = "GTX"  # Good Till Crossing (Post Only)


class KlinesInterval(str, Enum):
    """Candlestick/K-line intervals."""
    MIN_1 = "1m"
    MIN_3 = "3m"
    MIN_5 = "5m"
    MIN_15 = "15m"
    MIN_30 = "30m"
    HOUR_1 = "1h"
    HOUR_2 = "2h"
    HOUR_4 = "4h"
    HOUR_6 = "6h"
    HOUR_8 = "8h"
    HOUR_12 = "12h"
    DAY_1 = "1d"
    DAY_3 = "3d"
    WEEK_1 = "1w"
    MONTH_1 = "1M"


# Default Futures endpoints or configuration keys
DEFAULT_SYMBOL = "BTCUSDT"
DEFAULT_LEVERAGE = 1
