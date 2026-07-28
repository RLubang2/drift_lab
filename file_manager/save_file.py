from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui_manager.user_interface_config import UserInterfaceConfig

from PyQt6.QtWidgets import QFileDialog


class SaveFile:
    def __init__(self, ui_config: UserInterfaceConfig) -> None:
        self.ui_config = ui_config
        self.ui_config.save_file_button.clicked.connect(self._save_file)

    def _save_file(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(
            None, "Save File", "", "CSV file (*.csv)"
        )
        if file_path:
            if not file_path.endswith(".csv"):
                file_path += ".csv"
            self.ui_config.file_name.setText(file_path)
