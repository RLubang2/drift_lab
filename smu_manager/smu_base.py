from abc import ABC, abstractmethod


class SMUBase(ABC):
    @abstractmethod
    def smu_visa_connect(self, visa_address: str) -> None:
        pass

    @abstractmethod
    def smu_query(self) -> str | None:
        pass

    @abstractmethod
    def smu_reset(self) -> None:
        pass

    @abstractmethod
    def smu_write(self, command: str) -> None:
        pass

    @abstractmethod
    def smu_mode(self, mode: str) -> None:
        pass

    @abstractmethod
    def smu_set_voltage(self, voltage: float) -> None:
        pass

    @abstractmethod
    def smu_set_current(self, current: float) -> None:
        pass

    @abstractmethod
    def smu_output_on(self) -> None:
        pass

    @abstractmethod
    def smu_output_off(self) -> None:
        pass

    @abstractmethod
    def smu_close(self) -> None:
        pass

    @abstractmethod
    def set_current_limit(self, current: float) -> None:
        pass

    @abstractmethod
    def set_voltage_limit(self, voltage: float) -> None:
        pass

    @abstractmethod
    def select_channel(self, channel: int) -> None:
        pass
