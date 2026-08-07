from __future__ import annotations

import time
from typing import TYPE_CHECKING, Optional, Any

if TYPE_CHECKING:
    from ui_manager.user_interface_config import UserInterfaceConfig

import serial
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException
import time
from PyQt6.QtSerialPort import QSerialPortInfo
from PyQt6.QtWidgets import QMessageBox

from temperature_manager.tempe_base import TempBase


class TempSerialControl(TempBase):
    def __init__(self, ui_config: UserInterfaceConfig) -> None:
        self.ui_config = ui_config
        self.watlow = None
        self._dev_list()

    def connect_dev(self) -> None:
        port = self.ui_config.serial_port.currentText()
        baudrate = self.ui_config.baudrate.value()
        # self.address = self.ui_config.serial_address.value()

        

        if self.ui_config.serial_port.currentIndex() == 0:
            QMessageBox.critical(None, "Connection Error", "Please select a valid serial port.")
            return
        
        try:
            self.watlow = ModbusSerialClient(
                        port = port,
                        baudrate = baudrate,
                        parity="N",
                        stopbits=1,
                        bytesize=8,
                        timeout=1
                    )
            
            self.watlow.connect()

        except ModbusException  as e:
            QMessageBox.critical(None, "Connection Error", f"Failed to connect to device: {e}")

    def hardware_info(self) -> str| None:
        dev_address = self.ui_config.serial_address.value()

        if self.watlow is None:
            return
        try:

            dev_id_register = self.watlow.read_holding_registers(
                address = 0,
                count = 1,
                device_id = dev_address
            )

            dev_id = dev_id_register.registers[0]

            chunk = [int(str(dev_id)[i:i+2]) for i in range(0, len(str(dev_id)), 2)]
            result = "".join(chr(val) for val in chunk)

            return result

        except ModbusException as e:
            QMessageBox.critical(None, "Unable to get hardware info", f"Error: {e}")
            return None

    def temp_write_setpoint(self, temp_target) -> None:
        dev_address = self.ui_config.serial_address.value()
        temp_target = int(temp_target)

        if temp_target < 0:
            temp_target = temp_target & 0xFFFF

        if self.watlow is None:
            return
        try:
            self.watlow.write_register(
                address = 300,
                value = temp_target,
                device_id = dev_address
                )
        except ModbusException as e:
            QMessageBox.critical(None, "Unable to set temperature", f"Error: {e}")

    def temp_read_setpoint(self) -> Optional[float]:
        dev_address = self.ui_config.serial_address.value()

        if self.watlow is None:
            return None
        try:
            temp = self.watlow.read_holding_registers(
                address = 100,
                count = 1,
                device_id = dev_address
            )

            return temp.registers[0]
        
        except ModbusException as e:
            QMessageBox.critical(None, "Unable to read", f"Error: {e}")
            return None

    def temp_soak_time(self, soak_time: int, temp_target: float, abort_check=None) -> None:
        while True:
            if abort_check is not None and abort_check():
                return

            current_temp = self.temp_read_setpoint()

            if current_temp is None:
                return
            coverted_temp = current_temp - 65536 if current_temp > 32767 else current_temp

            if abs(abs(coverted_temp) - abs(temp_target)) <= 1:
                break

            time.sleep(5)
            
        if abort_check is not None and abort_check():
            return

        time.sleep(soak_time)

    def close_dev(self):
        if self.watlow is None:
            return None

        self.watlow.close()


    def _dev_list(self) -> None:
        port_list = self.ui_config.serial_port
        port_list.clear()
        port_list.addItem("Select Port")

        for port in QSerialPortInfo.availablePorts():
            display = port.portName()
            # if port.description():
            #     display += f" - {port.description()}"
            port_list.addItem(display, port.portName())
