from __future__ import annotations

from typing import Any, Optional

import pyvisa as visa
from PyQt6.QtWidgets import QMessageBox

_VOLTAGE_RANGES: dict[int, str] = {
    0: "100e-3", 1: "1", 2: "10", 3: "100", 4: "1000",
}

_CURRENT_RANGES: dict[int, str] = {
    0: "100e-9", 1: "1e-6", 2: "10e-6", 3: "100e-6",
    4: "1e-3", 5: "10e-3", 6: "100e-3", 7: "1",
}

_RANGE_MAP: dict[int, dict[int, str]] = {0: _VOLTAGE_RANGES, 1: _CURRENT_RANGES}
_FUNCTION_MAP: dict[int, str] = {0: "DCV", 1: "DCI"}


class DmmMeasurement:
    def __init__(self) -> None:
        self.rm: visa.ResourceManager = visa.ResourceManager()
        self.dmm: Optional[Any] = None

    def dmm_connect(self, visa_address: str) -> Optional[Any]:
        try:
            self.dmm = self.rm.open_resource(visa_address)
            return self.dmm
        except visa.VisaIOError as e:
            QMessageBox.critical(None, "Unable to connect", f"Error connecting: {e}")
            self.dmm = None
            return None

    def dmm_write(self, command: str) -> None:
        if self.dmm is None:
            QMessageBox.critical(None, "Unable to write", "No instrument connected")
            return
        try:
            self.dmm.write(command)
        except visa.VisaIOError as e:
            QMessageBox.critical(None, "Unable to write", f"Error: {e}")

    def dmm_query(self, command: str) -> Optional[str]:
        if self.dmm is None:
            QMessageBox.critical(None, "Unable to query", "No instrument connected")
            return None
        try:
            return self.dmm.query(command)
        except visa.VisaIOError as e:
            QMessageBox.critical(None, "Unable to query", f"Error: {e}")
            return None

    def dmm_range(self, mode: int, meas_range: int) -> Optional[str]:
        return _RANGE_MAP.get(mode, {}).get(meas_range)

    def dmm_function(self, index: int) -> Optional[str]:
        return _FUNCTION_MAP.get(index)

    def dmm_read(self) -> Optional[str]:
        if self.dmm is None:
            QMessageBox.critical(None, "Unable to read", "No instrument connected")
            return None
        try:
            return self.dmm.read()
        except visa.VisaIOError as e:
            QMessageBox.critical(None, "Unable to read", f"Error: {e}")
            return None

    def dmm_clear(self) -> None:
        if self.dmm is None:
            return
        try:
            self.dmm.clear()
        except visa.VisaIOError as e:
            QMessageBox.critical(None, "Unable to clear", f"Error: {e}")

    def dmm_close(self) -> None:
        if self.dmm is None:
            return
        try:
            self.dmm.close()
        except visa.VisaIOError as e:
            QMessageBox.critical(None, "Unable to close", f"Error: {e}")

    def dmm_reset(self) -> None:
        self.dmm_write("PRESET NORM")
        self.dmm_clear()
