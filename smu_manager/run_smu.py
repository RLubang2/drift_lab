from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui_manager.user_interface_config import UserInterfaceConfig

from smu_manager.keithley_24xx import Keithley24xx
from smu_manager.agilent_34xx import Agilent34xx
from ui_manager.user_interface_variable import SUPPLY_NUMBER


class RunSMU:
    def __init__(self, ui_config: UserInterfaceConfig) -> None:
        self.ui_config = ui_config
        self._connect_buttons()

    def run_smu(self, supply_num: int) -> None:
        visa_address = self.ui_config.get_smu_address(supply_num)
        voltage = self.ui_config.get_smu_voltage(supply_num)
        current = self.ui_config.get_smu_current(supply_num)
        mode = self.ui_config.get_smu_mode(supply_num)
        model = self.ui_config.get_smu_model(supply_num)
        run_state = self.ui_config.get_smu_run_button_state(supply_num)

        if model == "MODEL 2400":
            smu = Keithley24xx(visa_address)
            if run_state:
                self.ui_config.set_channel_enabled(supply_num, False)
                smu.run_keithley_24xx(mode, voltage, current)
                self.ui_config.enable_smu_input(supply_num, False)
            else:
                smu.smu_output_off()
                smu.smu_reset()
                self.ui_config.enable_smu_input(supply_num, True)

        elif model == "E3631A":
            smu = Agilent34xx(visa_address)
            if run_state:
                self.ui_config.set_channel_enabled(supply_num, True)
                channel = self.ui_config.get_smu_channel(supply_num)
                smu.run_agilent_34xx(mode, voltage, current, channel)
                self.ui_config.enable_smu_input(supply_num, False)
            else:
                smu.smu_output_off()
                smu.smu_reset()
                self.ui_config.enable_smu_input(supply_num, True)

    def _connect_buttons(self) -> None:
        for supply_num in SUPPLY_NUMBER:
            self.ui_config.supply[supply_num]["smu_run"].clicked.connect(
                partial(self.run_smu, supply_num)
            )
