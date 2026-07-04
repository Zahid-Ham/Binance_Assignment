class TradingBotException(Exception):
    """Base exception class for all errors in the trading bot."""
    pass


class ConfigurationError(TradingBotException):
    """Raised when there is an issue with configuration or environment variables."""
    pass


class APIConnectionError(TradingBotException):
    """Raised when the bot fails to connect to the Binance API."""
    pass


class AuthenticationError(APIConnectionError):
    """Raised when the API key or secret validation fails."""
    pass


class OrderExecutionError(TradingBotException):
    """Raised when an order placement or cancellation fails on Binance."""
    pass


class ValidationError(TradingBotException):
    """Raised when inputs or trade constraints fail validation checks."""
    pass


class MarketDataError(TradingBotException):
    """Raised when market data retrieval or parsing fails."""
    pass
