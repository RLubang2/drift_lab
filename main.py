import sys
import logging
from typing import Optional

from PyQt6 import QtWidgets
from PyQt6.QtGui import QCloseEvent
from PyQt6.uic.load_ui import loadUi
from PyQt6.QtCore import Qt

from ui_manager.user_interface_config import UserInterfaceConfig
from temperature_manager.temp_profile import CustomTempProfile, RampTempProfile
from smu_manager.run_smu import RunSMU
from smu_manager.connect_smu import ConnectSMU
from measurement_manager.dmm import DmmMeasurement
from measurement_manager.dmm_connect import ConnectDMM
from test_manager.test import RunTest
from ni_pxie_6570.connect_digital import ConnectDigital
from temperature_manager.temp_run import RunTemp
from cons_window.console import ConsoleWindow
from temperature_manager.temp_connect import TempConnect


import sys
import os



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, console: ConsoleWindow) -> None:
        super().__init__()
        self.console = console
        self._run_test: Optional[RunTest] = None

    def set_run_test(self, run_test: RunTest) -> None:
        self._run_test = run_test

    def closeEvent(self, event: Optional[QCloseEvent]) -> None:
        try:
            if self._run_test is not None:
                self._run_test.reset_all_equipment()
        except Exception:
            pass
        try:
            if self.console is not None:
                self.console.close()
        except RuntimeError:
            pass
        super().closeEvent(event)

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def setup_ui(console: ConsoleWindow) -> MainWindow:
    window = MainWindow(console)
    loadUi(resource_path("mainwindow.ui"), window)
    return window


def main() -> None: 
    logging.basicConfig(level=logging.INFO)
    app = QtWidgets.QApplication(sys.argv)

    console = ConsoleWindow()
    window = setup_ui(console)

    ui_config = UserInterfaceConfig(window)
    RampTempProfile(ui_config)
    CustomTempProfile(ui_config)
    TempConnect(ui_config)
    ConnectSMU(ui_config)
    RunSMU(ui_config)
    ConnectDMM(ui_config)
    ConnectDigital(ui_config)
    RunTemp(ui_config)

    run_test = RunTest(ui_config, console)
    window.set_run_test(run_test)

    app.aboutToQuit.connect(lambda: _on_quit(run_test, console))

    window.show()
    console.setGeometry(
        window.x() + window.width() + 20, window.y(), 400, window.height()
    )
    console.show()

    sys.exit(app.exec())


def _on_quit(run_test: RunTest, console: ConsoleWindow) -> None:
    try:
        run_test.reset_all_equipment()
    except Exception:
        pass
    try:
        console.close()
    except RuntimeError:
        pass


if __name__ == "__main__":
    main()
