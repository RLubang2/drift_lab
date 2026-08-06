from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui_manager.user_interface_config import UserInterfaceConfig

from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import Qt


class TableViewV2:
    def __init__(self, ui_config: UserInterfaceConfig) -> None:
        self.ui_config = ui_config
        self.table = self.ui_config.measure_tableview
        self.model = QStandardItemModel()
        self.table.setModel(self.model)

    def update_results(self, results: dict) -> None:
        self.model.clear()

        max_readings = max(
            (len(readings) for sites in results.values() for readings in sites.values()),
            default=0,
        )

        headers = [
            "Temperature",
            "Unit",
            *[f"Read {i}" for i in range(1, max_readings + 1)],
        ]
        self.model.setHorizontalHeaderLabels(headers)

        for temp, sites in results.items():
            for site, readings in sites.items():
                row_items = [
                    QStandardItem(str(temp)),
                    QStandardItem(str(site)),
                ]
                row_items.extend(QStandardItem(str(v)) for v in readings)

                for item in row_items:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                self.model.appendRow(row_items)

        self.table.resizeColumnsToContents()
