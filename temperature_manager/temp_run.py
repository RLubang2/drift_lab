from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ui_manager.user_interface_config import UserInterfaceConfig

from temperature_manager.temp_gpib_control import TempGPIBControl
from temperature_manager.temp_serial_control import TempSerialControl
from temperature_manager.tempe_base import TempBase


class RunTemp:
    def __init__(self, ui_config: UserInterfaceConfig) -> None:
        self.ui_config = ui_config
        self.serial_comm = TempSerialControl(ui_config)
        self.gpib_comm = TempGPIBControl(ui_config)

    @property
    def controller(self) -> TempBase:
        if self.ui_config.temp_tab_comm.currentIndex() == 0:
            return self.gpib_comm
        return self.serial_comm

    def connect_dev(self) -> None:
        return self.controller.connect_dev()

    def hardware_info(self) -> Optional[str]:
        return self.controller.hardware_info()

    def temp_write(self, temp: float) -> None:
        return self.controller.temp_write_setpoint(temp)

    def temp_read(self) -> Optional[float]:
        return self.controller.temp_read_setpoint()

    def temp_soak(self, temp: float, abort_check=None) -> None:
        soak_time = self.ui_config.temp_soak_time.value()
        return self.controller.temp_soak_time(soak_time, temp, abort_check=abort_check)

    def temp_close(self):
        return self.controller.close_dev()
