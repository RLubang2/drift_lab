from PyQt6.QtWidgets import QMainWindow, QPlainTextEdit
from PyQt6.QtCore import pyqtSlot


class ConsoleWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Debug Console")
        self.resize(300, 500)

        self._console = QPlainTextEdit()
        self._console.setReadOnly(True)
        self.setCentralWidget(self._console)

    @pyqtSlot(str)
    def log(self, text: str) -> None:
        self._console.appendPlainText(str(text))
