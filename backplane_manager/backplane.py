from ui_manager.user_interface_config import UserInterfaceConfig as UserInterfaceConfig
from backplane_manager.mux_control import SwitchBackplaneToDmm as DinToDmm
from backplane_manager.mux_control import SwitchBoardToBackplane as DutboardToDin
from backplane_manager.mux_control import EnableDmmMux as MuxDmm
from ni_pxie_6570.ni_digital import PXIE6570
from ui_manager.user_interface_variable import (
        DIN_OUT,
        DIN_OUT1,
        DIN_OUT2,
        DIN_OUT3,
        DIN_OUT4,
        DIN_OUT5,
        DIN_OUT6,
    )
from functools import partial

class BackplaneOutput:
    def __init__(self, ui_config: UserInterfaceConfig):
        self.ui_config = ui_config
        # self.pxie_slot = self.ui_config.ni_slot_address
        self.pxie_slot = None
        # self.voltage_hi = self.ui_config.ni_voltage_lvl.value()
        self.voltage_hi = 0
        self.voltage_lo = 0
        self.current_level =0
        # self.current_level = self.ui_config.ni_current_lvl.value()
        self.nidigital_control = None
        self.mux_dut_to_din = DutboardToDin(self.pxie_slot)
        self.mux_din_to_dmm = DinToDmm(self.pxie_slot)
        self.enable_mux_dmm = MuxDmm(self.pxie_slot)

        self.ping_ni_digital()

    def count_enable_output(self):
        for x in range(1,17):
            if self.ui_config.din_output[x]['outx'].isChecked():
                print(f"The out {x} is enabled")

    def ni_digital_idn(self):
        self.pxie_slot = self.ui_config.ni_slot_address.text()
        self.nidigital_control = NIDigital(self.pxie_slot)
    
        idn = self.nidigital_control.idn_intrument()
        self.ui_config.ni_response.setText(idn)

    def ping_ni_digital(self):
        self.ui_config.ni_button_ping.clicked.connect(partial(self.ni_digital_idn))

    def check_enabled_checkbox(self) -> bool:
        self.is_any_checked = any(self.ui_config.din_output[x]['outx'].isChecked() for x in range(1, DIN_OUT+1))
        # return print("true") if self.is_any_checked else print("false")
        return self.is_any_checked
    

    def check_out_1_16(self) -> bool:
        self.is_any_checked_in_1_16 = any(self.ui_config.din_output[x]['outx'].isChecked() for x in DIN_OUT1)
        # return print("true") if self.is_any_checked_in_1_16 else print("false")
        return self.is_any_checked_in_1_16
    

    def check_out_17_32(self) -> bool:
        self.is_any_checked_in_17_33 = any(self.ui_config.din_output[x]['outx'].isChecked() for x in DIN_OUT2)
        # return print("true") if self.is_any_checked_in_1_16 else print("false")
        return self.is_any_checked_in_17_33
    

    def check_out_33_48(self) -> bool:
        self.is_any_checked_in_33_48 = any(self.ui_config.din_output[x]['outx'].isChecked() for x in DIN_OUT3)
        # return print("true") if self.is_any_checked_in_1_16 else print("false")
        return self.is_any_checked_in_33_48
    

    def check_out_49_64(self) -> bool:
        self.is_any_checked_in_49_64 = any(self.ui_config.din_output[x]['outx'].isChecked() for x in DIN_OUT4)
        # return print("true") if self.is_any_checked_in_1_16 else print("false")
        return self.is_any_checked_in_49_64
    

    def check_out_65_80(self) -> bool:
        self.is_any_checked_in_65_80 = any(self.ui_config.din_output[x]['outx'].isChecked() for x in DIN_OUT5)
        # return print("true") if self.is_any_checked_in_1_16 else print("false")
        return self.is_any_checked_in_65_80
    

    def check_out_81_96(self) -> bool:
        self.is_any_checked_in_81_97 = any(self.ui_config.din_output[x]['outx'].isChecked() for x in DIN_OUT6)
        # return print("true") if self.is_any_checked_in_1_16 else print("false")
        return self.is_any_checked_in_81_97
    


    # def board_to_din_output1(self):
    #     """Enable U1 Mux"""
    #     u1_mux = self.enable_mux_dmm.enable_mux_u1()
    #     self.nidigital_control.force_voltage(u1_mux, self.voltage_hi, self.current_level)

    #     for x in DIN_OUT1:
    #         if self.ui_config.din_output[x]['outx'].isChecked():
    #             print("here")

    # def mux_matrix(self, x):
    #     if x in DIN_OUT1:
    #         self.dmm_mux = self.enable_mux_dmm.enable_mux_u1()
    #         return self.dmm_mux
        # elif x in 
        
    