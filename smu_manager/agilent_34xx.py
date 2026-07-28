from __future__ import annotations

import time
from typing import Optional

import pyvisa as visa

from smu_manager.smu_base import SMUBase


class Agilent34xx(SMUBase):
    def __init__(self, visa_address: str) -> None:
        self.visa_address = visa_address
        self.rm = visa.ResourceManager()
        self.instrument = None

    def smu_visa_connect(self, visa_address: str) -> None:
        try:
            self.instrument = self.rm.open_resource(visa_address)
            self.visa_address = visa_address
        except visa.VisaIOError:
            pass

    def smu_query(self) -> Optional[str]:
        if not self.instrument:
            return None
        try:
            return self.instrument.query("*IDN?")  # type: ignore
        except visa.VisaIOError:
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
        self.smu_write(f":SOURce:FUNCtion {mode}")

    def smu_set_voltage(self, voltage: float) -> None:
        self.smu_write(f":SOURce:VOLTage {voltage}")

    def smu_set_current(self, current: float) -> None:
        self.smu_write(f":SOURce:CURRent {current}")

    def smu_output_on(self) -> None:
        self.smu_write(":OUTPut ON")

    def smu_output_off(self) -> None:
        self.smu_write(":OUTPut OFF")

    def smu_close(self) -> None:
        if self.instrument:
            self.instrument.close()

    def set_current_limit(self, current: float) -> None:
        self.smu_write(f"SENS:CURR:PROT {current}")

    def set_voltage_limit(self, voltage: float) -> None:
        self.smu_write(f"SENS:VOLT:PROT {voltage}")

    def select_channel(self, channel: int) -> None:
        self.smu_write(f":INSTrument:NSELect {channel}")

    def run_agilent_34xx(
        self, mode: str, voltage: float, current: float, channel: int
    ) -> None:
        self.select_channel(channel)
        self.smu_mode(mode)
        time.sleep(0.1)
        self.smu_set_voltage(voltage)
        self.smu_set_current(current)
        time.sleep(0.1)
        self.smu_output_on()

    def stop_agilent_34xx(self) -> None:
        self.smu_output_off()
