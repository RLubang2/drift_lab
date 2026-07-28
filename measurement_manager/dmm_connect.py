from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui_manager.user_interface_config import UserInterfaceConfig

import pyvisa as visa
from PyQt6.QtWidgets import QMessageBox
from functools import partial

class ConnectDMM:
    def __init__(self, ui_config: UserInterfaceConfig) -> None:
        self.ui_config = ui_config
        self.ui_config.meas_ping_button.pressed.connect(partial(self._connect_dmm))

    def _connect_dmm(self) -> None:
        visa_address = self.ui_config.meas_address.currentText()
        if not visa_address:
            return

        rm = visa.ResourceManager()
        try:
            instrument = rm.open_resource(visa_address)
            instrument.write("Reset; End")  # type: ignore
            dev_id = instrument.query("Id?")  # type: ignore
            self.ui_config.meas_response.setText(dev_id)
        except visa.VisaIOError as e:
            QMessageBox.critical(None, "Unable to Query ID", f"Error: {e}")
            self.ui_config.meas_response.setText("")
