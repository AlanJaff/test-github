from pytest_bdd import scenario, given, when, then
# -*- coding: utf-8 -*-
from unittest import TestCase, skip
from device import init_device_for_test, unplug, start_program
from pprint import pprint
# import plant_model
from Skytest import categories, id, trace
from Skylab.Signal import AnalogLine, DiscreteLine, DigitalLine
from Skylab.Statement import W32COMUSBDEV, TestExecutor
import Report
from SkyImage.io import imtoreport
from chilly import wait_for
from helpers.data_recorder import ProcessDataRecorder
import time
from DataAnalysis import read_tdms
from miele_process_analyzer.plot import create_nvd3_plot
from DataAnalysis.Plot import DyPlot
from proj_config import st, bt, doper, sleep_time, optical_interface, msg, connecting_time, Report_heading

# @given("Hil has started")
# def step_impl():
#     init_device_for_test(optical_interface, connecting_time, sleep_time)
#     dopx_read_name = self._testMethodName + "_-_" + self.__module__
#     print(dopx_read_name)
#     self.rec = ProcessDataRecorder(self._testMethodName, "helpers.test_record.DopXRead")
#     self.rec.start()
#
# @when("we select the program WT_Wolle_Single")
# def step_impl():
#
#     """    Wolle waschen mit Anwahl Single    """
#     # pprint(AnalogLine.GLOBAL_PS_Context__ContextParaWM.get_value())
#     msg["ProgId"] = 8
#     msg["SelectionParaWM"]["Extras"]["Single"] = True
#     doper.write_part(st.GLOBAL_PS_Select, msg)
#     time.sleep(sleep_time / 2)
#
#     """    Infomationen aus den DopX Elementen auslesen    """
#     global_ps_context = doper.get(st.GLOBAL_PS_Context)
#     print('\n')
#     print("ProgId = %d " % global_ps_context["ProgAttributesDWTDWM"]["ProgId"])
#     print("MaxProgrammDuration = %d " % global_ps_context["ProgAttributesDWTDWM"]["MaxProgrammDuration"])
#     global_ds_devicestate = doper.get(st.GLOBAL_DS_DeviceState)
#     print("Remaining Time: %d min " % ((global_ds_devicestate["RemainingTime"]) / 60))
#     print("Spinning Speed: %d rpm " % global_ds_devicestate["SpinningSpeed"])
#
#     """    Reporting zusammenstellen    """
#     Report.add_heading(1, "Begin/Start von Test " + str(self._testMethodName))
#     tR = Report_heading()
#     tR.Kategorie(str(self._testMethodName))
#     tR.SimZeitpunkt("Starte die Test-Umgebung und wähle 'Wolle' an")
#     tR.Beeinflussung("Starte den Programmablauf für x-Zeit")
#     tR.Beeinflussung("Aufnahme des Testest in deine TDMS Datei")
#     tR.Besonderheiten("zur Zeit keine")
#     Report.add_table(tR.get_table(), True)
#     Report.add_paragraph("ENDE des Tests " + str(self._testMethodName))
#
#     """    Angewähltes Programm starten    """
#     print("Starten")
#     start_program()
#     time.sleep(20)
#     # global_ds_devicestate = doper.get(st.GLOBAL_DS_DeviceState)
#     # print("Remaining Time: %d min " % ((global_ds_devicestate["RemainingTime"]) / 60))
#     # print("Spinning Speed: %d rpm " % global_ds_devicestate["SpinningSpeed"])
#
# @then("we check the remaining time")
# def step_impl():
#     assert (global_ds_devicestate["RemainingTime"]) / 60 == 7
#     # self.assertTrue((global_ds_devicestate["RemainingTime"]) / 60 == 29)
