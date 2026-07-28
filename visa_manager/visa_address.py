from __future__ import annotations

import pyvisa as visa
from PyQt6 import QtWidgets


class VisaAddressList:
    def __init__(self) -> None:
        try:
            self.rm = visa.ResourceManager()
        except visa.VisaIOError as e:
            QtWidgets.QMessageBox.critical(
                None, "Error", f"Failed to initialize VISA Resource Manager: {e}"
            )
            raise

    def get_addresses(self) -> list[str]:
        try:
            return list(self.rm.list_resources()) if self.rm else []
        except visa.VisaIOError:
            return []

    def populate_combobox(self, combobox: QtWidgets.QComboBox) -> None:
        try:
            resource_list = self.get_addresses()
            combobox.clear()
            combobox.addItem("Select Equipment Address")

            for resource in resource_list:
                combobox.addItem(resource)

            if not resource_list:
                combobox.addItem("No VISA devices found")
        except visa.VisaIOError:
            combobox.clear()
