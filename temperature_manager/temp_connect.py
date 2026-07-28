from temperature_manager.temp_run import RunTemp
from ui_manager.user_interface_config import UserInterfaceConfig
from functools import partial


class TempConnect:
    def __init__(self, ui_config: UserInterfaceConfig):
        self.ui_config = ui_config
        self.temp_run = RunTemp(ui_config)
        self.ui_config.temp_ping_button.clicked.connect(partial(self._connect_temp))

    def _connect_temp(self) -> None:
        self.temp_run.connect_dev()

        id = self.temp_run.hardware_info()
        if id:
            self.ui_config.temp_response.setText(id)
        else:
            return