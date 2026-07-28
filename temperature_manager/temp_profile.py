from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui_manager.user_interface_config import UserInterfaceConfig

from PyQt6.QtGui import QStandardItem


class CustomTempProfile:
    def __init__(self, ui_config: UserInterfaceConfig) -> None:
        self.ui_config = ui_config
        self.ui_config.add_row_button.clicked.connect(self._add_row)
        self.ui_config.rem_row_button.clicked.connect(self._remove_row)

    def _add_row(self) -> None:
        self.ui_config.temp_model.appendRow([QStandardItem("20")])

    def _remove_row(self) -> None:
        selected = self.ui_config.temp_table.selectionModel().selectedIndexes()  # type: ignore
        if selected:
            self.ui_config.temp_model.removeRow(selected[0].row())
        elif self.ui_config.temp_model.rowCount() > 0:
            self.ui_config.temp_model.removeRow(
                self.ui_config.temp_model.rowCount() - 1
            )


class RampTempProfile:
    def __init__(self, ui_config: UserInterfaceConfig) -> None:
        self.ui_config = ui_config
        self.ui_config.temp_start_ramp.setRange(-100, 1000)
        self.ui_config.temp_end_ramp.setRange(-100, 1000)
        self.ui_config.temp_inc_ramp.setRange(-100, 1000)
