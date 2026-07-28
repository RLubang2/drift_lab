from PyQt6 import QtWidgets
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from ui_manager.user_interface_variable import (
    SUPPLY_NUMBER,
    DIN_OUT_NUMBER,
)
from visa_manager.visa_address import VisaAddressList as VisaAddressList


class UserInterfaceConfig:

    def __init__(self, window: QtWidgets.QMainWindow) -> None:
        self.window = window
        self._init_supply_widget()
        self._init_temp_widgets()
        self._init_backplane_widgets()
        self._init_measurement_widget()
        self._init_run_test_tab_widgets()
        self._init_main_tab()

        self._populate_supply_addresses()
        self._populate_temp_address()
        self._populate_dmm_address()
        # self._select_temp_mode()
        # self._temp_mode_index()
        


    
    def _init_supply_widget(self) -> None:

        self.supply = {}


        for supply_num in SUPPLY_NUMBER:
            self.supply[supply_num] = {
                'smu_address': self.window.findChild(
                    QtWidgets.QComboBox, f'smu_address_{supply_num}'
                ),
                'smu_brand': self.window.findChild(
                    QtWidgets.QLineEdit, f'smu_brand_{supply_num}'
                ),
                'smu_model': self.window.findChild(
                    QtWidgets.QLineEdit, f'smu_model_{supply_num}'
                ),
                'smu_mode_volt': self.window.findChild(
                    QtWidgets.QRadioButton, f'smu_mode_volt_{supply_num}'
                ),
                'smu_mode_curr': self.window.findChild(
                    QtWidgets.QRadioButton, f'smu_mode_curr_{supply_num}'
                ),
                'smu_channel': self.window.findChild(
                    QtWidgets.QSpinBox, f'smu_channel_{supply_num}'
                ),
                'smu_voltage': self.window.findChild(
                    QtWidgets.QDoubleSpinBox, f'smu_voltage_{supply_num}'
                ),
                'smu_current': self.window.findChild(
                    QtWidgets.QDoubleSpinBox, f'smu_current_{supply_num}'
                ),
                'smu_ping': self.window.findChild(
                    QtWidgets.QPushButton, f'smu_button_ping_{supply_num}'
                ),
                'smu_run': self.window.findChild(
                    QtWidgets.QPushButton, f'smu_button_run_{supply_num}'
                )
            }
    def _init_main_tab(self)-> None:
        self.window.findChild(QtWidgets.QTabWidget, 'tabSMS').setCurrentIndex(0)

    def _populate_supply_addresses(self) -> None:
        for supply_num in SUPPLY_NUMBER:
            VisaAddressList().populate_combobox(self.supply[supply_num]['smu_address'])


    def get_smu_address(self, supply_num: int) -> str:
        """Get the selected VISA address for a given supply number."""
        return self.supply[supply_num]['smu_address'].currentText()


    def get_smu_brand(self, supply_num: int) -> str:
        """Get the brand name for a given supply number."""
        return self.supply[supply_num]['smu_brand'].text()


    def get_smu_model(self, supply_num: int) -> str:
        """Get the model name for a given supply number."""
        return self.supply[supply_num]['smu_model'].text()


    def get_smu_mode(self, supply_num: int) -> str:

        if self.supply[supply_num]['smu_mode_volt'].isChecked():
            return "VOLT"
        elif self.supply[supply_num]['smu_mode_curr'].isChecked():
            return "CURR"
        
        return "VOLT"  # Default to voltage mode if neither is selected


    def get_smu_channel(self, supply_num: int) -> int:
        """Get the selected channel number for a given supply number."""
        return self.supply[supply_num]['smu_channel'].value()


    def get_smu_voltage(self, supply_num: int) -> float:
        """Get the voltage setpoint for a given supply number."""
        try:
            return self.supply[supply_num]['smu_voltage'].value()
        except ValueError:
            return 0.0  # Default to 0.0 if conversion fails


    def get_smu_current(self, supply_num: int) -> float:
        """Get the current setpoint for a given supply number."""
        try:
            return self.supply[supply_num]['smu_current'].value()
        except ValueError:
            return 0.0  # Default to 0.0 if conversion fails
        

    def get_smu_run_button_state(self, supply_num: int) -> bool:
        """Get the state of the run button for a given supply number."""
        return self.supply[supply_num]['smu_run'].isChecked()
    

    def get_smu_ping_button_state(self, supply_num: int) -> bool:
        """Get the state of the ping button for a given supply number."""
        return self.supply[supply_num]['smu_ping'].isChecked()
    

    def set_brand(self, supply_num: int, brand: str) -> None:
        """Set the brand name for a given supply number."""
        self.supply[supply_num]['smu_brand'].setText(brand)

    
    def set_model(self, supply_num: int, model: str) -> None:
        """Set the model name for a given supply number."""
        self.supply[supply_num]['smu_model'].setText(model)

    def set_smu_mode_volt_enabled(self, supply_num: int, enabled: bool)-> None:
        self.supply[supply_num]['smu_mode_volt'].isEnabled(enabled)
    
    def set_smu_mode_curr_enabled(self, supply_num: int, enabled: bool)-> None:
        self.supply[supply_num]['smu_mode_curr'].isEnabled(enabled)

    def set_channel_enabled(self, supply_num: int, enabled: bool) -> None:
        """Enable or disable the channel selection for a given supply number."""
        self.supply[supply_num]['smu_channel'].setEnabled(enabled)

    
    def set_voltage_enabled(self, supply_num: int, enabled: bool) -> None:
        """Enable or disable the voltage setpoint for a given supply number."""
        self.supply[supply_num]['smu_voltage'].setEnabled(enabled)

    
    def set_current_enabled(self, supply_num: int, enabled: bool) -> None:
        """Enable or disable the current setpoint for a given supply number."""
        self.supply[supply_num]['smu_current'].setEnabled(enabled)

    
    def set_voltage_mode_enabled(self, supply_num: int, enabled: bool) -> None:
        """Enable or disable the mode selection for a given supply number."""
        self.supply[supply_num]['smu_mode_volt'].setEnabled(enabled)

    
    def set_current_mode_enabled(self, supply_num: int, enabled: bool) -> None:
        """Enable or disable the mode selection for a given supply number.""" 
        self.supply[supply_num]['smu_mode_curr'].setEnabled(enabled)


    def set_ping_button_state(self, supply_num: int, state: bool) -> None:
        """Set the state of the ping button for a given supply number."""
        self.supply[supply_num]['smu_ping'].setChecked(state)


    def set_run_button_state(self, supply_num: int, state: bool) -> None:
        """Set the state of the run button for a given supply number."""
        self.supply[supply_num]['smu_run'].setChecked(state)

        

    def clear_smu_info(self, supply_num: int) -> None:
        """Clear all information for a given supply number."""
        self.set_brand(supply_num, "")
        self.set_model(supply_num, "")
        self.set_channel_enabled(supply_num, False)
        self.set_voltage_enabled(supply_num, False)
        self.set_current_enabled(supply_num, False)
        self.set_voltage_mode_enabled(supply_num, False)
        self.set_current_mode_enabled(supply_num, False)


    def enable_smu_input(self, supply_num: int, state: bool)-> None:
        self.set_channel_enabled(supply_num, state)
        self.set_voltage_enabled(supply_num, state)
        self.set_current_enabled(supply_num, state)
        self.set_current_mode_enabled(supply_num, state)
        self.set_voltage_mode_enabled(supply_num, state)

    """Temperature Setup"""

    def _init_temp_widgets(self):
        """Temperature Comm Mode"""
        self.temp_comm_mode = self.window.findChild(QtWidgets.QComboBox, 'comm_mode')
        # self.temp_comm_mode.addItems(["GPIB", "SERIAL"])
        self.temp_tab_comm = self.window.findChild(QtWidgets.QTabWidget, 'tabComms')

        self.temp_comm_mode.currentIndexChanged.connect(self.switch_coms)
        self.temp_comm_mode.setCurrentIndex(0)
        self.switch_coms(self.temp_comm_mode.currentIndex())

        

        """"GPIB Widgets"""
        self.temp_address = self.window.findChild(QtWidgets.QComboBox, 'temp_gpib_address')
        self.temp_response = self.window.findChild(QtWidgets.QLineEdit, 'oven_response')
        self.temp_ping_button = self.window.findChild(QtWidgets.QPushButton, 'oven_button_response')
        self.temp_mode = self.window.findChild(QtWidgets.QComboBox, 'oven_mode')
        self.temp_mode.addItems(["Ramp", "Custom"])

        """Temp Tab Widget"""
        self.temp_tab_widget = self.window.findChild(QtWidgets.QTabWidget, 'tab_temp_mode')

        self.temp_mode.currentIndexChanged.connect(self.switch_tab)
        self.temp_mode.setCurrentIndex(0)
        self.switch_tab(self.temp_mode.currentIndex())



        """"RAMP Config"""
        self.temp_start_ramp = self.window.findChild(QtWidgets.QDoubleSpinBox, 'temp_ramp_start')
        self.temp_end_ramp = self.window.findChild(QtWidgets.QDoubleSpinBox, 'temp_ramp_end')
        self.temp_inc_ramp = self.window.findChild(QtWidgets.QDoubleSpinBox, 'temp_ramp_inc')
        self.temp_soak_time = self.window.findChild(QtWidgets.QSpinBox, 'temp_soak_time')
        self.temp_soak_time.setMaximum(9999)


        """"Custom Profile"""
        # self.temp_soak_cust = self.window.findChild(QtWidgets.QDoubleSpinBox, 'temp_cust_soak')

        self.add_row_button = self.window.findChild(QtWidgets.QPushButton, 'add_temp')
        self.rem_row_button = self.window.findChild(QtWidgets.QPushButton, 'remove_temp')
        self.temp_table = self.window.findChild(QtWidgets.QTableView, 'tableTempCustom')
        self.temp_model = QStandardItemModel(0,1)
        self.temp_model.setHorizontalHeaderLabels(["Temperature"])
        self.temp_table.setModel(self.temp_model)
        self.temp_table.horizontalHeader().setStretchLastSection(True) #type: ignore


        """Serial Comm Widget"""
        self.serial_port = self.window.findChild(QtWidgets.QComboBox, 'temp_serial_port')
        self.baudrate = self.window.findChild(QtWidgets.QSpinBox, 'temp_baudrate')
        self.baudrate.setMaximum(999999)
        self.serial_address = self.window.findChild(QtWidgets.QSpinBox, 'temp_serial_address')


        

    def _populate_temp_address(self) -> None:
        VisaAddressList().populate_combobox(self.temp_address)

    
    # def _select_temp_mode(self):
    #     self.select_mode = ["Ramp", "Custom"]
    #     self.temp_mode.addItems(self.select_mode)

    # def _temp_mode_index(self):
    #     self.temp_mode.currentIndexChanged.connect(self.switch_tab)

    def switch_coms(self, index):
        self.temp_tab_comm.setCurrentIndex(index)

        if index == 0:
            self.temp_tab_comm.setTabEnabled(1, False)
            self.temp_tab_comm.setTabEnabled(0, True)

        elif index == 1:
            self.temp_tab_comm.setTabEnabled(1, True)
            self.temp_tab_comm.setTabEnabled(0, False)


    def switch_tab(self, index):
        self.temp_tab_widget.setCurrentIndex(index)

        if index == 0:
            self.temp_tab_widget.setTabEnabled(1, False)
            self.temp_tab_widget.setTabEnabled(0, True)

        elif index == 1:
            self.temp_tab_widget.setTabEnabled(1, True)
            self.temp_tab_widget.setTabEnabled(0, False)

        # self.selected_mode = self.temp_mode.currentText()
        # print(self.selected_mode)

        # if self.selected_mode == "Ramp":
        #     self.temp_tab_widget.setCurrentIndex(0)
        
        # elif self.selected_mode == "Custom":
        #     self.temp_tab_widget.setCurrentIndex(1)



    # def add_table_row(self):
    #     self.new_item = QStandardItem("20")
    #     self.model.appendRow([self.new_item])


    # def remove_table_row(self):
    #     self.selected_row = self.table.selectionModel().selectedIndexes()

    #     if self.selected_row:
    #         self.row_to_remove = self.selected_row[0].row()
    #         self.model.removeRow(self.row_to_remove)

    #     elif self.model.rowCount()>0:
    #         self.model.removeRow(self.model.rowCount() - 1)

    """Back Plane Config"""

    def _init_backplane_widgets(self) -> None:
        self.ni_slot_address = self.window.findChild(QtWidgets.QLineEdit, 'ni_pxie_slot')
        self.ni_response = self.window.findChild(QtWidgets.QLineEdit, 'ni_inst_response')
        self.ni_button_ping = self.window.findChild(QtWidgets.QPushButton, 'ni_button_ping')

        self.ni_voltage_lvl = self.window.findChild(QtWidgets.QDoubleSpinBox, 'nidigital_voltage')
        self.ni_current_lvl = self.window.findChild(QtWidgets.QDoubleSpinBox, 'nidigital_current')

        self.din_output = {}
        for output_number in DIN_OUT_NUMBER:
            self.din_output[output_number] = {
                'outx': self.window.findChild(
                    QtWidgets.QCheckBox, f'din_out_{output_number}'
                ),
            
            }


    def _init_measurement_widget(self) -> None:
        self.meas_address = self.window.findChild(QtWidgets.QComboBox, 'meas_address')
        self.meas_response = self.window.findChild(QtWidgets.QLineEdit, 'meas_response')
        self.meas_ping_button = self.window.findChild(QtWidgets.QPushButton, 'meas_ping_button')
        self.meas_mode = self.window.findChild(QtWidgets.QComboBox, 'meas_mode')
        self.meas_mode.addItems(["Voltage", "Current"])
        self.meas_range = self.window.findChild(QtWidgets.QComboBox, 'meas_range')
        self.meas_sample = self.window.findChild(QtWidgets.QSpinBox, 'meas_sample')
        self.meas_sample.setMinimum(1)
        self.meas_count = self.window.findChild(QtWidgets.QSpinBox, 'meas_count')
        self.meas_count.setMinimum(1)
        self.meas_mode.currentIndexChanged.connect(self.switch_range)
        self.meas_mode.setCurrentIndex(0)
        self.switch_range(self.meas_mode.currentIndex())


        self.measure_tableview = self.window.findChild(QtWidgets.QTableView, 'measure_output_table')
        # self.measure_model = QStandardItemModel()
        # self.measure_header = ['Temperature']
    
    def _populate_dmm_address(self) -> None:
        VisaAddressList().populate_combobox(self.meas_address)

    def switch_range(self, index):
        if index == 0:
            self.meas_range.clear()
            self.meas_range.addItems(["100 mV", "1 V", "10 V", "100 V", "1000 V"])
        elif index == 1:
            self.meas_range.clear()
            self.meas_range.addItems(["100 nA", "1 uA", "10 uA", "100 uA", "1 mA", "10 mA", "100 mA", "1 A"])



    """"Initialize Run Test Widgets """

    def _init_run_test_tab_widgets(self) -> None:
        self.file_name = self.window.findChild(QtWidgets.QLineEdit, 'file_name')
        self.save_file_button = self.window.findChild(QtWidgets.QPushButton, 'save_file_button')

        self.temp_set = self.window.findChild(QtWidgets.QComboBox, 'temp_set')
        self.temp_test_mode = self.window.findChild(QtWidgets.QComboBox, 'temp_test_mode')

        self.test_run_button = self.window.findChild(QtWidgets.QPushButton, 'test_run_button')
        self.test_abort_button = self.window.findChild(QtWidgets.QPushButton, 'test_abort_button')

        self.temp_test_mode.currentIndexChanged.connect(self.enable_temp_set)
        self.enable_temp_set(self.temp_test_mode.currentIndex())

    def enable_temp_set(self, index):
        if index == 0:
            self.temp_set.setEnabled(False)
        else:
            self.temp_set.setEnabled(True)