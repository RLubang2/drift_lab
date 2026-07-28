from __future__ import annotations

try:
    from .mux_config import (
        MUX7, MUX8, MUX9, MUX10, MUX11, MUX12, MUX13, MUX14,
        MUX15, MUX16, MUX17,
    )
except ImportError:
    from mux_config import (
        MUX7, MUX8, MUX9, MUX10, MUX11, MUX12, MUX13, MUX14,
        MUX15, MUX16, MUX17,
    )

_BOARD_TO_BACKPLANE_MAP: dict[int, tuple[int, ...]] = {
    0: (MUX7, MUX8, MUX9, MUX10),
    1: (MUX7, MUX8, MUX9, MUX10),
    2: (MUX7,),
    3: (MUX8,),
    4: (MUX7, MUX8),
    5: (MUX9,),
    6: (MUX7, MUX9),
    7: (MUX8, MUX9),
    8: (MUX7, MUX8, MUX9),
    9: (MUX10,),
    10: (MUX7, MUX10),
    11: (MUX8, MUX10),
    12: (MUX7, MUX8, MUX10),
    13: (MUX9, MUX10),
    14: (MUX7, MUX9, MUX10),
    15: (MUX8, MUX9, MUX10),
}

_BACKPLANE_TO_DMM_MAP: dict[int, tuple[int, ...]] = {
    0: (MUX11, MUX12, MUX13, MUX14),
    1: (MUX11, MUX12, MUX13, MUX14),
    2: (MUX11,),
    3: (MUX12,),
    4: (MUX11, MUX12),
    5: (MUX13,),
    6: (MUX11, MUX13),
    7: (MUX12, MUX13),
    8: (MUX11, MUX12, MUX13),
    9: (MUX14,),
    10: (MUX11, MUX14),
    11: (MUX12, MUX14),
    12: (MUX11, MUX12, MUX14),
    13: (MUX13, MUX14),
    14: (MUX11, MUX13, MUX14),
    15: (MUX12, MUX13, MUX14),
}


def _channels_to_string(channels: tuple[int, ...]) -> str:
    return ", ".join(str(ch) for ch in channels)


class SwitchBoardToBackplane:
    def switch(self, value: int) -> str:
        channels = _BOARD_TO_BACKPLANE_MAP.get(value)
        if channels is None:
            raise ValueError(f"Invalid switch value: {value}")
        return _channels_to_string(channels)

    def reset(self) -> str:
        return _channels_to_string((MUX7, MUX8, MUX9, MUX10))


class SwitchBackplaneToDmm:
    def switch(self, value: int) -> str:
        channels = _BACKPLANE_TO_DMM_MAP.get(value)
        if channels is None:
            raise ValueError(f"Invalid switch value: {value}")
        return _channels_to_string(channels)

    def case_1(self) -> str:
        return _channels_to_string(_BACKPLANE_TO_DMM_MAP[1])

    def case_2(self) -> str:
        return _channels_to_string(_BACKPLANE_TO_DMM_MAP[2])

    def case_3(self) -> str:
        return _channels_to_string(_BACKPLANE_TO_DMM_MAP[3])

    def case_4(self) -> str:
        return _channels_to_string(_BACKPLANE_TO_DMM_MAP[4])

    def case_5(self) -> str:
        return _channels_to_string(_BACKPLANE_TO_DMM_MAP[5])

    def case_6(self) -> str:
        return _channels_to_string(_BACKPLANE_TO_DMM_MAP[6])

    def reset(self) -> str:
        return _channels_to_string((MUX11, MUX12, MUX13, MUX14))


class EnableDmmMux:
    def enable_mux_u1(self) -> str:
        return str(MUX15)

    def enable_mux_u3(self) -> str:
        return str(MUX16)

    def enable_mux_u2_u4(self) -> str:
        return str(MUX17)
