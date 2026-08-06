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

        rows = self._normalize_results(results)

        max_readings = max((len(readings) for _, _, readings in rows), default=0)

        headers = [
            "Temperature",
            "Unit",
            *[f"Read {i}" for i in range(1, max_readings + 1)],
        ]
        self.model.setHorizontalHeaderLabels(headers)

        for temp, site, readings in rows:
            row_items = [
                QStandardItem(str(temp)),
                QStandardItem(str(site)),
            ]
            row_items.extend(QStandardItem(str(v)) for v in readings)

            for item in row_items:
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.model.appendRow(row_items)

        self.table.resizeColumnsToContents()

    def _normalize_results(self, results: dict) -> list[tuple[object, object, list[object]]]:
        rows: list[tuple[object, object, list[object]]] = []

        if not isinstance(results, dict):
            return rows

        for top_key, top_value in results.items():
            if not isinstance(top_value, dict):
                continue

            nested_values = list(top_value.values())
            nested_is_list_of_lists = any(
                isinstance(value, list) and value and isinstance(value[0], list)
                for value in nested_values
            )

            if nested_is_list_of_lists:
                # Shape: site -> temp -> [reading_sets]
                for nested_key, nested_value in top_value.items():
                    if not isinstance(nested_value, list):
                        continue
                    for readings in nested_value:
                        rows.append((nested_key, top_key, list(readings)))
            else:
                # Shape: temp -> site -> readings
                for nested_key, readings in top_value.items():
                    if isinstance(readings, dict):
                        continue
                    if isinstance(readings, list):
                        rows.append((top_key, nested_key, list(readings)))
                    else:
                        rows.append((top_key, nested_key, [readings]))

        return rows
