from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

STATUS_COLORS = {
    "OK": "#2ecc71",
    "STALE": "#7f8c8d",
    "ERROR": "#e74c3c",
}


@dataclass
class ExchangeItemWidgets:
    checkbox: QCheckBox
    status_indicator: QLabel


class ExchangeList(QWidget):
    def __init__(self, exchanges: list[str], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._items: dict[str, ExchangeItemWidgets] = {}

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        header = QLabel("Exchanges")
        header.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(6)

        for exchange in exchanges:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(4, 0, 4, 0)
            row_layout.setSpacing(6)

            indicator = QLabel()
            indicator.setFixedSize(10, 10)
            indicator.setStyleSheet(
                "background-color: #7f8c8d; border-radius: 5px;"
            )

            checkbox = QCheckBox(exchange)
            checkbox.setChecked(True)

            row_layout.addWidget(indicator)
            row_layout.addWidget(checkbox)
            row_layout.addStretch(1)
            container_layout.addWidget(row)

            self._items[exchange] = ExchangeItemWidgets(
                checkbox=checkbox,
                status_indicator=indicator,
            )

        container_layout.addStretch(1)
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        button_row = QHBoxLayout()
        select_all = QPushButton("Select All")
        select_none = QPushButton("None")
        button_row.addWidget(select_all)
        button_row.addWidget(select_none)
        main_layout.addLayout(button_row)

        select_all.clicked.connect(self.select_all)
        select_none.clicked.connect(self.select_none)

    def select_all(self) -> None:
        for item in self._items.values():
            item.checkbox.setChecked(True)

    def select_none(self) -> None:
        for item in self._items.values():
            item.checkbox.setChecked(False)

    def selected_exchanges(self) -> set[str]:
        return {
            name
            for name, item in self._items.items()
            if item.checkbox.isChecked()
        }

    def set_exchange_status(self, exchange: str, status: str) -> None:
        item = self._items.get(exchange)
        if not item:
            return
        color = STATUS_COLORS.get(status, "#7f8c8d")
        item.status_indicator.setStyleSheet(
            f"background-color: {color}; border-radius: 5px;"
        )
