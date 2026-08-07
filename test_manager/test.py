from __future__ import annotations

import time
from typing import TYPE_CHECKING, Optional

from PyQt6.QtCore import QThread, pyqtSignal, QObject
from PyQt6.QtWidgets import QMessageBox, QApplication

if TYPE_CHECKING:
    from ui_manager.user_interface_config import UserInterfaceConfig
    from cons_window.console import ConsoleWindow

from measurement_manager.run_dmm import RunDMM
from measurement_manager.tableview import TableViewV2
from ni_pxie_6570.ni_digital import PXIE6570
from backplane.check_enabled_output import CheckEnableOutput
from backplane.mux_control import SwitchBackplaneToDmm, SwitchBoardToBackplane, EnableDmmMux
from file_manager.file_path import FilePath
from file_manager.save import SaveManager
from temperature_manager.temp_run import RunTemp
from ui_manager.user_interface_variable import (
    DIN_OUT1, DIN_OUT2, DIN_OUT3, DIN_OUT4, DIN_OUT5, DIN_OUT6,
)




class TestWorker(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result_ready = pyqtSignal(dict)
    log_message = pyqtSignal(str)

    def __init__(self, run_test: RunTest, test_mode: int, temp_set_mode: int) -> None:
        super().__init__()
        self._run_test = run_test
        self._test_mode = test_mode
        self._temp_set_mode = temp_set_mode
        self._abort_requested = False

    def request_abort(self) -> None:
        self._abort_requested = True

    @property
    def is_aborted(self) -> bool:
        return self._abort_requested

    def run(self) -> None:
        try:
            if self._test_mode == 0:
                self._run_ambient()
            elif self._test_mode == 1:
                if self._temp_set_mode == 0:
                    self._run_sweep()
                else:
                    self._run_custom()
            else:
                self._run_ambient()
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()

    def _validate_instrument_resources(self) -> bool:
        rt = self._run_test

        if rt.ui_config.meas_address.currentIndex() < 1:
            self.error.emit("No DMM resource connected. Please configure DMM address.")
            return False

        if not rt.ui_config.ni_slot_address.text().strip():
            self.error.emit("No NI PXIe-6570 resource connected. Please configure NI Digital slot address.")
            return False

        return True

    def _validate_temp_chamber(self) -> bool:
        rt = self._run_test
        if rt.ui_config.temp_tab_comm.currentIndex() == 0:
            if rt.ui_config.temp_address.currentIndex() < 1:
                self.error.emit("No temperature chamber connected. Please configure oven GPIB address.")
                return False
        else:
            if rt.ui_config.serial_port.currentIndex() < 1:
                self.error.emit("No temperature chamber connected. Please configure serial port.")
                return False
        return True

    def _run_ambient(self) -> None:
        if not self._validate_instrument_resources():
            return
        
        row_data = {}

        self.log_message.emit("Starting ambient test...")
        rt = self._run_test

        filepath = rt.ui_config.file_name.text().strip()
        actual_path = rt.save_manager.open_file(filepath)
        rt.ui_config.file_name.setText(actual_path)
        try:
            dut_output = self._read_output()

            if self._abort_requested:
                rt.save_manager.save_result("AMB", dut_output)
                return

            if dut_output:
                rt.save_manager.save_result("AMB", dut_output)
                for site, readings in dut_output.items():
                    row_data.setdefault(site, [])
                    row_data[site].append(
                        {
                            "temp": "AMB",
                            "readings": readings
                        }
                    )
            if row_data:
                self.result_ready.emit(row_data)

        except Exception as e:
            self.error.emit(f"Error during ambient test: {e}")
            rt.save_manager.close_file()

        finally:
            rt.save_manager.close_file()

    def _generate_set_points(self, start, end, step):
        if step == 0:
            raise ValueError("Step value cannot be zero.")

        set_points = []

        if start < end:
            temp = start
            while temp + step < end:
                temp += step
                set_points.append(temp)
        elif start > end:
            temp = start
            while temp - step > end:
                temp -= step
                set_points.append(temp)

        if set_points[-1] != end:
            set_points.append(end)

        return set_points

    def _run_sweep(self) -> None:
        if not self._validate_instrument_resources():
            return
        if not self._validate_temp_chamber():
            return
        self.log_message.emit("Starting Sweep Temperature Test...")
        rt = self._run_test

        filepath = rt.ui_config.file_name.text().strip()
        actual_path = rt.save_manager.open_file(filepath)
        rt.ui_config.file_name.setText(actual_path)

        temp_start = int(rt.ui_config.temp_start_ramp.value())
        temp_end = int(rt.ui_config.temp_end_ramp.value())
        temp_inc = int(rt.ui_config.temp_inc_ramp.value())

        row_data: dict = {}

        set_points = self._generate_set_points(temp_start, temp_end, temp_inc)

        try:
            rt.temp_chamber.connect_dev()
        except Exception as e:
            self.error.emit(f"Failed to connect to temperature chamber: {e}")
            rt.save_manager.close_file()
            rt.temp_chamber.temp_close()
            return

        try:
            for temp in set_points:
                if self._abort_requested:
                    return
                
                temp_val = temp
                self.log_message.emit(f"Testing in temperature: {temp_val}")
                rt.temp_chamber.temp_write(temp_val)
                self.log_message.emit(f"Soaking at temperature: {temp_val}")
                rt.temp_chamber.temp_soak(temp_val, abort_check=self.is_aborted)
                self.log_message.emit(f"Done soaking at temperature: {temp_val}")

                dut_output = self._read_output()

                if self._abort_requested:
                    rt.save_manager.save_result(temp_val, dut_output)
                    return

                if dut_output:
                    rt.save_manager.save_result(temp_val, dut_output)
                # row_data[temp_val] = dut_output

                for site, readings in dut_output.items():
                    row_data.setdefault(site, [])
                    row_data[site].append(
                        {
                            "temp": temp_val,
                            "readings": readings
                        }
                    )

            if row_data:
                self.result_ready.emit(row_data)

        except Exception as e:
            self.error.emit(f"Error during sweep temperature test: {e}")
            rt.temp_chamber.temp_close()
            rt.save_manager.close_file()

        finally:
            if temp_end < 0:
                rt.temp_chamber.temp_write(100)
                time.sleep(300)
                rt.temp_chamber.temp_write(25)
            else:
                rt.temp_chamber.temp_write(25)

            rt.save_manager.close_file()
            rt.temp_chamber.temp_close()

    # def _run_sweep(self) -> None:
    #     if not self._validate_instrument_resources():
    #         return
    #     if not self._validate_temp_chamber():
    #         return
    #     self.log_message.emit("Starting Sweep Temperature Test...")
    #     rt = self._run_test

    #     filepath = rt.ui_config.file_name.text().strip()
    #     actual_path = rt.save_manager.open_file(filepath)
    #     rt.ui_config.file_name.setText(actual_path)

    #     temp_start = int(rt.ui_config.temp_start_ramp.value() * 10)
    #     temp_end = int(rt.ui_config.temp_end_ramp.value() * 10)
    #     temp_inc = int(rt.ui_config.temp_inc_ramp.value() * 10)

    #     try:
    #         rt.temp_chamber.connect_dev()
    #     except Exception as e:
    #         self.error.emit(f"Failed to connect to temperature chamber: {e}")
    #         rt.save_manager.close_file()
    #         rt.temp_chamber.temp_close()
    #         return

    #     row_data: dict = {}

    #     step = -abs(temp_inc) if temp_start > temp_end else abs(temp_inc)

    #     try:
    #         for temp in range(temp_start, temp_end, step):
    #             if self._abort_requested:
    #                 return
    #             temp_val = temp / 10
    #             self.log_message.emit(f"Testing in temperature: {temp_val}")
    #             rt.temp_chamber.temp_write(temp_val)
    #             self.log_message.emit(f"Soaking at temperature: {temp_val}")
    #             rt.temp_chamber.temp_soak(temp_val)
    #             self.log_message.emit(f"Done soaking at temperature: {temp_val}")

    #             dut_output = self._read_output()

    #             if self._abort_requested:
    #                 rt.save_manager.save_result(temp_val, dut_output)
    #                 return

    #             if dut_output:
    #                 rt.save_manager.save_result(temp_val, dut_output)
    #             # row_data[temp_val] = dut_output

    #             for site, readings in dut_output.items():
    #                 row_data.setdefault(site, [])
    #                 row_data[site].append(
    #                     {
    #                         "temp": temp_val,
    #                         "readings": readings
    #                     }
    #                 )

    #         if row_data:
    #             self.result_ready.emit(row_data)

    #     except Exception as e:
    #         self.error.emit(f"Error during sweep temperature test: {e}")
    #         rt.temp_chamber.temp_close()
    #         rt.save_manager.close_file()

    #     finally:
    #         if temp_end < 0:
    #             rt.temp_chamber.temp_write(100)
    #             time.sleep(300)
    #             rt.temp_chamber.temp_write(25)
    #         else:
    #             rt.temp_chamber.temp_write(25)

    #         rt.save_manager.close_file()
    #         rt.temp_chamber.temp_close()

    def _run_custom(self) -> None:
        if not self._validate_instrument_resources():
            return
        if not self._validate_temp_chamber():
            return

        rt = self._run_test
        row_count = rt.ui_config.temp_model.rowCount()

        if row_count < 1:
            self.error.emit("Please set temperature point")
            return

        filepath = rt.ui_config.file_name.text().strip()
        actual_path = rt.save_manager.open_file(filepath)
        rt.ui_config.file_name.setText(actual_path)

        try:
            self.log_message.emit("Connecting to temperature chamber...")
            rt.temp_chamber.connect_dev()
        except Exception as e:
            self.error.emit(f"Failed to connect to temperature chamber: {e}")
            rt.temp_chamber.temp_close()
            rt.save_manager.close_file()
            return

        row_data: dict = {}
        test_point = 1
        try:
            for row in range(row_count):
                self.log_message.emit(f"Currently at Set Point No.: {test_point}")
                test_point += 1

                if self._abort_requested:
                    return
                temp_value = int(rt.ui_config.temp_model.index(row, 0).data())
                self.log_message.emit(f"Testing in temperature: {temp_value}")
                rt.temp_chamber.temp_write(temp_value)
                self.log_message.emit(f"Soaking at temperature: {temp_value}")
                rt.temp_chamber.temp_soak(temp_value, abort_check=self.is_aborted)

                self.log_message.emit(f"Done soaking at temperature: {temp_value}")

                dut_output = self._read_output()

                if self._abort_requested:
                    rt.save_manager.save_result(temp_value, dut_output)
                    return

                if dut_output:
                    rt.save_manager.save_result(temp_value, dut_output)
                # row_data[temp_value] = dut_output
                for site, readings in dut_output.items():
                    row_data.setdefault(site, [])
                    row_data[site].append(
                        {
                            "temp": temp_value,
                            "readings": readings
                        }
                    )

            if row_data:
                # print(row_data)
                self.result_ready.emit(row_data)

        except Exception as e:
            self.error.emit(f"Error during custom temperature test: {e}")
            rt.temp_chamber.temp_close()
            rt.save_manager.close_file()
        finally:
            last_temp = int(rt.ui_config.temp_model.index(row_count - 1, 0).data())

            if last_temp < 15:
                rt.temp_chamber.temp_write(100)
                QMessageBox.warning(None, 
                                     "Test Complete", 
                                     "Warming up to remove moisture. Please wait for 5 minutes before starting the next test."
                                     )
                
                while True:
                    temp_env = rt.temp_chamber.temp_read()
                    time.sleep(5)
                    if temp_env is None:
                        break
                    if temp_env > 85:
                        break

                time.sleep(180)
                rt.temp_chamber.temp_write(25)
            else:
                rt.temp_chamber.temp_write(25)

            rt.temp_chamber.temp_close()
            rt.save_manager.close_file()

    def _run_custom1(self) -> None:

        row_count = [10, 20, 30]
        row_data: dict = {}

        try:
            for row in range(len(row_count)):

                temp_value = row_count[row]


                dut_output = {1: [1.0, 2.0, 3.0], 
                              2: [4.0, 5.0, 6.0], 
                              3: [7.0, 8.0, 9.0], 
                              4: [10.0, 11.0, 12.0], 
                              6: [13.0, 14.0, 15.0]} 

                for site, readings in dut_output.items():
                    # print(site)
                    # print(readings)
                    row_data.setdefault(site, [])
                    row_data[site].append(
                        {
                            "temp": temp_value,
                            "readings": readings
                        }
                    )
                    # row_data[site].setdefault(temp_value, [])
                    # row_data[site][temp_value].append(readings)


            if row_data:
                print(row_data)

                # for site in row_data:
                #     for temp in site.values():
                #         print(temp.values())
                self.result_ready.emit(row_data)

        except Exception as e:
            self.error.emit(f"Error during custom temperature test: {e}")
        #     rt.temp_chamber.temp_close()
        #     rt.save_manager.close_file()
        # finally:
        #     rt.temp_chamber.temp_write(25)
        #     rt.temp_chamber.temp_close()
        #     rt.save_manager.close_file()

    def _read_output(self) -> dict:
        rt = self._run_test
        ni_voltage_level = rt.ui_config.ni_voltage_lvl.value()
        ni_current_level = rt.ui_config.ni_current_lvl.value()
        ni_resource = rt.ui_config.ni_slot_address.text()
        meas_count = rt.ui_config.meas_count.value()

        self.log_message.emit(
            f"NI Resource: {ni_resource}, V: {ni_voltage_level}, I: {ni_current_level}"
        )

        result: dict = {}
        output_num = 1

        rt.ni.reset_nidigital(ni_resource)
        time.sleep(0.1)
        rt.dmm.init_device()
        self.log_message.emit("DMM initialized successfully.")
        time.sleep(1)

        if not rt.backplane_config.check_enabled_checkbox():
            return result

        self.log_message.emit("Enabling MUX1")
        rt.ni.force_voltage(
            ni_resource,
            rt.enable_mux_dmm.enable_mux_u1(),
            ni_voltage_level,
            ni_current_level,
        )
        time.sleep(1)

        output_groups = [
            (rt.backplane_config.check_out_1_16, rt.switch_backplane_to_dmm.case_1, DIN_OUT1, 0.0),
            (rt.backplane_config.check_out_17_32, rt.switch_backplane_to_dmm.case_2, DIN_OUT2, ni_voltage_level),
            (rt.backplane_config.check_out_33_48, rt.switch_backplane_to_dmm.case_3, DIN_OUT3, ni_voltage_level),
            (rt.backplane_config.check_out_49_64, rt.switch_backplane_to_dmm.case_4, DIN_OUT4, ni_voltage_level),
            (rt.backplane_config.check_out_65_80, rt.switch_backplane_to_dmm.case_5, DIN_OUT5, ni_voltage_level),
            (rt.backplane_config.check_out_81_96, rt.switch_backplane_to_dmm.case_6, DIN_OUT6, ni_voltage_level),
        ]

        for check_fn, get_channel_fn, din_outputs, ni_voltage in output_groups:
            if self._abort_requested:
                break
            if not check_fn():
                continue

            backplane_channel = get_channel_fn()
            self.log_message.emit(f"Backplane Channel: {backplane_channel}")

            rt.ni.force_voltage(
                ni_resource, backplane_channel, ni_voltage, ni_current_level
            )
            time.sleep(5)

            try:
                for x in din_outputs:
                    if self._abort_requested:
                        break
                    if not rt.ui_config.din_output[x]["outx"].isChecked():
                        continue

                    self.log_message.emit(f"Measuring output at DIN no.: {x}")

                    dut_to_din = x % 16
                    channel = rt.switch_board_to_backplane.switch(dut_to_din)
                    for_voltage = 0.0 if dut_to_din == 1 else ni_voltage_level

                    self.log_message.emit(f"Measuring DIN_OUT{x}")

                    # if x == 5:
                    #     rt.ni.force_voltage(
                    #         ni_resource,
                    #         rt.switch_board_to_backplane.switch(1),
                    #         0.0,
                    #         ni_current_level
                    #         )

                    #     time.sleep(2)
                    # for _ in range(2):
                    rt.ni.force_voltage(
                        ni_resource, channel, for_voltage, ni_current_level
                    )
                    # if x == 5:
                    #     # self.log_message.emit("Measuring DIN5, Add delay 10 s")
                    #     time.sleep(2)
                    # else:
                    #     time.sleep(2)

                    time.sleep(2)

                    try:
                        output_data = []
                        for _ in range(meas_count):
                            if self._abort_requested:
                                break
                            time.sleep(0.1)
                            reading = rt.dmm.read_output()
                            time.sleep(0.1)
                            value = float(reading) if reading else None
                            output_data.append(value)
                    finally:
                        # rt.ni.disconnect_channel(ni_resource, channel)
                        rst_channel = rt.switch_board_to_backplane.switch(0)
                        rt.ni.force_voltage(
                            ni_resource,
                            rst_channel,
                            0.0,
                            ni_current_level
                        )
                        
                        time.sleep(1)
                    site_num = x
                    result[output_num] = output_data
                    output_num += 1
            finally:
                # rt.ni.disconnect_channel(ni_resource, backplane_channel)
                # rt.ni.reset_nidigital(ni_resource)
                # rt.dmm.dev_clear()
                rst_mux_dmm_channel = rt.switch_backplane_to_dmm.switch(0)
                rt.ni.force_voltage(
                    ni_resource,
                    rst_mux_dmm_channel,
                    0.0,
                    ni_current_level
                )
                time.sleep(1)

        return result


class RunTest:
    def __init__(self, ui_config: UserInterfaceConfig, console: ConsoleWindow) -> None:
        self.ui_config = ui_config
        self.console_window = console
        self.ni_resource: Optional[str] = None

        self.file_path = FilePath(self.ui_config)
        self.save_manager = SaveManager()

        self.switch_backplane_to_dmm = SwitchBackplaneToDmm()
        self.switch_board_to_backplane = SwitchBoardToBackplane()
        self.enable_mux_dmm = EnableDmmMux()
        self.ni = PXIE6570()

        self.dmm = RunDMM(self.ui_config)
        self.table_v2 = TableViewV2(self.ui_config)
        self.backplane_config = CheckEnableOutput(self.ui_config)
        self.temp_chamber = RunTemp(self.ui_config)

        self._worker: Optional[TestWorker] = None
        self._thread: Optional[QThread] = None

        self._connect_buttons()

    def _connect_buttons(self) -> None:
        self.ui_config.test_run_button.pressed.connect(self._start_test)
        self.ui_config.test_abort_button.pressed.connect(self._abort_test)

    def _start_test(self) -> None:
        if self._thread is not None and self._thread.isRunning():
            QMessageBox.warning(None, "Test Running", "A test is already in progress.")
            return

        test_mode = self.ui_config.temp_test_mode.currentIndex()
        temp_set_mode = self.ui_config.temp_set.currentIndex()

        self.console_window.log("Run Test initialized")
        self.console_window.log(f"Test Mode: {test_mode}, Set Mode: {temp_set_mode}")

        self._thread = QThread()
        self._worker = TestWorker(self, test_mode, temp_set_mode)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_test_finished)
        self._worker.error.connect(self._on_test_error)
        self._worker.result_ready.connect(self._on_result_ready)
        self._worker.log_message.connect(self.console_window.log)
        self.ui_config.test_run_button.setEnabled(False)
        self._thread.start()

    def _abort_test(self) -> None:
        self.console_window.log("Abort requested - resetting all equipment...")
        if self._worker is not None:
            self._worker.request_abort()
        self.reset_all_equipment()

        if self._thread is not None:
            self._thread.quit()
            self._thread.wait()

        self._thread = None
        self._worker = None

        self.ui_config.test_run_button.setEnabled(True)
        QMessageBox.critical(None, 
                             "Test Aborted", 
                             "The test has been aborted. All equipment has been reset."
                             )

    def _on_test_finished(self) -> None:
        self.ui_config.test_run_button.setEnabled(True)
        if self._thread is not None:
            self._thread.quit()
            self._thread.wait()
        self._thread = None
        self._worker = None
        self.console_window.log("Test finished.")
        # QMessageBox.information(None, "Test Result", "The test has finished.")

    def _on_test_error(self, message: str) -> None:
        self.console_window.log(f"ERROR: {message}")
        QMessageBox.critical(None, "Test Error", message)

    def _on_result_ready(self, results: dict) -> None:
        self.table_v2.update_results(results)
        if self.ui_config.temp_test_mode.currentIndex() == 0:
            QMessageBox.information(
                None, "Ambient Test", "Ambient test completed successfully."
            )
        else:
            QMessageBox.information(
                None, "Temperature Test", "Temperature test completed successfully."
            )

    def reset_all_equipment(self) -> None:
        ni_resource = self.ui_config.ni_slot_address.text().strip()
        if ni_resource:
            try:
                self.ni.reset_nidigital(ni_resource)
                self.console_window.log("NI Digital reset.")
            except Exception as e:
                self.console_window.log(f"Failed to reset NI Digital: {e}")

        if self.ui_config.meas_address.currentIndex() > 0:
            try:
                self.dmm.dev_reset()
                self.dmm.dev_close()
                self.console_window.log("DMM reset and closed.")
            except Exception as e:
                self.console_window.log(f"Failed to reset DMM: {e}")

        has_temp = False
        if self.ui_config.temp_tab_comm.currentIndex() == 0:
            has_temp = self.ui_config.temp_address.currentIndex() > 0
        else:
            has_temp = self.ui_config.serial_port.currentIndex() > 0

        if has_temp:
            try:
                self.temp_chamber.temp_write(25.0)
                time.sleep(1)
                self.temp_chamber.temp_close()
                self.console_window.log("Temperature chamber set to 25°C.")
            except Exception as e:
                self.console_window.log(f"Failed to reset temperature chamber: {e}")

        self.console_window.log("All equipment reset.")
