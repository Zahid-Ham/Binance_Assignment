"""
Command Line Interface (CLI) configuration.
Provides commands to control, monitor, configure and run the trading bot.
"""

import typer
from rich.console import Console
from rich.panel import Panel
from loguru import logger
from bot.config import load_config
from bot.logging_config import setup_logging
from bot.client import BinanceClient

app = typer.Typer(
    name="trading-bot",
    help="Production-quality Binance Futures Testnet Trading Bot CLI.",
    no_args_is_help=True,
)
console = Console()


@app.callback()
def main(
    log_level: str = typer.Option(
        "INFO", "--log-level", "-l", help="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )
) -> None:
    """
    Initialize global options and configuration.
    """
    setup_logging(log_level)
    logger.info("CLI callback execution started.")


@app.command()
def test_connection() -> None:
    """
    Check connection and authenticate with Binance Futures Testnet API.
    """
    console.print(Panel("[bold yellow]Testing connection to Binance Futures Testnet...[/]"))
    try:
        config = load_config()
        client = BinanceClient(config)
        client.connect()
        console.print("[bold green][OK] Connection test completed successfully (Mocked)![/]")
    except Exception as e:
        console.print(f"[bold red][ERROR] Connection check failed: {e}[/]")
        raise typer.Exit(code=1)


@app.command()
def run() -> None:
    """
    Start the main trading bot execution loop.
    """
    console.print(Panel("[bold green]Starting Binance Futures Trading Bot loop...[/]"))
    logger.info("Trading bot execution loop initialized.")
    # TODO: In the next phase, run the main trading algorithm / logic loop.
    console.print("[cyan]Trading bot started. Press Ctrl+C to exit.[/]")


if __name__ == "__main__":
    app()
