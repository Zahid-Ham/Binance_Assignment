<div align="center">

# ⚡ Binance Futures Testnet Trading Bot
### *A Production-Quality, Modular, and Robust Automated Trading System*

[![Python Version](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white&style=for-the-badge)](https://www.python.org/)
[![Binance API](https://img.shields.io/badge/Binance-Futures-orange?logo=binance&logoColor=white&style=for-the-badge)](https://python-binance.readthedocs.io/)
[![UI](https://img.shields.io/badge/Console-Rich%20%26%20Typer-blueviolet?style=for-the-badge)](https://rich.readthedocs.io/)
[![Logging](https://img.shields.io/badge/Logs-Loguru-green?style=for-the-badge)](https://github.com/Delgan/loguru)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

## 📌 Overview

This project is a production-grade **Binance Futures Testnet Trading Bot** built as a Python internship assignment. Designed using **Clean Architecture** principles, it provides a secure, modular, and highly interactive CLI interface to execute mock futures orders safely on the Binance Testnet environment.

* **What it is:** A robust, terminal-based trading bot that handles connection health checks, account balances, position diagnostics, and order placement.
* **Why it exists:** To bridge the gap between simple script-based trading and production-ready systems by enforcing proper type validation, customized exceptions, connection retry routines, and modular structure.
* **Who it is for:** Developers, traders, and maintainers looking for a solid architectural foundation to test trading strategies on Binance Futures without risking real capital.

---

## 🚀 Features

We present the features of this system formatted as card tables below:

| Feature Card | Core Capabilities |
| :--- | :--- |
| **📈 Order Placement Engine** | Supports execution of **MARKET** and **LIMIT** orders. Interfaces directly with Binance Testnet API. |
| **🛡️ Input Validation Guard** | Enforces checks on symbols (case-sensitive matching), positive quantities, sides (`BUY`/`SELL`), and prices. |
| **🔄 Automated Network Resiliency** | Handles requests with built-in retry mechanisms, exponential delays, and connection health-checks. |
| **🎨 Rich Interactive Console** | Features colored prompts, loading spinners, confirmation screens, and formatted tables/panels. |
| **📝 Rotation-Enabled Logging** | Daily and size-based (5 MB) log file rotations keeping log files compressed and maintained for 14 days. |
| **🧩 Decoupled Domain Logic** | Separates validation, API requests, configuration, and logging to follow strict Clean Architecture. |

---

## 🏛️ Architecture & Dataflow

The project follows a unidirectional dataflow pattern separating user-facing terminals, controllers, business rules, and API gateways:

```text
       [ User / Terminal ]
                │
                ▼
         [ bot/cli.py ]  ◄─────────►  [ bot/logging_config.py ]
                │
                ▼
      [ bot/validators.py ]
                │
                ▼
        [ bot/orders.py ] ◄────────►  [ bot/utils.py ]
         (OrderService)
                │
                ▼
        [ bot/client.py ] ◄────────►  [ bot/config.py ]
        (BinanceClient)
                │
                ▼
   [ Binance Testnet API Gateway ]
```

---

## 📁 Project Structure

```text
Binance_Assignment/
│
├── bot/                           # Core Bot package
│   ├── __init__.py                # Package entrypoint & metadata
│   ├── cli.py                     # Typer command-line routing and Rich UI loops
│   ├── client.py                  # Binance API connection, latency tracing, and retries
│   ├── config.py                  # Environment loader using Pydantic Settings
│   ├── constants.py               # Reusable Enums and global constants
│   ├── exceptions.py              # Domain custom exception classes
│   ├── logging_config.py          # Loguru rotating file and styled console setup
│   ├── utils.py                   # Formatting, masking, and calculations helpers
│   └── validators.py              # Input trade validation and normalization rules
│
├── logs/                          # Automatically generated log files directory
├── screenshots/                   # Placeholders for console UI screenshots
├── tests/                         # Unit tests directory
│   ├── test_client.py             # Client authentication and mock connection tests
│   ├── test_orders.py             # Order validation and execution path tests
│   └── test_validators.py         # Formats, ranges, and types validation tests
│
├── .env.example                   # Configurations credentials template
├── .gitignore                     # Git configuration patterns
├── README.md                      # Premium repository documentation
├── requirements.txt               # Project dependency package requirements
└── run.py                         # Application entrypoint launcher script
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
| :--- | :--- |
| **Python 3.12** | Programming language utilizing modern type-hints and speed features. |
| **python-binance** | Unofficial Python wrapper for the Binance API endpoints. |
| **Pydantic v2** | Settings management and data validation via environment bindings. |
| **Typer** | Builds clear CLI options and subcommand structures. |
| **Rich** | Renders beautiful tables, panels, spinners, and logs to the console. |
| **Loguru** | High-performance rotating and structured diagnostics logging. |

---

## 💻 Installation

### 1. Prerequisite Checks
Ensure you have Python 3.12 (or higher) installed on your system.

### 2. Set Up Virtual Environment
Clone the repository and initialize a virtual environment:
```bash
git clone https://github.com/Zahid-Ham/Binance_Assignment.git
cd Binance_Assignment
python -m venv venv
```

Activate the environment:
* **Windows (Cmd/PowerShell):**
  ```powershell
  .\venv\Scripts\activate
  ```
* **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environmental Variables
Copy the template `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open the `.env` file and insert your Binance Futures Testnet keys:
```env
BINANCE_API_KEY=your_actual_testnet_api_key_here
BINANCE_SECRET_KEY=your_actual_testnet_secret_key_here
BASE_URL=https://testnet.binancefuture.com
```

---

## 📖 Usage

The application can be run in two modes: **Interactive Mode** or **CLI Option Mode**.

### 1. Interactive Mode
Run the script without any parameters to launch the prompt walkthrough:
```bash
python run.py
```
* **Step-by-step Loop:** It will guide you through choosing a symbol, order side, order type, quantity, and price.
* **Confirmation Table:** Displays the summarized parameters before calling the API.
* **Placing another order:** Prompts to repeat the cycle without restarting the script.

### 2. CLI Option Mode
Execute commands directly with arguments:
```bash
# Place a Market Buy Order
python run.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

# Place a Limit Sell Order
python run.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 1.5 --price 1850.0
```

### 3. Connection Health Check
Test your keys and ping connectivity to the Testnet:
```bash
python run.py test-connection
```

---

## 📷 Screenshots / Demos

Below are mock placeholders representing the terminal output layouts:

### Startup Banner
```text
┌────────────────────────── Startup Initialized ───────────────────────────┐
│ Binance Futures Testnet Trading Bot                                      │
│ Version: 1.0.0 | Environment: Testnet                                    │
│ Clean Architecture - Production Quality                                  │
└──────────────────────────────────────────────────────────────────────────┘
```

### Order Summary Table
```text
                         Order Specifications                          
┌───────────┬──────────────────────────────────────────────────────────────┐
│ Parameter │ Value                                                        │
├───────────┼──────────────────────────────────────────────────────────────┤
│ Symbol    │ BTCUSDT                                                      │
│ Side      │ BUY                                                          │
│ Type      | LIMIT                                                        │
│ Quantity  │ 0.1                                                          │
│ Price     │ $30,000.00                                                   │
└───────────┴──────────────────────────────────────────────────────────────┘
```

### Execution Outcome Panel
```text
┌───────────────────────── Order Execution Successful ────────────────────────┐
│ SUCCESS: Limit order placed successfully. Order ID: 54321                  │
│                                                                             │
│ Order Summary:                                                              │
│ Order Request: LIMIT BUY - Symbol: BTCUSDT, Qty: 0.1 @ Price: 30000.0       │
│                                                                             │
│ Execution Details:                                                          │
│ ID: 54321 | Status: NEW | Type: LIMIT | Side: BUY | Avg Price: 0.0          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📝 Logging Configuration

The system uses `Loguru` to output to both console stdout (colored) and daily rotating log files under the `logs/` directory.

### Log File Rules:
* **Log Location:** `logs/trading_bot.log`
* **Rotation Size:** `5 MB`
* **Retention Period:** `14 days`
* **Compression:** Automatically compressed as a `.zip` file on rotation.

### Log Format:
`Date Time | Level | Module:Function:Line - Message`

*Example logs from execution:*
```text
2026-07-04 10:15:12.767 | INFO     | bot.client:__init__:91 - Initializing BinanceClient with Key: test...y123 and Host: https://testnet.binancefuture.com
2026-07-04 10:15:13.701 | INFO     | bot.client:connect:114 - Client connected. Verifying connection via ping...
2026-07-04 10:15:14.558 | INFO     | bot.client:_execute_request:142 - Response: futures_ping received in 856.58ms
```

---

## 🛡️ Input Validation

Every parameter is pre-checked by `bot/validators.py` before API transmission:

* **Trading Symbol:** Must be uppercase. Matches supported assets: `BTCUSDT`, `ETHUSDT`, `BNBUSDT`, `SOLUSDT`.
* **Trade Side:** Restricted strictly to `BUY` and `SELL`.
* **Order Type:** Restricted strictly to `LIMIT` and `MARKET`.
* **Quantity:** Must be positive, numeric, and not exceed a maximum limit of `100.0` units (configurable).
* **Price:** Required only for `LIMIT` orders. Must be numeric and positive.

---

## 💥 Exception Handling

Custom exception domains mapped under `bot/exceptions.py` capture error states:

* **`AuthenticationException`**: Triggers on bad signatures, IP bans, or invalid API credentials (HTTP 401 / code `-2014`/`-2015`).
* **`RateLimitException`**: Triggers when requests hit the rate limits (HTTP 429 / code `-1003`).
* **`NetworkException`**: Handles offline states, proxy failures, and timeouts.
* **`ValidationException`**: Intercepts incorrect pricing, invalid sides, or unsupported symbols.
* **`APIException`**: Captures other exchange-specific failures (e.g. insufficient margin).

### Retry Mechanism
If a request encounters a network-related failure (`requests.exceptions.RequestException`), the client automatically retries up to **5 times** (configured by `MAXIMUM_RETRIES`), sleeping **2.0 seconds** (`RETRY_DELAY_SECONDS`) between attempts.

---

## ✨ Interactive Rich UX

To make the CLI experience feel premium, we leverage:
* **Interactive Prompts:** Simple choice listings with validation fallbacks.
* **Loading Spinner:** A pulsing status indicator shown during API roundtrips.
* **Console Coloring:** Success messages printed in bold **green**, errors in **red**, and warnings in **yellow**.

---

## 🔮 Future Roadmaps

In subsequent phases, we plan to implement:
- [ ] **Stop Loss & Take Profit Order Support**
- [ ] **One-Cancels-the-Other (OCO) Orders**
- [ ] **Grid Trading Strategy Engine**
- [ ] **TWAP / VWAP Execution Algorithms**
- [ ] **Docker Containerization**
- [ ] **GitHub Actions CI/CD Integration**

---

## 👤 Author

Developed by **Zahid** as a python software engineering internship assignment.

*Built with ❤️ using Python.*
