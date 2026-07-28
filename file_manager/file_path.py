from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui_manager.user_interface_config import UserInterfaceConfig

from PyQt6.QtWidgets import QFileDialog


class FilePath:
    def __init__(self, ui_config: UserInterfaceConfig) -> None:
        self.ui_config = ui_config
        self.ui_config.save_file_button.clicked.connect(self._browse_save_path)

    def _browse_save_path(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            None, "Save CSV", "results.csv", "CSV Files (*.csv)"
        )
        if path:
            self.ui_config.file_name.setText(path)
