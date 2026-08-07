from abc import ABC, abstractmethod


class TempBase(ABC):
    @abstractmethod
    def connect_dev(self) -> None:
        pass

    @abstractmethod
    def hardware_info(self) -> str | None:
        pass

    @abstractmethod
    def temp_write_setpoint(self, temp_target) -> None:
        pass

    @abstractmethod
    def temp_read_setpoint(self) -> float | None:
        pass

    @abstractmethod
    def temp_soak_time(self, soak_time: int, temp_target: float, abort_check) -> None:
        pass

    @abstractmethod
    def close_dev (self) -> None:
        pass
    
    @abstractmethod
    def _dev_list(self) -> None:
        pass
