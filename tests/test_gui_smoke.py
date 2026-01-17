import os

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PySide6 = pytest.importorskip("PySide6")
from PySide6.QtWidgets import QApplication

from src.gui.main_window import MainWindow


def test_main_window_smoke() -> None:
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    assert window.windowTitle() == "USDT/USDC Monitor"
    window.close()
    app.quit()
