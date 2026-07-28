from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui_manager.user_interface_config import UserInterfaceConfig

from ui_manager.user_interface_variable import (
    DIN_OUT, DIN_OUT1, DIN_OUT2, DIN_OUT3, DIN_OUT4, DIN_OUT5, DIN_OUT6,
)


class CheckEnableOutput:
    def __init__(self, ui_config: UserInterfaceConfig) -> None:
        self.ui_config = ui_config

    def _is_group_checked(self, group: range) -> bool:
        return any(
            self.ui_config.din_output[x]["outx"].isChecked() for x in group
        )

    def check_enabled_checkbox(self) -> bool:
        return self._is_group_checked(range(1, DIN_OUT + 1))

    def check_out_1_16(self) -> bool:
        return self._is_group_checked(DIN_OUT1)

    def check_out_17_32(self) -> bool:
        return self._is_group_checked(DIN_OUT2)

    def check_out_33_48(self) -> bool:
        return self._is_group_checked(DIN_OUT3)

    def check_out_49_64(self) -> bool:
        return self._is_group_checked(DIN_OUT4)

    def check_out_65_80(self) -> bool:
        return self._is_group_checked(DIN_OUT5)

    def check_out_81_96(self) -> bool:
        return self._is_group_checked(DIN_OUT6)
