# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-07-04

### Added
- **Core Architecture & Client Integration**:
  - Implemented the modular `BinanceClient` wrapping `python-binance` configured for the Futures Testnet environment.
  - Added structured return types (`AssetBalance`, `PositionInfo`, `AccountInfoResponse`, `OrderResponse`) to keep exchange models separate from business logic.
  - Built automatic connection retry handling and request latency instrumentation measuring network performance in milliseconds.
  - Implemented custom error domain exception classes (`APIException`, `AuthenticationException`, `RateLimitException`, `NetworkException`, `ValidationException`) mapping API codes.
- **Order Service Orchestration**:
  - Implemented `OrderService` using dependency injection to coordinate validation, pre-execution order logs, client executions, and post-execution outcomes.
- **Robust Validation Engine**:
  - Added comprehensive trade parameter validators in `bot/validators.py` for symbol cases/types, buy/sell sides, limit/market order types, positive quantities, and limit prices.
- **Advanced Logging**:
  - Configured high-performance logging via `Loguru` utilizing colorized console outputs and daily rotating ZIP compressed logs under the `logs/` directory.
- **Command Line Interface (CLI)**:
  - Developed a double-mode CLI using `Typer` and `Rich` support.
  - Built interactive prompts with autocomplete options, spinner overlays during network requests, confirmation screens, and styled outcome tables/panels.
  - Added direct command line parameter inputs parsing (e.g. `python run.py --symbol ...`).
- **CI/CD Actions & Environment Setup**:
  - Added GitHub Actions pipeline executing linting checks via Ruff and the unit tests suite via pytest.
  - Standardized `.env.example`, `.gitignore`, `CONTRIBUTING.md`, and requirements pins.
- **Test Coverage**:
  - Completed 27 unit tests verifying validator parameters, network retry recovery, exception formatting, and OrderService execution pathways.

---

### Known Limitations
* **Hedge Mode Limitation**: Current client connections default to one-way position execution. Dual position sides (Hedge Mode) are not currently supported.
* **Leverage Setup**: Leverage changes are not yet integrated into the interactive loop or CLI arguments.
* **Stop Orders**: The bot currently supports only `MARKET` and `LIMIT` orders; stop-loss or take-profit orders are not processed in this version.

---

### Future Roadmap
- [ ] Implement Stop Loss, Take Profit, and Trailing Stop order executions.
- [ ] Add support for OCO (One-Cancels-the-Other) orders and Hedge Mode.
- [ ] Integrate grid trading and TWAP strategy engines.
- [ ] Containerize application using Docker.
- [ ] Add detailed dashboard visualizations (terminal-based or web interfaces).
- [ ] Increase unit test coverage (e.g. mocking websocket feeds).
