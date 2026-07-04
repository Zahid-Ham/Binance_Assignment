#!/usr/bin/env python3
"""
Entry point to run the trading bot application.
Imports and executes the CLI application.
"""

import sys
from bot.cli import app

if __name__ == "__main__":
    try:
        app()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting.")
        sys.exit(0)
    except Exception as e:
        print(f"Unhandled critical error: {e}", file=sys.stderr)
        sys.exit(1)
