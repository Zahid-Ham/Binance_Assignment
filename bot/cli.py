"""Command Line Interface (CLI) configuration.

Provides command-line options and interactive prompting loops powered by Typer and Rich.
"""

from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from loguru import logger

from bot.config import load_config
from bot.logging_config import setup_logging
from bot.client import BinanceClient
from bot.orders import OrderService, OrderResult
from bot.constants import APP_NAME, VERSION, SUPPORTED_SYMBOLS, SUPPORTED_ORDER_TYPES, SUPPORTED_SIDES

app = typer.Typer(
    name="trading-bot",
    help="Production-quality Binance Futures Testnet Trading Bot CLI.",
    no_args_is_help=False,
)
console = Console()


def display_startup_banner() -> None:
    """Render a beautiful colored startup banner with metadata."""
    banner_text = Text()
    banner_text.append(f"{APP_NAME}\n", style="bold green")
    banner_text.append(f"Version: {VERSION} | Environment: Testnet\n", style="cyan")
    banner_text.append("Clean Architecture - Production Quality", style="italic blue")

    console.print(
        Panel(
            banner_text,
            title="[bold white]Startup Initialized[/bold white]",
            border_style="green",
            expand=False,
        )
    )


def render_order_table(
    symbol: str, side: str, order_type: str, quantity: float, price: Optional[float]
) -> None:
    """Render a clean Rich Table detailing the order specifications for confirmation."""
    table = Table(title="[bold yellow]Order Specifications[/bold yellow]", show_header=True, header_style="bold blue")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="magenta")

    table.add_row("Symbol", symbol)
    table.add_row("Side", side)
    table.add_row("Type", order_type)
    table.add_row("Quantity", str(quantity))
    if price is not None:
        table.add_row("Price", f"${price:,.2f}")

    console.print(table)


def render_result_panel(result: OrderResult) -> None:
    """Render the post-execution OrderResult details inside a Rich Panel."""
    if result.is_success:
        title = "[bold green]Order Execution Successful[/bold green]"
        border_style = "green"
        msg_style = "bold green"
    else:
        title = "[bold red]Order Execution Failed[/bold red]"
        border_style = "red"
        msg_style = "bold red"

    markup = (
        f"[{msg_style}]{result.message}[/{msg_style}]\n\n"
        f"[bold cyan]Order Summary:[/bold cyan]\n{result.order_summary}\n\n"
        f"[bold magenta]Execution Details:[/bold magenta]\n{result.execution_summary}"
    )
    content = Text.from_markup(markup)
    console.print(Panel(content, title=title, border_style=border_style, expand=True))


def execute_order(
    service: OrderService,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float],
) -> OrderResult:
    """Helper to dispatch orders through OrderService while showing a spinner status."""
    with console.status("[bold yellow]Sending request to Binance Futures Testnet...[/bold yellow]") as status:
        if order_type.upper() == "LIMIT":
            # We assume validation catches missing price, default to 0.0 just in case
            price_val = price if price is not None else 0.0
            result = service.place_limit_order(
                symbol=symbol, side=side, quantity=quantity, price=price_val
            )
        else:
            result = service.place_market_order(
                symbol=symbol, side=side, quantity=quantity
            )
    return result


