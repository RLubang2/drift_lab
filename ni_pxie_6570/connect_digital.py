from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui_manager.user_interface_config import UserInterfaceConfig

from ni_pxie_6570.ni_digital import PXIE6570
from functools import partial

class ConnectDigital:
    def __init__(self, ui_config: UserInterfaceConfig) -> None:
        self.ui_config = ui_config
        self.nidigital_control = PXIE6570()
        self.ui_config.ni_button_ping.clicked.connect(partial(self._connect_digital))

    def _connect_digital(self) -> None:
        pxie_slot = self.ui_config.ni_slot_address.text()
        idn = self.nidigital_control.idn_intrument(pxie_slot)
        self.ui_config.ni_response.setText(idn)
