import os

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


def test_main_window_smoke() -> None:
    QtWidgets = pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    QApplication = QtWidgets.QApplication
    from src.gui.main_window import MainWindow

    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    assert window.windowTitle() == "USDT/USDC Monitor"
    window.close()
    app.quit()
