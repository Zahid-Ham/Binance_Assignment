"""Binance Futures API Client Wrapper.

Manages connections, authentication, retries, exception translation,
performance instrumentation, and structured responses.
"""

import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional
from binance.client import Client
from binance.exceptions import BinanceAPIException
from requests.exceptions import RequestException

from bot.config import Settings
from bot.constants import DEFAULT_TIMEOUT_SECONDS, MAXIMUM_RETRIES, RETRY_DELAY_SECONDS
from bot.exceptions import (
    APIException,
    AuthenticationException,
    NetworkException,
    RateLimitException,
)
from bot.logging_config import get_logger
from bot.utils import mask_api_key

logger = get_logger("BinanceClient")


@dataclass(frozen=True)
class ServerTimeResponse:
    """Structured container for server time."""
    server_time_ms: int


@dataclass(frozen=True)
class AssetBalance:
    """Structured container for asset balance."""
    asset: str
    wallet_balance: float
    unrealized_pnl: float


@dataclass(frozen=True)
class PositionInfo:
    """Structured container for position status."""
    symbol: str
    position_amt: float
    entry_price: float
    unrealized_pnl: float
    leverage: int


@dataclass(frozen=True)
class AccountInfoResponse:
    """Structured container for account information."""
    can_trade: bool
    total_wallet_balance: float
    assets: List[AssetBalance]
    positions: List[PositionInfo]


@dataclass(frozen=True)
class OrderResponse:
    """Structured container for placed/retrieved order details."""
    order_id: int
    symbol: str
    status: str
    client_order_id: str
    price: float
    avg_price: float
    orig_qty: float
    executed_qty: float
    side: str
    type: str
    update_time_ms: int


