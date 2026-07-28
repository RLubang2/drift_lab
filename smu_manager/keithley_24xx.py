from __future__ import annotations

import time
from typing import Optional

import pyvisa as visa
from PyQt6.QtWidgets import QMessageBox

from smu_manager.smu_base import SMUBase


class Keithley24xx(SMUBase):
    def __init__(self, visa_address: str) -> None:
        self.visa_address = visa_address
        self.rm = visa.ResourceManager()
        self.instrument = None
        self.smu_visa_connect(self.visa_address)

    def smu_visa_connect(self, visa_address: str) -> None:
        try:
            self.instrument = self.rm.open_resource(visa_address)
        except visa.VisaIOError as e:
            QMessageBox.critical(None, "Failed to connect", f"Error {e}")

    def smu_query(self) -> Optional[str]:
        if not self.instrument:
            QMessageBox.critical(None, "Failed to query SMU", "No instrument connected")
            return None
        try:
            return self.instrument.query("*IDN?")  # type: ignore
        except visa.VisaIOError as e:
            QMessageBox.critical(None, "Failed to query SMU", f"Error {e}")
            return None

    def smu_reset(self) -> None:
        if not self.instrument:
            return
        try:
            self.instrument.write("*RST")  # type: ignore
        except visa.VisaIOError:
            pass

    def smu_write(self, command: str) -> None:
        if not self.instrument:
            return
        try:
            self.instrument.write(command)  # type: ignore
        except visa.VisaIOError:
            pass

    def smu_mode(self, mode: str) -> None:
        self.smu_write(f"SOUR:FUNC {mode}")

    def smu_set_voltage(self, voltage: float) -> None:
        self.smu_write(f"SOUR:VOLT {voltage}")

    def smu_set_current(self, current: float) -> None:
        self.smu_write(f"SOUR:CURR {current}")

    def smu_output_on(self) -> None:
        self.smu_write("OUTP ON")

    def smu_output_off(self) -> None:
        self.smu_write("OUTP OFF")

    def smu_close(self) -> None:
        if self.instrument:
            self.instrument.close()

    def set_current_limit(self, current: float) -> None:
        self.smu_write(f"SENS:CURR:PROT {current}")

    def set_voltage_limit(self, voltage: float) -> None:
        self.smu_write(f"SENS:VOLT:PROT {voltage}")

    def select_channel(self, channel: int) -> None:
        pass

    def run_keithley_24xx(self, mode: str, voltage: float, current: float) -> None:
        self.smu_mode(mode)
        time.sleep(0.1)
        if mode == "VOLT":
            self.smu_set_voltage(voltage)
            self.set_current_limit(current)
        elif mode == "CURR":
            self.smu_set_current(current)
            self.set_voltage_limit(voltage)
        time.sleep(0.1)
        self.smu_output_on()

    def stop_keithley_24xx(self) -> None:
        self.smu_output_off()
