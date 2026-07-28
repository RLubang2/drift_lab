
from backplane_manager.mux_config import (
    MUX0, MUX1, MUX2, MUX3, MUX4, MUX5, MUX6, MUX7, MUX8, MUX9,
    MUX10, MUX11, MUX12, MUX13, MUX14, MUX15, MUX16, MUX17, MUX18, MUX19, MUX20
)


class SwitchBoardToBackplane:
    def __init__(self, resource_name) -> None:
        self.resource_name = resource_name
    
    def case_1(self):
        # Enable S1
        return f'{self.resource_name}/{MUX7}, {self.resource_name}/{MUX8}, {self.resource_name}/{MUX9}, {self.resource_name}/{MUX10}'
    
    def case_2(self):
        # Enable S2
        return f'{self.resource_name}/{MUX7}'
    
    def case_3(self):
        # Enable S3
        return f'{self.resource_name}/{MUX8}'
    
    def case_4(self):
        # Enable S4
        return f'{self.resource_name}/{MUX7}, {self.resource_name}/{MUX8}'
    
    def case_5(self):
        # Enable S5
        return f'{self.resource_name}/{MUX9}'
    
    def case_6(self):
        # Enable S6
        return f'{self.resource_name}/{MUX7}, {self.resource_name}/{MUX9}'
    
    def case_7(self):
        # Enable S7
        return f'{self.resource_name}/{MUX8}, {self.resource_name}/{MUX9}'
    
    def case_8(self):
        # Enable S8
        return f'{self.resource_name}/{MUX7}, {self.resource_name}/{MUX8}, {self.resource_name}/{MUX9}'
    
    def case_9(self):
        # Enable S9
        return f'{self.resource_name}/{MUX10}'
    
    def case_10(self):
        # Enable S10
        return f'{self.resource_name}/{MUX7}, {self.resource_name}/{MUX10}'
    
    def case_11(self):
        # Enable S11
        return f'{self.resource_name}/{MUX8}, {self.resource_name}/{MUX10}'
    
    def case_12(self):
        # Enable S12
        return f'{self.resource_name}/{MUX7}, {self.resource_name}/{MUX8}, {self.resource_name}/{MUX10}'
    
    def case_13(self):  
        # Enable S13
        return f'{self.resource_name}/{MUX9}, {self.resource_name}/{MUX10}'
    
    def case_14(self):
        # Enable S14
        return f'{self.resource_name}/{MUX7}, {self.resource_name}/{MUX9}, {self.resource_name}/{MUX10}'    
    
    def case_15(self):
        # Enable S15
        return f'{self.resource_name}/{MUX8}, {self.resource_name}/{MUX9}, {self.resource_name}/{MUX10}'    
    
    def case_0(self):
        # Enable S16
        return f'{self.resource_name}/{MUX7}, {self.resource_name}/{MUX8}, {self.resource_name}/{MUX9}, {self.resource_name}/{MUX10}'
    
    def switch(self, value):
        # getattr fetches the case_ method by name and calls it to return the channel string
        return getattr(self, f"case_{value}")()
    
    def reset(self):
        return f'{self.resource_name}/{MUX7}, {self.resource_name}/{MUX8}, {self.resource_name}/{MUX9}, {self.resource_name}/{MUX10}'

class SwitchBackplaneToDmm:
    def __init__(self, resource_name) -> None:
        self.resource_name = resource_name
    
    def case_1(self):
        # Enable S1
        return f'{self.resource_name}/{MUX11}, {self.resource_name}/{MUX12}, {self.resource_name}/{MUX13}, {self.resource_name}/{MUX14}'
    
    def case_2(self):
        # Enable S2
        return f'{self.resource_name}/{MUX11}'
    
    def case_3(self):
        # Enable S3
        return f'{self.resource_name}/{MUX12}'
    
    def case_4(self):
        # Enable S4
        return f'{self.resource_name}/{MUX11}, {self.resource_name}/{MUX12}'
    
    def case_5(self):
        # Enable S5
        return f'{self.resource_name}/{MUX13}'
    
    def case_6(self):
        # Enable S6
        return f'{self.resource_name}/{MUX11}, {self.resource_name}/{MUX13}'
    
    def case_7(self):
        # Enable S7
        return f'{self.resource_name}/{MUX12}, {self.resource_name}/{MUX13}'
    
    def case_8(self):
        # Enable S8
        return f'{self.resource_name}/{MUX11}, {self.resource_name}/{MUX12}, {self.resource_name}/{MUX13}'
    
    def case_9(self):
        # Enable S9
        return f'{self.resource_name}/{MUX14}'
    
    def case_10(self):
        # Enable S10
        return f'{self.resource_name}/{MUX11}, {self.resource_name}/{MUX14}'
    
    def case_11(self):
        # Enable S11
        return f'{self.resource_name}/{MUX12}, {self.resource_name}/{MUX14}'
    
    def case_12(self):
        # Enable S12
        return f'{self.resource_name}/{MUX11}, {self.resource_name}/{MUX12}, {self.resource_name}/{MUX14}'
    
    def case_13(self):  
        # Enable S13
        return f'{self.resource_name}/{MUX13}, {self.resource_name}/{MUX14}'
    
    def case_14(self):
        # Enable S14
        return f'{self.resource_name}/{MUX11}, {self.resource_name}/{MUX13}, {self.resource_name}/{MUX14}'    
    
    def case_15(self):
        # Enable S15
        return f'{self.resource_name}/{MUX12}, {self.resource_name}/{MUX13}, {self.resource_name}/{MUX14}'    
    
    def case_0(self):
        # Enable S16
        return f'{self.resource_name}/{MUX11}, {self.resource_name}/{MUX12}, {self.resource_name}/{MUX13}, {self.resource_name}/{MUX14}'
    
    def switch(self, value):
        # getattr fetches the case_ method by name and calls it to return the channel string
        return getattr(self, f"case_{value}")()
    
    def reset(self):
        return f'{self.resource_name}/{MUX11}, {self.resource_name}/{MUX12}, {self.resource_name}/{MUX13}, {self.resource_name}/{MUX14}'
    

class EnableDmmMux:
    def __init__(self, resource_name) -> None:
        self.resource_name = resource_name

    def enable_mux_u1(self):
        return f'{self.resource_name}/{MUX15}'
    
    def enable_mux_u3(self):
        return f'{self.resource_name}/{MUX16}'
    
    def enable_mux_u2_u4(self):
        return f'{self.resource_name}/{MUX17}'
    
