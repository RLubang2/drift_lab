from __future__ import annotations

import time
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ui_manager.user_interface_config import UserInterfaceConfig

from measurement_manager.dmm import DmmMeasurement


class RunDMM:
    def __init__(self, ui_config: UserInterfaceConfig) -> None:
        self.ui_config = ui_config
        self.keysight_3458 = DmmMeasurement()

    def init_device(self) -> None:
        visa_address = self.ui_config.meas_address.currentText()
        dev_mode = self.ui_config.meas_mode.currentIndex()
        dev_range = self.ui_config.meas_range.currentIndex()

        range_val = self.keysight_3458.dmm_range(dev_mode, dev_range)
        sample = self.ui_config.meas_sample.value()
        function = self.keysight_3458.dmm_function(dev_mode)

        self.keysight_3458.dmm_connect(visa_address)
        time.sleep(1)
        self.keysight_3458.dmm_clear()

        commands = [
            "PRESET NORM",
            "OFORMAT ASCII",
            f"{function} {range_val}",
            f"NPLC {sample}",
            "NDIG 9",
            "AZERO ON",
            "TRIG AUTO",
            "END ALWAYS",
        ]
        for cmd in commands:
            self.keysight_3458.dmm_write(cmd)

    def read_output(self) -> Optional[str]:
        self.keysight_3458.dmm_write("TARM HOLD")
        time.sleep(0.2)
        self.keysight_3458.dmm_write("TARM SGL, 1")
        time.sleep(0.2)
        result = self.keysight_3458.dmm_read()
        time.sleep(0.2)
        self.keysight_3458.dmm_clear()
        time.sleep(0.2)
        return result

    def dev_clear(self) -> None:
        self.keysight_3458.dmm_clear()

    def dev_close(self) -> None:
        self.keysight_3458.dmm_close()

    def dev_reset(self) -> None:
        self.keysight_3458.dmm_reset()
