from __future__ import annotations

import logging
from typing import Optional

import nidigital
from PyQt6.QtWidgets import QMessageBox


logger = logging.getLogger(__name__)


class PXIE6570:
    def __init__(self) -> None:
        self._session: Optional[nidigital.Session] = None

    def idn_intrument(self, resource_name: str) -> str:
        try:
            with nidigital.Session(resource_name=resource_name, id_query=True) as session:
                return session.instrument_model
        except nidigital.Error as e:
            QMessageBox.warning(
                None, "IDN Query Error", f"Failed to query instrument ID: {e}"
            )
            return ""

    def force_voltage(
        self,
        resource_name: str,
        channels: str,
        voltage: float,
        current_limit: float,
    ) -> None:
        try:
            with nidigital.Session(resource_name=resource_name) as session:
                ch = session.channels[channels]
                ch.selected_function = nidigital.SelectedFunction.PPMU
                ch.ppmu_output_function = nidigital.PPMUOutputFunction.VOLTAGE
                ch.ppmu_voltage_level = voltage
                ch.ppmu_current_limit_range = current_limit
                ch.ppmu_source()
        except nidigital.Error as e:
            QMessageBox.warning(
                None, "Force Voltage Error", f"Failed to force voltage: {e}"
            )
        except Exception as e:
            logger.error("Error forcing voltage: %s", e)

    def reset_nidigital(self, resource_name: str) -> None:
        try:
            with nidigital.Session(resource_name=resource_name) as session:
                session.reset()
        except nidigital.Error as e:
            QMessageBox.warning(
                None, "Reset Error", f"Failed to reset NI Digital device: {e}"
            )
            return ""

    def disconnect_channel(self, resource_name: str, channels: str) -> None:
        try:
            with nidigital.Session(resource_name=resource_name) as session:
                session.channels[channels].selected_function = (
                    nidigital.SelectedFunction.DISCONNECT
                )
        except nidigital.Error as e:
            QMessageBox.warning(
                None, "Disconnect Error", f"Failed to disconnect: {e}"
            )
