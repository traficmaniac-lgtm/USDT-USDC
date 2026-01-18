# USDT/USDC Monitor (GUI-only v0.1)

This branch (`gui-v0.1`) provides a **GUI-only** PySide6 desktop shell for monitoring the USDT/USDC pair across multiple exchanges. It uses **mock data only** (no real exchange connections, no API keys, no business logic).

## Features

- Professional terminal-style main window layout
- Exchange selection with status indicators
- Quotes table with sortable columns and timer updates
- Start/Stop controls with status indicator
- Log panel with color-coded messages
- Placeholder "Arbitrage" tab for future work

## Run

From the repository root:

```bash
python -m src.app
```

> **Note:** On Linux you may need system OpenGL libraries (for example, `libGL`) for Qt to initialize properly.

## Tests

```bash
pytest
```
