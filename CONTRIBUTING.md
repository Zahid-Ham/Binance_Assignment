# Contributing to Binance Futures Trading Bot

Thank you for showing interest in contributing to the Binance Futures Trading Bot project! We welcome all contributions, including bug fixes, feature enhancements, documentation updates, and testing additions.

To maintain our code quality, modular architecture, and project organization, please read and follow these contribution guidelines.

---

## 🚀 Project Setup

To set up a local development workspace, follow these commands:

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/Zahid-Ham/Binance_Assignment.git
   cd Binance_Assignment
   ```

2. **Initialize a Virtual Environment**
   We enforce Python 3.12 for this codebase:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   Install both project dependencies and development tools (e.g. pytest, ruff):
   ```bash
   pip install -r requirements.txt
   pip install ruff pytest
   ```

4. **Verify Setup**
   Run the local tests to ensure the setup is correct:
   ```bash
   python -m pytest tests/
   ```

---

## 🎨 Coding Standards

We follow strict standards to keep the code neat, professional, and easy to maintain:

* **PEP8 Compliance**: All code must conform to PEP8 standards.
* **Docstrings**: We use **Google-style docstrings** for all modules, classes, and functions.
* **Type Hints**: Complete type hints (via `typing`) are required for all function arguments and return signatures.
* **Separation of Concerns**: Do not mix user-interface options (CLI), validation logic, and exchange API requests. Keep these contained within their respective modules (`bot/cli.py`, `bot/validators.py`, `bot/client.py`).
* **Linter Checks**: We use **Ruff** for static analysis. Before committing, run linting checks:
  ```bash
  ruff check .
  ```

---

## 📁 Folder Structure

Please respect our modular project structure layout:

```text
Binance_Assignment/
│
├── bot/                           # Main package containing domain modules
│   ├── cli.py                     # User interface prompts and flags
│   ├── client.py                  # API gateways and connectivity retries
│   ├── config.py                  # Config loader and validators
│   ├── exceptions.py              # Custom domain error classes
│   ├── validators.py              # Input trade validation checks
│   └── ...
│
├── tests/                         # Unit and integration test suites
├── logs/                          # Rotation log files (Ignored in Git)
└── .github/workflows/             # GitHub Actions CI configurations
```

---

## 🌿 Branch Naming Conventions

Always create a descriptive branch for your changes:

* **Feature Branches**: `feat/brief-description` (e.g. `feat/stop-loss-order`)
* **Bug Fixes**: `fix/brief-description` (e.g. `fix/rate-limit-retry`)
* **Documentation**: `docs/brief-description` (e.g. `docs/update-contributing`)
* **Chore/Maintenance**: `chore/brief-description` (e.g. `chore/dependency-upgrade`)

---

## 💬 Commit Message Conventions

We follow the **Conventional Commits** specification for commit messages:

* `feat: ...` for a new feature implementation (e.g., `feat: integrate trailing stops`).
* `fix: ...` for a bug fix (e.g., `fix: resolve float cast precision error`).
* `docs: ...` for documentation changes (e.g., `docs: add installation instructions`).
* `test: ...` for adding or refactoring test cases (e.g., `test: add order service failures mock tests`).
* `chore: ...` for dependency updates, Git configuration, or tooling scripts (e.g., `chore: pin requirements versions`).

---

## 🐛 Issue Reporting

If you encounter a bug or have a feature proposal, please open an Issue with:

1. **Clear Title**: Brief summary of the bug/proposal.
2. **Context Details**: Your operating system, Python version, and dependency versions.
3. **Reproducible Steps**: Code snippets or command executions that trigger the bug.
4. **Expected vs Actual Behavior**: Contrast the outcome with what should have happened.
5. **Console Log Traces**: Logs from `logs/trading_bot.log` showing traceback exceptions.

---

## 📥 Pull Request Guidelines

Before submitting a Pull Request (PR):

1. **Keep it focused**: A single PR should address a single issue or implement a single feature.
2. **Test your code**: Ensure all unit tests pass locally:
   ```bash
   python -m pytest tests/
   ```
3. **Run Lint Checks**: Confirm there are no style or syntax warning errors:
   ```bash
   ruff check .
   ```
4. **Sync with Main**: Merge the latest commits from the upstream `main` branch to resolve conflicts.
5. **Describe your changes**: Write a clear description of the problem solved, changes made, and manual testing completed.
