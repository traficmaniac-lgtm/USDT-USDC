from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QWidget,
)


class TopBar(QWidget):
    start_requested = Signal()
    stop_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.pair_combo = QComboBox()
        self.pair_combo.addItems([
            "USDT/USDC",
            "USDT/USDT",
            "USDC/USDT",
            "EURC/USDC",
            "DAI/USDC",
        ])
        self.pair_combo.setCurrentText("USDT/USDC")

        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(250, 10000)
        self.interval_spin.setValue(1000)
        self.interval_spin.setSuffix(" ms")

        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)

        self.status_label = QLabel("STOPPED")
        self.status_label.setObjectName("statusLabel")
        self._update_status_style(is_running=False)

        layout.addWidget(QLabel("Pair"))
        layout.addWidget(self.pair_combo)
        layout.addWidget(QLabel("Interval"))
        layout.addWidget(self.interval_spin)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addStretch(1)
        layout.addWidget(QLabel("Status:"))
        layout.addWidget(self.status_label)

        self.start_button.clicked.connect(self.start_requested.emit)
        self.stop_button.clicked.connect(self.stop_requested.emit)

    def update_running_state(self, is_running: bool) -> None:
        self.start_button.setEnabled(not is_running)
        self.stop_button.setEnabled(is_running)
        self.status_label.setText("RUNNING" if is_running else "STOPPED")
        self._update_status_style(is_running=is_running)

    def _update_status_style(self, is_running: bool) -> None:
        color = "#2ecc71" if is_running else "#e74c3c"
        self.status_label.setStyleSheet(
            f"color: {color}; font-weight: bold;"
        )

    def current_pair(self) -> str:
        return self.pair_combo.currentText()

    def interval_ms(self) -> int:
        return self.interval_spin.value()
