from __future__ import annotations

import time

from loguru import logger
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QMainWindow,
    QSplitter,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.core.mock_data import MockQuoteEngine
from src.gui.widgets.arbitrage_tab import ArbitrageTab
from src.gui.widgets.exchange_list import ExchangeList
from src.gui.widgets.log_panel import LogPanel
from src.gui.widgets.quotes_table import QuotesTable
from src.gui.widgets.topbar import TopBar

EXCHANGES = [
    "Binance",
    "OKX",
    "Bybit",
    "KuCoin",
    "Gate.io",
    "Bitget",
    "Kraken",
    "Coinbase",
    "HTX",
    "MEXC",
    "Crypto.com",
]


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("USDT/USDC Monitor")
        self.resize(1200, 800)

        self.top_bar = TopBar()
        self.exchange_list = ExchangeList(EXCHANGES)
        self.quotes_table = QuotesTable()
        self.log_panel = LogPanel()
        self.arbitrage_tab = ArbitrageTab()

        self._quote_engine = MockQuoteEngine(EXCHANGES)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh_quotes)
        self._last_log_time = 0.0

        self._build_layout()
        self._connect_signals()
        self._apply_styles()

        self._refresh_quotes()

    def _build_layout(self) -> None:
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        layout.addWidget(self.top_bar)

        horizontal_split = QSplitter(Qt.Horizontal)
        horizontal_split.addWidget(self.exchange_list)

        tabs = QTabWidget()
        tabs.addTab(self.quotes_table, "Quotes")
        tabs.addTab(self.arbitrage_tab, "Arbitrage")
        horizontal_split.addWidget(tabs)
        horizontal_split.setStretchFactor(1, 1)

        vertical_split = QSplitter(Qt.Vertical)
        vertical_split.addWidget(horizontal_split)
        vertical_split.addWidget(self.log_panel)
        vertical_split.setStretchFactor(0, 3)
        vertical_split.setStretchFactor(1, 1)

        layout.addWidget(vertical_split)
        self.setCentralWidget(central)

    def _connect_signals(self) -> None:
        self.top_bar.start_requested.connect(self.start_monitoring)
        self.top_bar.stop_requested.connect(self.stop_monitoring)
        self.top_bar.interval_spin.valueChanged.connect(self._update_interval)

    def _apply_styles(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #1e1e1e;
                color: #ecf0f1;
            }
            QLabel { color: #ecf0f1; }
            QTabWidget::pane { border: 1px solid #2c3e50; }
            QTableWidget { background-color: #111; gridline-color: #2c3e50; }
            QHeaderView::section { background-color: #2c3e50; color: #ecf0f1; }
            QTextEdit { background-color: #111; color: #ecf0f1; }
            QPushButton { background-color: #2c3e50; padding: 6px 12px; }
            QPushButton:disabled { background-color: #34495e; color: #7f8c8d; }
            QComboBox, QSpinBox { background-color: #2c3e50; padding: 4px; }
            """
        )

    def start_monitoring(self) -> None:
        self.top_bar.update_running_state(True)
        self._timer.start(self.top_bar.interval_ms())
        self._log("INFO", "Monitoring started")

    def stop_monitoring(self) -> None:
        self.top_bar.update_running_state(False)
        self._timer.stop()
        self._log("WARN", "Monitoring stopped")

    def _update_interval(self, value: int) -> None:
        if self._timer.isActive():
            self._timer.setInterval(value)
            self._log("INFO", f"Refresh interval set to {value} ms")

    def _refresh_quotes(self) -> None:
        enabled = self.exchange_list.selected_exchanges()
        rows = self._quote_engine.refresh(enabled)
        self.quotes_table.update_rows(rows)
        for row in rows:
            self.exchange_list.set_exchange_status(row.exchange, row.status)

        now = time.time()
        if now - self._last_log_time > 5:
            self._last_log_time = now
            self._log(
                "INFO",
                f"Updated quotes for {len(enabled)} exchanges",
            )

    def _log(self, level: str, message: str) -> None:
        self.log_panel.append_message(level, message)
        if level == "INFO":
            logger.info(message)
        elif level == "WARN":
            logger.warning(message)
        else:
            logger.error(message)
