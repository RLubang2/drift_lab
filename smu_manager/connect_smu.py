from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui_manager.user_interface_config import UserInterfaceConfig

import pyvisa as visa
from PyQt6.QtWidgets import QMessageBox

from ui_manager.user_interface_variable import SUPPLY_NUMBER


class ConnectSMU:
    def __init__(self, ui_config: UserInterfaceConfig) -> None:
        self.ui_config = ui_config
        self._connect_buttons()

    def connect_smu(self, supply_num: int) -> None:
        visa_address = self.ui_config.supply[supply_num]["smu_address"].currentText()
        if not visa_address:
            return

        try:
            rm = visa.ResourceManager()
            instrument = rm.open_resource(visa_address)
            ping_response = instrument.query("*IDN?")  # type: ignore
            dev_id = tuple(ping_response.strip().split(","))
            self.ui_config.supply[supply_num]["smu_brand"].setText(dev_id[0])
            self.ui_config.supply[supply_num]["smu_model"].setText(dev_id[1])

            if self.ui_config.get_smu_ping_button_state(supply_num):
                self.ui_config.supply[supply_num]["smu_ping"].setText("Disconnect")
                self.ui_config.enable_smu_input(supply_num, True)

        except visa.VisaIOError as e:
            self.ui_config.supply[supply_num]["smu_brand"].setText("")
            self.ui_config.supply[supply_num]["smu_model"].setText("")
            self.ui_config.set_ping_button_state(supply_num, False)
            self.ui_config.supply[supply_num]["smu_address"].setCurrentIndex(0)
            QMessageBox.warning(
                None, "Connection Error", f"Failed to connect to SMU: {e}"
            )

    def _connect_buttons(self) -> None:
        for supply_num in SUPPLY_NUMBER:
            self.ui_config.supply[supply_num]["smu_ping"].clicked.connect(
                partial(self.connect_smu, supply_num)
            )