class BinanceClient:
    """Production-ready client wrapper for Binance Futures Testnet."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the BinanceClient.

        Args:
            settings: Loaded configuration parameters.
        """
        self.api_key = settings.BINANCE_API_KEY.get_secret_value()
        self.secret_key = settings.BINANCE_SECRET_KEY.get_secret_value()
        self.base_url = settings.BASE_URL
        self._client: Optional[Client] = None

        logger.info(
            f"Initializing BinanceClient with Key: {mask_api_key(self.api_key)} "
            f"and Host: {self.base_url}"
        )

    def connect(self) -> None:
        """Establish connection using python-binance client with Testnet enabled.

        Raises:
            AuthenticationException: If client initialization fails.
        """
        try:
            logger.info("Initializing python-binance Client...")
            # We initialize with testnet=True to match requirements
            self._client = Client(
                api_key=self.api_key,
                api_secret=self.secret_key,
                testnet=True,
            )
            # Override base endpoints if config sets a custom URL
            if self.base_url:
                self._client.FUTURES_URL = self.base_url

            logger.info("Client connected. Verifying connection via ping...")
            self.ping()
        except (BinanceAPIException, RequestException, Exception) as e:
            logger.error(f"Failed to connect or ping: {e}")
            raise AuthenticationException(f"Connection setup failed: {e}") from e

    def _execute_request(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Execute request with retries, latency instrumentation, and error handling.

        Args:
            func: python-binance API function.
            *args: Arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            The raw response dictionary from the exchange.
        """
        method_name = getattr(func, "__name__", str(func))
        logger.debug(f"Request: {method_name} - args: {args}, kwargs: {kwargs}")

        attempt = 0
        while attempt < MAXIMUM_RETRIES:
            attempt += 1
            start_time = time.perf_counter()
            try:
                # Execute request
                response = func(*args, **kwargs)
                latency = (time.perf_counter() - start_time) * 1000
                logger.info(f"Response: {method_name} received in {latency:.2f}ms")
                logger.debug(f"Response Payload: {response}")
                return response
            except BinanceAPIException as e:
                latency = (time.perf_counter() - start_time) * 1000
                logger.warning(
                    f"Binance API Error on {method_name} (code={e.code}) in {latency:.2f}ms: {e.message}"
                )
                # Map credentials error codes: -1022 (Signature), -2014, -2015 (API Key)
                if e.code in (-1022, -2014, -2015):
                    raise AuthenticationException(f"Binance authentication failed: {e.message}") from e
                # Map rate limit error codes: -1003, -1015, or HTTP 429
                if e.code in (-1003, -1015) or "429" in str(e.message):
                    raise RateLimitException(f"Binance rate limit hit: {e.message}") from e
                raise APIException(f"Binance API request failed: {e.message}") from e
            except RequestException as e:
                latency = (time.perf_counter() - start_time) * 1000
                logger.warning(
                    f"Network error on {method_name} in {latency:.2f}ms (Attempt {attempt}/{MAXIMUM_RETRIES}): {e}"
                )
                if attempt >= MAXIMUM_RETRIES:
                    logger.error(f"Network request exhausted all retries for: {method_name}")
                    raise NetworkException(f"Network request failed after {MAXIMUM_RETRIES} attempts: {e}") from e
                time.sleep(RETRY_DELAY_SECONDS)
            except Exception as e:
                logger.error(f"Unexpected request error in {method_name}: {e}")
                raise APIException(f"Unexpected error executing {method_name}: {e}") from e

    def ping(self) -> bool:
        """Ping the Binance Futures server.

        Returns:
            bool: True if server responded.
        """
        if not self._client:
            raise APIException("Client is not connected. Call connect() first.")
        self._execute_request(self._client.futures_ping)
        return True

    def server_time(self) -> int:
        """Fetch current Binance server time.

        Returns:
            int: Server time in epoch milliseconds.
        """
        if not self._client:
            raise APIException("Client is not connected. Call connect() first.")
        res = self._execute_request(self._client.futures_time)
        return int(res["serverTime"])

    def account_info(self) -> AccountInfoResponse:
        """Fetch account balances and active positions on Futures.

        Returns:
            AccountInfoResponse: Object with balance and position status.
        """
        if not self._client:
            raise APIException("Client is not connected. Call connect() first.")
        res = self._execute_request(self._client.futures_account)

        # Parse assets list
        assets: List[AssetBalance] = []
        for asset in res.get("assets", []):
            wallet_bal = float(asset.get("walletBalance", 0.0))
            if wallet_bal > 0:  # Only track assets with positive balance
                assets.append(
                    AssetBalance(
                        asset=asset["asset"],
                        wallet_balance=wallet_bal,
                        unrealized_pnl=float(asset.get("unrealizedProfit", 0.0)),
                    )
                )

        # Parse positions list
        positions: List[PositionInfo] = []
        for pos in res.get("positions", []):
            qty = float(pos.get("positionAmt", 0.0))
            if qty != 0:  # Only track active positions
                positions.append(
                    PositionInfo(
                        symbol=pos["symbol"],
                        position_amt=qty,
                        entry_price=float(pos.get("entryPrice", 0.0)),
                        unrealized_pnl=float(pos.get("unrealizedProfit", 0.0)),
                        leverage=int(pos.get("leverage", 1)),
                    )
                )

        return AccountInfoResponse(
            can_trade=res.get("canTrade", False),
            total_wallet_balance=float(res.get("totalWalletBalance", 0.0)),
            assets=assets,
            positions=positions,
        )

    def place_market_order(self, symbol: str, side: str, quantity: float) -> OrderResponse:
        """Place a market order on Binance Futures.

        Args:
            symbol: Trading pair (e.g. BTCUSDT).
            side: BUY or SELL.
            quantity: Amount of asset.

        Returns:
            OrderResponse: Details of the placed order.
        """
        if not self._client:
            raise APIException("Client is not connected. Call connect() first.")

        res = self._execute_request(
            self._client.futures_create_order,
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity,
        )
        return self._parse_order_response(res)

    def place_limit_order(
        self, symbol: str, side: str, quantity: float, price: float
    ) -> OrderResponse:
        """Place a limit order on Binance Futures.

        Args:
            symbol: Trading pair (e.g. BTCUSDT).
            side: BUY or SELL.
            quantity: Amount of asset.
            price: Order execution limit price.

        Returns:
            OrderResponse: Details of the placed order.
        """
        if not self._client:
            raise APIException("Client is not connected. Call connect() first.")

        res = self._execute_request(
            self._client.futures_create_order,
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=price,
            timeInForce="GTC",
        )
        return self._parse_order_response(res)

    def cancel_order(self, symbol: str, order_id: int) -> OrderResponse:
        """Cancel an active open order on Binance Futures.

        Args:
            symbol: Trading pair.
            order_id: Unique order ID.

        Returns:
            OrderResponse: Details of the cancelled order.
        """
        if not self._client:
            raise APIException("Client is not connected. Call connect() first.")

        res = self._execute_request(
            self._client.futures_cancel_order,
            symbol=symbol,
            orderId=order_id,
        )
        return self._parse_order_response(res)

    def get_order(self, symbol: str, order_id: int) -> OrderResponse:
        """Retrieve details of an order.

        Args:
            symbol: Trading pair.
            order_id: Unique order ID.

        Returns:
            OrderResponse: Details of the requested order.
        """
        if not self._client:
            raise APIException("Client is not connected. Call connect() first.")

        res = self._execute_request(
            self._client.futures_get_order,
            symbol=symbol,
            orderId=order_id,
        )
        return self._parse_order_response(res)

    def _parse_order_response(self, res: Dict[str, Any]) -> OrderResponse:
        """Helper to map a raw dict response to an OrderResponse object."""
        return OrderResponse(
            order_id=res["orderId"],
            symbol=res["symbol"],
            status=res["status"],
            client_order_id=res.get("clientOrderId", ""),
            price=float(res.get("price", 0.0)),
            avg_price=float(res.get("avgPrice", 0.0)),
            orig_qty=float(res.get("origQty", 0.0)),
            executed_qty=float(res.get("executedQty", 0.0)),
            side=res["side"],
            type=res["type"],
            update_time_ms=res.get("updateTime", 0),
        )
