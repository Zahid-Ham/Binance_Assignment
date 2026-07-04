# Binance Futures Testnet Trading Bot

A production-quality, modular, and robust automated trading bot for the Binance Futures Testnet. Designed using clean architecture principles and Python best practices.

## Table of Contents

- [Project Description](#project-description)
- [Architecture & Design](#architecture--design)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [License](#license)

## Project Description

This trading bot connects to the Binance Futures Testnet API to monitor market data, manage positions, and execute automated trading strategies safely without risking real capital. It is engineered with robust validation, clean separating layers, detailed logging, and custom exception handling.

## Architecture & Design

Following Clean Architecture principles:
- **`bot/client.py`**: Handles API connections, requests, and rate-limiting.
- **`bot/orders.py`**: Manages execution and tracking of limit, market, and stop orders.
- **`bot/config.py`**: Validates environmental parameters using standard types and Pydantic models.
- **`bot/validators.py`**: Validates trade sizes, symbols, prices, and risk management parameters.
- **`bot/logging_config.py`**: Configures advanced logging using `loguru` and formatting with `rich`.

## Project Structure

```text
Binance_Assignment/
│
├── bot/                       # Main application package
│   ├── __init__.py            # Package entrypoint
│   ├── client.py              # Binance API client interface
│   ├── config.py              # Application settings & validation
│   ├── constants.py           # Enums and global constants
│   ├── exceptions.py          # Custom domain exceptions
│   ├── validators.py          # Input validation helpers
│   ├── orders.py              # Order construction & management
│   ├── logging_config.py      # Logger initialization and setup
│   ├── utils.py               # Shared utility functions
│   └── cli.py                 # CLI commands (Typer)
│
├── logs/                      # Rotating log files directory
├── tests/                     # Unit and integration test suite
├── screenshots/               # Execution and test screenshots
├── .env.example               # Template for environment configurations
├── .gitignore                 # Version control ignores
├── README.md                  # Project documentation
├── requirements.txt           # Package dependencies
└── run.py                     # Application entrypoint script
```

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Zahid-Ham/Binance_Assignment.git
   cd Binance_Assignment
   ```

2. **Set up virtual environment (Python 3.12):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in your Binance Futures Testnet API Key and Secret.

## Usage

Run the trading bot CLI:
```bash
python run.py --help
```

## Testing

Run unit tests via `pytest`:
```bash
pytest
```
