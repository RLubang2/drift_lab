from __future__ import annotations

import csv
from pathlib import Path
from datetime import datetime
from typing import Optional, IO


class SaveManager:
    def __init__(self) -> None:
        self._file: Optional[IO] = None
        self._writer: Optional[csv.writer] = None
        self._file_path: Optional[Path] = None
        self._header_written: bool = False

    def open_file(self, file_path: str = "") -> str:
        if file_path:
            save_path = Path(file_path)
        else:
            default_dir = (
                Path("C:/Measurement")
                if Path("C:/").exists()
                else Path.home() / "Measurement"
            )
            default_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = default_dir / f"Measurement_{timestamp}.csv"

        self._file_path = save_path
        self._file = open(save_path, "w", newline="")
        self._writer = csv.writer(self._file)
        self._header_written = False
        return str(save_path)

    def save_result(self, temp: str | float, result: dict) -> None:
        if self._writer is None:
            raise RuntimeError("CSV file is not open. Call open_file() first.")

        if not self._header_written:
            first_site = next(iter(result))
            read_count = len(result[first_site])
            header = ["Temp", "Site"] + [f"Reading{i + 1}" for i in range(read_count)]
            self._writer.writerow(header)
            self._header_written = True

        for site, readings in result.items():
            self._writer.writerow([temp, site, *readings])

        if self._file:
            self._file.flush()

    def close_file(self) -> None:
        if self._file:
            self._file.close()
        self._file = None
        self._writer = None
        self._file_path = None
        self._header_written = False
