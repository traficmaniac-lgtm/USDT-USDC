from __future__ import annotations

from datetime import datetime

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

LEVEL_COLORS = {
    "INFO": "#3498db",
    "WARN": "#f39c12",
    "ERROR": "#e74c3c",
}


class LogPanel(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        header_layout = QHBoxLayout()
        header = QLabel("Logs")
        header.setStyleSheet("font-weight: bold;")
        clear_button = QPushButton("Clear")
        header_layout.addWidget(header)
        header_layout.addStretch(1)
        header_layout.addWidget(clear_button)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        layout.addLayout(header_layout)
        layout.addWidget(self.text_edit)

        clear_button.clicked.connect(self.clear)

    def clear(self) -> None:
        self.text_edit.clear()

    def append_message(self, level: str, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = LEVEL_COLORS.get(level, "#ecf0f1")
        formatted = (
            f"<span style='color:{color};'>"
            f"[{timestamp}] {level}: {message}"
            "</span>"
        )
        self.text_edit.append(formatted)
