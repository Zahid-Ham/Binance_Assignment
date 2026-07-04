"""Order Service Orchestrator.

Orchestrates input validation, calls the Binance client API, logs progression,
and formats human-readable summaries and outcomes.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional
from loguru import logger

from bot.client import BinanceClient, OrderResponse
from bot.exceptions import TradingBotException
from bot.validators import validate_trade_inputs


@dataclass(frozen=True)
class OrderResult:
    """Structured container detailing the outcome of an order request."""
    is_success: bool
    message: str
    order_summary: str
    execution_summary: str
    order_details: Optional[OrderResponse] = None


class OrderService:
    """Service class for managing trade order validation and execution."""

    def __init__(self, client: BinanceClient) -> None:
        """Initialize the OrderService.

        Args:
            client: Dependency-injected Binance API client instance.
        """
        self.client = client
        logger.info("OrderService initialized with BinanceClient dependency.")

    def place_market_order(self, symbol: str, side: str, quantity: float) -> OrderResult:
        """Place a MARKET order on Binance Futures after validating inputs.

        Args:
            symbol: Trading symbol (e.g. BTCUSDT).
            side: Order side (BUY or SELL).
            quantity: Order quantity.

        Returns:
            OrderResult: The formatted result of the trade execution.
        """
        logger.info(f"Received request for MARKET order: {side} {quantity} {symbol}")

        # 1. Validate Input
        logger.debug("Validating market order inputs...")
        val_res = validate_trade_inputs(
            symbol=symbol, side=side, order_type="MARKET", quantity=quantity
        )

        if not val_res.is_valid:
            error_msg = f"Market order input validation failed: {val_res.error_message}"
            logger.warning(error_msg)
            return OrderResult(
                is_success=False,
                message=f"FAILED: {val_res.error_message}",
                order_summary=self._generate_pre_execution_summary(
                    symbol, side, "MARKET", quantity, None
                ),
                execution_summary=error_msg,
            )

        logger.debug("Market order inputs validated successfully.")

        # Generate pre-execution summary
        order_summary = self._generate_pre_execution_summary(
            val_res.symbol, val_res.side, val_res.order_type, val_res.quantity, None
        )

        # 2. Execute Order via BinanceClient
        logger.info(f"Calling Binance API to execute MARKET order: {order_summary}")
        try:
            order_res = self.client.place_market_order(
                symbol=val_res.symbol,
                side=val_res.side,
                quantity=val_res.quantity,
            )
            success_msg = f"SUCCESS: Market order placed successfully. Order ID: {order_res.order_id}"
            execution_summary = self._generate_execution_summary(order_res)
            logger.info(success_msg)
            return OrderResult(
                is_success=True,
                message=success_msg,
                order_summary=order_summary,
                execution_summary=execution_summary,
                order_details=order_res,
            )
        except TradingBotException as e:
            fail_msg = f"FAILED: Order execution failed due to an application exception: {e.message}"
            logger.error(fail_msg)
            return OrderResult(
                is_success=False,
                message=fail_msg,
                order_summary=order_summary,
                execution_summary=f"API Exception: {e.message}",
            )
        except Exception as e:
            fail_msg = f"FAILED: Unexpected error executing order: {e}"
            logger.error(fail_msg)
            return OrderResult(
                is_success=False,
                message=fail_msg,
                order_summary=order_summary,
                execution_summary=f"Unexpected Error: {e}",
            )

    def place_limit_order(
        self, symbol: str, side: str, quantity: float, price: float
    ) -> OrderResult:
        """Place a LIMIT order on Binance Futures after validating inputs.

        Args:
            symbol: Trading symbol (e.g. BTCUSDT).
            side: Order side (BUY or SELL).
            quantity: Order quantity.
            price: Execution price constraint.

        Returns:
            OrderResult: The formatted result of the trade execution.
        """
        logger.info(f"Received request for LIMIT order: {side} {quantity} {symbol} @ {price}")

        # 1. Validate Input
        logger.debug("Validating limit order inputs...")
        val_res = validate_trade_inputs(
            symbol=symbol, side=side, order_type="LIMIT", quantity=quantity, price=price
        )

        if not val_res.is_valid:
            error_msg = f"Limit order input validation failed: {val_res.error_message}"
            logger.warning(error_msg)
            return OrderResult(
                is_success=False,
                message=f"FAILED: {val_res.error_message}",
                order_summary=self._generate_pre_execution_summary(
                    symbol, side, "LIMIT", quantity, price
                ),
                execution_summary=error_msg,
            )

        logger.debug("Limit order inputs validated successfully.")

        # Generate pre-execution summary
        order_summary = self._generate_pre_execution_summary(
            val_res.symbol, val_res.side, val_res.order_type, val_res.quantity, val_res.price
        )

        # 2. Execute Order via BinanceClient
        logger.info(f"Calling Binance API to execute LIMIT order: {order_summary}")
        try:
            # We assert val_res.price is float since validation passed
            assert val_res.price is not None
            order_res = self.client.place_limit_order(
                symbol=val_res.symbol,
                side=val_res.side,
                quantity=val_res.quantity,
                price=val_res.price,
            )
            success_msg = f"SUCCESS: Limit order placed successfully. Order ID: {order_res.order_id}"
            execution_summary = self._generate_execution_summary(order_res)
            logger.info(success_msg)
            return OrderResult(
                is_success=True,
                message=success_msg,
                order_summary=order_summary,
                execution_summary=execution_summary,
                order_details=order_res,
            )
        except TradingBotException as e:
            fail_msg = f"FAILED: Order execution failed due to an application exception: {e.message}"
            logger.error(fail_msg)
            return OrderResult(
                is_success=False,
                message=fail_msg,
                order_summary=order_summary,
                execution_summary=f"API Exception: {e.message}",
            )
        except Exception as e:
            fail_msg = f"FAILED: Unexpected error executing order: {e}"
            logger.error(fail_msg)
            return OrderResult(
                is_success=False,
                message=fail_msg,
                order_summary=order_summary,
                execution_summary=f"Unexpected Error: {e}",
            )

    def _generate_pre_execution_summary(
        self, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float]
    ) -> str:
        """Generate a description of the order requirements before placement."""
        price_str = f" @ Price: {price}" if price is not None else ""
        return f"Order Request: {order_type} {side} - Symbol: {symbol}, Qty: {quantity}{price_str}"

    def _generate_execution_summary(self, res: OrderResponse) -> str:
        """Generate a detailed execution summary of a placed order."""
        return (
            f"Execution Details -> ID: {res.order_id} | Symbol: {res.symbol} | "
            f"Status: {res.status} | Client ID: {res.client_order_id} | "
            f"Type: {res.type} | Side: {res.side} | "
            f"Orig Qty: {res.orig_qty} | Exec Qty: {res.executed_qty} | "
            f"Avg Price: {res.avg_price} | Update Time: {res.update_time_ms}"
        )
