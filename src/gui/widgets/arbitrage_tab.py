from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ArbitrageTab(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        placeholder = QLabel("Arbitrage view coming soon...")
        placeholder.setStyleSheet("color: #7f8c8d;")
        layout.addWidget(placeholder)
        layout.addStretch(1)
