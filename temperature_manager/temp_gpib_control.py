from __future__ import annotations

import time
from typing import TYPE_CHECKING, Optional, Any

if TYPE_CHECKING:
    from ui_manager.user_interface_config import UserInterfaceConfig

import pyvisa as visa
from PyQt6.QtWidgets import QMessageBox

from temperature_manager.tempe_base import TempBase


class TempGPIBControl(TempBase):
    def __init__(self, ui_config: UserInterfaceConfig) -> None:
        self.ui_config = ui_config
        self.watlow: Optional[Any] = None
        self.rm = visa.ResourceManager()

    def connect_dev(self) -> None:
        visa_address = self.ui_config.temp_address.currentText()

        if self.ui_config.temp_address.currentIndex() == 0:
            QMessageBox.critical(None, "Connection Error", "Please select a valid GPIB address.")
            return
        
        try:
            self.watlow = self.rm.open_resource(visa_address)
        except visa.VisaIOError as e:
            QMessageBox.critical(None, "Connection Error", f"Failed to connect to device: {e}")

    def hardware_info(self) -> None:
        if self.watlow is None:
            return
        try:
            self.watlow.query("*IDN?")
        except visa.VisaIOError as e:
            QMessageBox.critical(None, "Unable to get hardware info", f"Error: {e}")

    def temp_write_setpoint(self, temp_target: float) -> None:
        if self.watlow is None:
            return
        try:
            self.watlow.write(f"W 300, {temp_target * 10}")
        except visa.VisaIOError as e:
            QMessageBox.critical(None, "Unable to write setpoint", f"Error: {e}")

    def temp_read_setpoint(self) -> Optional[float]:
        if self.watlow is None:
            return None
        try:
            temp = self.watlow.write(f"R? 100, 1")
            return temp * 0.1
        except visa.VisaIOError as e:
            QMessageBox.critical(None, "Unable to read setpoint", f"Error: {e}")
            return None

    def temp_soak_time(self, soak_time: int, temp_target: float) -> None:
        while True:
            current_temp = self.temp_read_setpoint()
            if current_temp is None:
                return
            
            if abs(current_temp - temp_target) <= 1:
                break
            
            time.sleep(1)  # Wait for 1 second before checking again
            
        time.sleep(soak_time)

    def close_dev(self) -> None:
        if self.watlow is None:
            return None
        self.watlow.close()

    def _dev_list(self) -> None:
        pass
