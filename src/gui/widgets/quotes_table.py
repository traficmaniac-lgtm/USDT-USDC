from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.core.mock_data import QuoteRow


class QuotesTable(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.table = QTableWidget(0, 6, self)
        self.table.setHorizontalHeaderLabels(
            ["Exchange", "Bid", "Ask", "Spread", "Age", "Status"]
        )
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.table)

    def update_rows(self, rows: list[QuoteRow]) -> None:
        self.table.setSortingEnabled(False)
        existing = {
            self.table.item(row, 0).text(): row
            for row in range(self.table.rowCount())
            if self.table.item(row, 0) is not None
        }
        for row_data in rows:
            if row_data.exchange in existing:
                row_idx = existing[row_data.exchange]
            else:
                row_idx = self.table.rowCount()
                self.table.insertRow(row_idx)
                self.table.setItem(row_idx, 0, QTableWidgetItem(row_data.exchange))

            self._set_number_item(row_idx, 1, row_data.bid)
            self._set_number_item(row_idx, 2, row_data.ask)
            self._set_number_item(row_idx, 3, row_data.spread)
            age_item = QTableWidgetItem(f"{row_data.age_s:.1f}s")
            age_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 4, age_item)

            status_item = QTableWidgetItem(row_data.status)
            status_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 5, status_item)

        self.table.setSortingEnabled(True)

    def _set_number_item(
        self, row: int, column: int, value: float | None
    ) -> None:
        text = "-" if value is None else f"{value:.6f}"
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.table.setItem(row, column, item)
