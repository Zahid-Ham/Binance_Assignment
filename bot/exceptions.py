"""Custom exceptions hierarchy for the Trading Bot.

All exception classes derive from TradingBotException and define
default informative messages.
"""


class TradingBotException(Exception):
    """Base exception class for all errors in the trading bot.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self, message: str = "A generic trading bot error occurred.") -> None:
        super().__init__(message)
        self.message = message


class ConfigurationException(TradingBotException):
    """Raised when configuration variables are missing, malformed, or invalid."""

    def __init__(self, message: str = "Configuration validation failed.") -> None:
        super().__init__(message)


class ValidationException(TradingBotException):
    """Raised when trading inputs (price, quantity, symbol) fail validation."""

    def __init__(self, message: str = "Validation of trade input failed.") -> None:
        super().__init__(message)


class APIException(TradingBotException):
    """Raised when the exchange API returns a failure response."""

    def __init__(self, message: str = "Exchange API returned an error.") -> None:
        super().__init__(message)


class NetworkException(TradingBotException):
    """Raised when network failures or timeouts occur while communicating with the exchange."""

    def __init__(self, message: str = "Network connection failed or timed out.") -> None:
        super().__init__(message)


class OrderPlacementException(TradingBotException):
    """Raised when placing, adjusting, or cancelling an order on the exchange fails."""

    def __init__(self, message: str = "Order execution failed.") -> None:
        super().__init__(message)


class AuthenticationException(TradingBotException):
    """Raised when exchange API key, secret, or signature authentication fails."""

    def __init__(self, message: str = "Authentication with exchange API failed.") -> None:
        super().__init__(message)


class RateLimitException(TradingBotException):
    """Raised when API request rate limits are hit or the bot is temporarily banned."""

    def __init__(self, message: str = "Exchange API rate limit exceeded.") -> None:
        super().__init__(message)