def start_interactive_loop(service: OrderService) -> None:
    """Execute the interactive terminal prompting loop."""
    console.print("\n[bold blue]Entering Interactive Order Placement Mode...[/bold blue]\n")
    
    while True:
        # 1. Collect symbol
        symbols_list = list(SUPPORTED_SYMBOLS)
        symbol = Prompt.ask(
            "Select Trading Symbol",
            choices=symbols_list,
            default=symbols_list[0],
        )

        # 2. Collect side
        side = Prompt.ask(
            "Select Side",
            choices=list(SUPPORTED_SIDES),
            default="BUY",
        )

        # 3. Collect order type
        order_type = Prompt.ask(
            "Select Order Type",
            choices=list(SUPPORTED_ORDER_TYPES),
            default="MARKET",
        )

        # 4. Collect quantity
        quantity_str = Prompt.ask("Enter Quantity")
        try:
            quantity = float(quantity_str)
        except ValueError:
            console.print("[bold red]Quantity must be a numeric value.[/bold red]")
            continue

        # 5. Collect price if LIMIT
        price: Optional[float] = None
        if order_type == "LIMIT":
            price_str = Prompt.ask("Enter Price")
            try:
                price = float(price_str)
            except ValueError:
                console.print("[bold red]Price must be a numeric value for LIMIT orders.[/bold red]")
                continue

        # 6. Show Confirmation Table
        console.print("")
        render_order_table(symbol, side, order_type, quantity, price)
        console.print("")

        # 7. Ask for execution confirmation
        confirmed = Confirm.ask("Do you want to submit this order?")
        if confirmed:
            result = execute_order(service, symbol, side, order_type, quantity, price)
            render_result_panel(result)
        else:
            console.print("[bold yellow]Order cancelled by user.[/bold yellow]")

        # 8. Loop prompt
        another = Confirm.ask("Do you want to place another order?")
        if not another:
            console.print("\n[bold green]Thank you for using the Trading Bot CLI. Goodbye![/bold green]")
            break


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    symbol: Optional[str] = typer.Option(
        None, "--symbol", "-s", help="Trading symbol (e.g. BTCUSDT)"
    ),
    side: Optional[str] = typer.Option(
        None, "--side", "-d", help="Order Side (BUY or SELL)"
    ),
    order_type: Optional[str] = typer.Option(
        None, "--type", "-t", help="Order Type (LIMIT or MARKET)"
    ),
    quantity: Optional[float] = typer.Option(
        None, "--quantity", "-q", help="Order quantity"
    ),
    price: Optional[float] = typer.Option(
        None, "--price", "-p", help="Order price (LIMIT orders only)"
    ),
    log_level: str = typer.Option(
        "INFO", "--log-level", "-l", help="Logging level (DEBUG, INFO, WARNING, ERROR)"
    ),
) -> None:
    """Initialize options, print startup banners, and route CLI vs Interactive loops."""
    setup_logging(log_level)
    
    # If a subcommand (like test-connection) is called, skip main trade dispatch
    if ctx.invoked_subcommand is not None:
        return

    display_startup_banner()

    # Initialize connection settings
    try:
        config = load_config()
        client = BinanceClient(config)
        client.connect()
        service = OrderService(client)
    except Exception as e:
        console.print(Panel(f"[bold red]Initialization Failure:[/bold red]\n{e}", border_style="red"))
        raise typer.Exit(code=1)

    # Detect Mode: CLI Args Mode vs Interactive Mode
    has_args = any(x is not None for x in [symbol, side, order_type, quantity])
    
    if has_args:
        # Validate that all required CLI parameters are present
        if not all(x is not None for x in [symbol, side, order_type, quantity]):
            console.print(
                "[bold red]Error: Missing required parameters. For CLI mode, you must provide "
                "--symbol, --side, --type, and --quantity.[/bold red]"
            )
            raise typer.Exit(code=1)

        # Enforce price parameter check for LIMIT orders
        if order_type.upper() == "LIMIT" and price is None:
            console.print("[bold red]Error: --price is required when --type is LIMIT.[/bold red]")
            raise typer.Exit(code=1)

        # Execute immediately (CLI Mode)
        console.print("[bold blue]Executing in CLI Arguments Mode...[/bold blue]\n")
        render_order_table(symbol, side, order_type, quantity, price)
        result = execute_order(service, symbol, side, order_type, quantity, price)
        render_result_panel(result)
        if not result.is_success:
            raise typer.Exit(code=1)
    else:
        # Enter Interactive Loop
        start_interactive_loop(service)


@app.command()
def test_connection() -> None:
    """Check connection and authenticate with Binance Futures Testnet API."""
    console.print(Panel("[bold yellow]Testing connection to Binance Futures Testnet...[/]"))
    try:
        config = load_config()
        client = BinanceClient(config)
        client.connect()
        console.print("[bold green][OK] Connection test completed successfully (Mocked)![/]")
    except Exception as e:
        console.print(f"[bold red][ERROR] Connection check failed: {e}[/]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
