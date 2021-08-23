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
from proj_config import  st, bt, doper, sleep_time, optical_interface, msg, connecting_time, Report_heading


class Heating(TestCase):

    def setUp(self):
        init_device_for_test(optical_interface)
        signals = [DiscreteLine.myBlpmModelDruckwert.name,
                   AnalogLine.LDR2HeatingPlotValue.name,
                   DigitalLine.myBlpmModelHeatingLIsActive.name,
                   DigitalLine.myBlpmModelHeatingNIsActive.name]
        self.rec = ProcessDataRecorder(self._testMethodName, signals)
        self.rec.start()

    @categories("WT1f")
    def test_WT_WaschenHeizen(self):
        """
        -System hochfahren
            WT Modus 3 anwaelen
            WT Prog. 8 fuer Wolle auswaehlen
                Singel anwaelen
        :param :
        :return: -
        """
        # if not W32COMUSBDEV.IsConnected(optical_interface):
        #     W32COMUSBDEV.Connect(optical_interface)
        time.sleep(sleep_time)
        # monitor = build_optic_monitor_sky(optical_interface)
        # doper = build_optic_doper(rx_id=14, rx_unit=254, optic_monitor=monitor)
        msg["ProgId"] = 146
        # msg["SelectionParaWM"]["ProgramMode"] = 3
        doper.write_part(st.GLOBAL_PS_Select, msg)
        time.sleep(sleep_time)
        global_ds_devicestate = doper.get(st.GLOBAL_DS_DeviceState)
        time.sleep(3)
        global_ps_context = doper.get(st.GLOBAL_PS_Context)
        print('\n')
        DigitalLine.TASTE_START_STOP.set_value(True)
        time.sleep(0.25)
        DigitalLine.TASTE_START_STOP.set_value(False)
        time.sleep((global_ds_devicestate["RemainingTime"]) + 2 * 15)
        print("DryingTime = %s" % str(global_ps_context["ContextParaWM"]["DryingTime"]))
        print("ProgId = %d " % global_ps_context["ProgAttributesDWTDWM"]["ProgId"])
        print("MinVisible = %d " % global_ps_context["ContextParaWM"]["DryingTime"]["MinVisible"])
        print("MaxProgrammDuration = %d " % global_ps_context["ProgAttributesDWTDWM"]["MaxProgrammDuration"])
        print("Remaining Time: %d min " % (global_ds_devicestate["RemainingTime"]) / 60)
        print("Spinning Speed: %d rpm " % global_ds_devicestate["SpinningSpeed"])
        assert global_ps_context["ContextParaWM"]["DryingTime"]["MinVisible"] == 15
        W32COMUSBDEV.Disconnect(optical_interface)

    def tearDown(self):
        self.rec.stop()
        unplug(optical_interface)


class Waschen(TestCase):
    """    Waschen: Programme und Zeit ausgeben und aufnehmen    """

    def setUp(self):
        init_device_for_test(optical_interface, connecting_time, sleep_time)
        dopx_read_name = self._testMethodName + "_-_" + self.__module__
        print(dopx_read_name)
        self.rec = ProcessDataRecorder(self._testMethodName, "helpers.test_record.DopXRead")
        self.rec.start()
    # @id(12424)
    # @trace("")
    @categories("WT1f")
    def test_WT_Wolle_Single(self):
        global actuator, Sensor_StartValue, Sensor_IstValue
        """        Wolle waschen mit Anwahl Single        """
        # pprint(AnalogLine.GLOBAL_PS_Context__ContextParaWM.get_value())
        msg["ProgId"] = 8  # Wolle
        msg["SelectionParaWM"]["Extras"]["Single"] = True  # Enable the settings of the program variables
        doper.write_part(st.GLOBAL_PS_Select, msg)  # Display selected program on SBAE (System Bedienanzeige-Einheit)
        time.sleep(sleep_time / 2)  # Pause 3 sek

        """        Infomationen aus den DopX Elementen auslesen        """
        print()  # print a blank line
        global_ps_context = doper.get(st.GLOBAL_PS_Context)
        print("ProgId = %d " % global_ps_context["ProgAttributesDWTDWM"]["ProgId"])

        #  Variables from GLOBAL_DS_DeviceState --------------------------------------------
        global_ds_devicestate = doper.get(st.GLOBAL_DS_DeviceState)
        print("Remaining Time: %d min " % ((global_ds_devicestate["RemainingTime"]) / 60))
        print("Spinning Speed: %d rpm " % global_ds_devicestate["SpinningSpeed"])
        print()  # print a blank line

        """        Reporting zusammenstellen        """
        Report.add_heading(1, "Begin/Start von Test " + str(self._testMethodName))
        tR = Report_heading()
        tR.Kategorie(str(self._testMethodName))
        tR.SimZeitpunkt("Starte die Test-Umgebung und wähle 'Wolle' an")
        tR.Beeinflussung("Starte den Programmablauf für x-Zeit")
        tR.Beeinflussung("Aufnahme des Testest in deine TDMS Datei")
        tR.Besonderheiten("zur Zeit keine")
        Report.add_table(tR.get_table(), True)
        Report.add_paragraph("ENDE des Tests " + str(self._testMethodName))
        print("Reporting for the Test Case is developed")
        print()  # print a blank line
        # Water Level -------------------------------------------------------
        # WaterLevel = global_cs_devicecontext["ServiceAttributesWM"]\
        #                                     ["WaterLevel"]\
        #                                     ["CurrentValue"]
        # print("Ist_WaterLevel = %d mmWS" % (WaterLevel / 10))  # convert to mmWS
        # print()  # print an blank line

        """    Simulation des angewählten Programms per E-Finger starten    """
        print("Start the Program by triggering the electronic Finger")
        print()  # print a blank line
        time.sleep(sleep_time)
        start_program()  # start the simulation by pressing the electronic finger

        # **************************************************************************************
        # Actuator checking phase **************************************************************
        # **************************************************************************************

        # Waif for required actuator to be activated -----------------------------------------------------
        # Actuator = wait_for(get_actuator, value=True, max_timeout_s=300)  # "Kein actuator wurde innerhalb von 5 min aktiviert"
        # print("Heat Actuator Status (Engage ON/OFF) = ", Actuator)  # print the engage statue of the actuator
        # Engage = False
        # while not Engage:
        #     # cdv_actuatorData = doper.get(st.CDV_ActuatorDat)  # get the required variable form DopX interface
        #     # Actuator = cdv_actuatorData["Heater1"]\
        #     #                            ["CurrentValue"]  # read out "Heating Actuator" value from DopX interface
        #     value = get_actuator(actuator_name)
        #     Actuator = value
        #     print(f"Heat Actuator Status (Engage ON/OFF) = {bool(Actuator)}")  # convert to boolean value
        #     print()  # print an blank line
        # if Actuator:  # if Actuator == True
        #     # Saving Sensor_StartValue ---------------------------------------------------
        #     global_cs_devicecontext = doper.get(st.GLOBAL_CS_DeviceContext)  # get the required variable form DopX interface
        #     Sensor_StartValue = global_cs_devicecontext["ServiceAttributesWM"]\
        #                                                ["NtcTemperature"]\
        #                                                ["CurrentValue"]  # read out and save "StartTemp." value
        #     print("Sensor_StartValue =  %d°C" % Sensor_StartValue)
        #     print()  # print a blank line

        # Create a Time-Counter by elapsed seconds -----------------------------------------------------
        TimeCounter = 960  # set timer loop for 16 min (300 sec for 5 min)
        print("Time counter has started:")
        for seconds in range(1, TimeCounter + 1):  # run time counter
            print()  # print a blank line
            print(seconds, "seconds elapsed")  # print the current elapsed seconds

            # Saving Sensor_IstValue ---------------------------------------------------
            global_cs_devicecontext = doper.get(st.GLOBAL_CS_DeviceContext)  # get the required variable form DopX interface
            Sensor_IstValue = global_cs_devicecontext["ServiceAttributesWM"]\
                                                     ["NtcTemperature"]\
                                                     ["CurrentValue"]  # read out "IstTemp." value from DopX
            print("Sensor_IstValue = %d°C" % Sensor_IstValue)  # print "IstTemp." variable

            if seconds >= 180:  # check if elapsed seconds equals to 180 sec
                print(seconds)  # print the actual seconds status
                if Sensor_IstValue - Sensor_StartValue >= 3:  # check if temperature increase of 3°C is achieved

                    print("Sensor_StartValue at 0 sec = %d°C" % Sensor_StartValue)
                    print("Sensor_IstValue after Heat Element activation = " + Sensor_IstValue + "°C")
                    self.assertTrue((global_cs_devicecontext["ServiceAttributesWM"]
                                                            ["NtcTemperature"]
                                                            ["CurrentValue"]) == 20)
                    print(seconds, "seconds elapsed")  # print the current elapsed seconds
                    print("Temperature Increase of 3°C is reached")  # print reached Temperature increase
                break
            elif Sensor_IstValue - Sensor_StartValue >= 3:
                print()  # print a blank line
                print("Sensor_StartValue at 0 sec = %d°C" % Sensor_StartValue)  # print the saved StartTemp.
                print("Sensor_IstValue at " + str(seconds) + " sec = " + str(Sensor_IstValue) + "°C")  # print the actual_IstTemp.
                print("Temperature Increase of 3°C achieved in %d seconds elapsed" % seconds)  # print reached Temperature increase
                print()  # print a blank line
                break
                # while seconds <= 960:
                #     print("elapsed seconds = ", seconds)
                #     cdv_actuatorData = doper.get(st.CDV_ActuatorDat)  # get the required variable form DopX interface
                #     Engage_LyePump = cdv_actuatorData["LyePump"]["CurrentValue"]
                #     print("Ist the Lye Pump activated? = ", Engage_LyePump)
                #     if Engage_LyePump:
                #         print("Ist the Lye Pump activated? = ", Engage_LyePump)
                #         cdv_actuatorData = doper.get(st.CDV_ActuatorDat)  # get the required variable form DopX interface
                #             break
                #         global_cs_devicecontext = doper.get(st.GLOBAL_CS_DeviceContext)  # get the required variable form DopX interface
                #         WaterLevel = global_cs_devicecontext["ServiceAttributesWM"]\
                #                                             ["WaterLevel"]\
                #                                             ["CurrentValue"]
                #         print("Ist Water Level = %d mmWS" % (WaterLevel / 10))  # convert to mmWS
                #         Ist_LyePump = cdv_actuatorData["LyePump"]["CurrentValue"]
                #         print("Ist_LyePump = ", Ist_LyePump)
                #         if Max_LyePump - Ist_LyePump <= 5:
                #             reached_LypPump_Decrease = Max_LyePump - Ist_LyePump
                #             print("reached_LypPump_Decrease = ", reached_LypPump_Decrease)
                #             break
                #         return True
        #  -----------------------------------------------------------------------------------------
        #  Temperature Increase checking phase <END> -----------------------------------------------------
        #  -----------------------------------------------------------------------------------------

        # A = False
        # while not A:  # i == False
        #
        #     # NTC-Temperature ---------------------------------------------------
        #     global_cs_devicecontext = doper.get(st.GLOBAL_CS_DeviceContext)
        #     aktuelle_IstTemp = global_cs_devicecontext["ServiceAttributesWM"]\
        #                                             ["NtcTemperature"]\
        #                                             ["CurrentValue"]
        #     print("aktuelle_IstTemp. = %d°C" % aktuelle_IstTemp)
        #
        #     # Actuator ----------------------------------------------------------
        #     cdv_actuatorData = doper.get(st.CDV_ActuatorDat)
        #     Heater1 = cdv_actuatorData["Heater1"]["CurrentValue"]
        #     print(f"Heater Element (Engage ON/OFF) = {bool(Heater1)}")  # convert to boolean value
        #
        #     # Water Level -------------------------------------------------------
        #     WaterLevel = global_cs_devicecontext["ServiceAttributesWM"]\
        #                                         ["WaterLevel"]\
        #                                         ["CurrentValue"]
        #     print("Ist Water Level = %d mmWS" % (WaterLevel / 10))  # convert to mmWS
        #
        #     #  -------------------------------------------------------
        #     if aktuelle_IstTemp >= 25:
        #         print("aktuelle_IstTemp. = %d°C" % aktuelle_IstTemp)
        #         print(f"Heater Element (Engage ON/OFF) = {bool(Heater1)}")  # convert to boolean value
        #         print("Ist Water Level = %d mmWS" % (WaterLevel / 10))  # convert to  mmWS
        #         A = True
        # WaterLevel = global_cs_devicecontext["ServiceAttributesWM"]\
        #                                     ["WaterLevel"]\
        #                                     ["CurrentValue"]
        # #assert (global_cs_devicecontext["ServiceAttributesWM"]["WaterLevel"]["CurrentValue"]) == (WaterLevel / 10)
        # self.assertTrue((global_cs_devicecontext["ServiceAttributesWM"]["WaterLevel"]["CurrentValue"])/10 == (WaterLevel/10))

        #assert (global_cs_devicecontext["ServiceAttributesWM"]["NtcTemperature"]["CurrentValue"]) == IstTemperature
        global_cs_devicecontext = doper.get(st.GLOBAL_CS_DeviceContext)  # get the required variable form DopX interface
        self.assertTrue((global_cs_devicecontext["ServiceAttributesWM"]
                                                ["NtcTemperature"]
                                                ["CurrentValue"]) == Sensor_IstValue)

        self.assertTrue((global_ds_devicestate["RemainingTime"]) / 60 == 29)
        # assert (global_ds_devicestate["RemainingTime"]) / 60 == 7

    @categories("WT1f", "W1")
    def test_WT_Wolle(self):
        """
        Konfiguration Test
        """
        msg["ProgId"] = 8
        msg["SelectionParaWM"]["Extras"]["Single"] = False
        doper.write_part(st.GLOBAL_PS_Select, msg)
        time.sleep(sleep_time / 2)
        """
        Test Infomationen auslesen
        """
        global_ps_context = doper.get(st.GLOBAL_PS_Context)
        print('\n')
        print("ProgId = %d " % global_ps_context["ProgAttributesDWTDWM"]["ProgId"])
        print("MaxProgrammDuration = %d " % global_ps_context["ProgAttributesDWTDWM"]["MaxProgrammDuration"])
        global_ds_devicestate = doper.get(st.GLOBAL_DS_DeviceState)
        print("Remaining Time: %d min " % ((global_ds_devicestate["RemainingTime"]) / 60))
        print("Spinning Speed: %d rpm " % global_ds_devicestate["SpinningSpeed"])

        """        Reporting zusammenstellen        """
        Report.add_heading(1, str(self.__module__))
        tR = Report_heading()
        tR.Kategorie(str(self.__module__))
        tR.SimZeitpunkt("Start die Test-Umgebung und wähle 'Wolle' an")
        tR.Beeinflussung("Programmabbruch mit Abpumpen")
        tR.Beeinflussung("Abpumpzeit verlaengern (um den Wert N6), erneute Abfrage")
        tR.Besonderheiten("zur Zeit keine")
        Report.add_table(tR.get_table(), True)
        Report.add_paragraph("ENDE des Tests " + str(self._testMethodName))
        # Starten
        print("Starten")
        start_program()
        time.sleep(10)
        # print("Warten")
        # # wait_for(lambda: doper.get(st.GLOBAL_CS_DeviceContext)["ServiceAttributesWM"]["WaterLevel"]["CurrentValue"] > 400,
        # #          True, 10, "ich bin hier herein gefallen")
        # print(doper.get(st.GLOBAL_CS_DeviceContext)["ServiceAttributesWM"]["WaterLevel"]["CurrentValue"])
        # print("Warten")
        # time.sleep(1 * 15)
        # print(doper.get(st.GLOBAL_CS_DeviceContext)["ServiceAttributesWM"]["WaterLevel"]["CurrentValue"])
        # # pprint(doper.get(st.GLOBAL_CS_DeviceContext)["ServiceAttributesWM"])
        # print("Warten")
        # time.sleep(1 * 15)
        # print(doper.get(st.GLOBAL_CS_DeviceContext)["ServiceAttributesWM"]["WaterLevel"]["CurrentValue"])
        # print("Warten")
        # time.sleep(1 * 15)
        # print(doper.get(st.GLOBAL_CS_DeviceContext)["ServiceAttributesWM"]["WaterLevel"]["CurrentValue"])
        # print("Warten")
        # time.sleep(1 * 15)
        # print(doper.get(st.GLOBAL_CS_DeviceContext)["ServiceAttributesWM"]["WaterLevel"]["CurrentValue"])
        # # pprint(doper.get(st.GLOBAL_CS_DeviceContext)["ServiceAttributesWM"]["WaterLevel"])
        # assert (global_ds_devicestate["RemainingTime"]) / 60 == 39aha s
        self.assertTrue((global_ds_devicestate["RemainingTime"]) / 60 == 39)

    def tearDown(self):
        self.rec.stop()
        unplug(optical_interface)
        _plot_relevant_data_nvd3(self.rec.file_name)


class Trocknen(TestCase):
    def setUp(self):
        init_device_for_test(optical_interface)
        dopx_read_name = self._testMethodName + self.__module__
        print(dopx_read_name)
        self.rec = ProcessDataRecorder(self._testMethodName, "helpers.test_record.DopXRead")
        self.rec.start()

    @categories("WT1f", "T1")
    def test_WT_Wolle_Single(self):
        """

        :return:
        """
        msg["ProgId"] = 8
        msg["SelectionParaWM"]["ProgramMode"] = 2
        doper.write_part(st.GLOBAL_PS_Select, msg)
        time.sleep(sleep_time / 2)
        """
        Test Infomationen auslesen
        """
        global_ds_devicestate = doper.get(st.GLOBAL_DS_DeviceState)
        time.sleep(sleep_time)
        global_ps_context = doper.get(st.GLOBAL_PS_Context)
        print('\n')
        print("ProgId = %d " % global_ps_context["ProgAttributesDWTDWM"]["ProgId"])
        print("Remaining Time: %d min " % ((global_ds_devicestate["RemainingTime"]) / 60))
        print("Spinning Speed: %d rpm " % global_ds_devicestate["SpinningSpeed"])
        print("MaxProgrammDuration = %d " % global_ps_context["ProgAttributesDWTDWM"]["MaxProgrammDuration"])
        print("DryingTime = %s" % str(global_ps_context["ContextParaWM"]["DryingTime"]))
        print("MinVisible = %d " % global_ps_context["ContextParaWM"]["DryingTime"]["MinVisible"])
        """
        Reporting zusammenstellen
        """
        Report.add_heading(1, str(self.__module__))
        tR = Report_heading()
        tR.Kategorie(str(self.__module__))
        tR.SimZeitpunkt("Start die Test-Umgebung und wähle 'Wolle' an")
        tR.Beeinflussung("Programmabbruch mit Abpumpen")
        tR.Beeinflussung("Abpumpzeit verlaengern (um den Wert N6), erneute Abfrage")
        tR.Besonderheiten("zur Zeit keine")
        Report.add_table(tR.get_table(), True)
        Report.add_paragraph("ENDE des Tests " + str(self._testMethodName))
        # Starten
        start_program()
        time.sleep(15)
        time.sleep(global_ds_devicestate["RemainingTime"])
        assert (global_ds_devicestate["RemainingTime"]) / 60 == 2
        assert global_ps_context["ContextParaWM"]["DryingTime"]["MinVisible"] == 3

    def tearDown(self):
        self.rec.stop()
        unplug(optical_interface)


class WaschenUndTrocknen(TestCase):

    def setUp(self):
        init_device_for_test(optical_interface)
        # signals = [AnalogLine.myBlpmModelNtcTemperature.name]
        dopx_read_name = self._testMethodName + self.__module__
        print(dopx_read_name)
        # self.rec = ProcessDataRecorder(self._testMethodName, signals)
        self.rec = ProcessDataRecorder(self._testMethodName, "helpers.test_record.DopXRead")
        self.rec.start()

    @categories("WT1f")
    @id("611989")
    def test_WT_Waschen_146(self):
        """
        -System hochfahren
            WT Modus 3 anwaelen
            WT Prog. 146 QuickPowerWash
                Singel anwaelen
        """
        time.sleep(sleep_time)
        msg["ProgId"] = 146
        msg["SelectionParaWM"]["ProgramMode"] = 3
        doper.write_part(st.GLOBAL_PS_Select, msg)
        time.sleep(sleep_time)
        global_ds_devicestate = doper.get(st.GLOBAL_DS_DeviceState)
        time.sleep(3)
        global_ps_context = doper.get(st.GLOBAL_PS_Context)
        time.sleep(3)
        global_cs_devicecontext = doper.get(st.GLOBAL_CS_DeviceContext)
        pprint(global_cs_devicecontext)
        print('\n')
        # Starten
        start_program()
        # print((global_ds_devicestate["RemainingTime"]) + 2 * 15)
        # time.sleep((global_ds_devicestate["RemainingTime"]) + 2 * 15)
        # assert wait_for(lambda: global_cs_devicecontext["ServiceAttributesWM"]["WaterLevel"]["CurrentValue"], True,
        #                 60 * 5)
        time.sleep(9 * 15)
        print("ProgId = %d " % global_ps_context["ProgAttributesDWTDWM"]["ProgId"])
        print("MinVisible = %d " % global_ps_context["ContextParaWM"]["DryingTime"]["MinVisible"])
        print("MaxProgrammDuration = %d " % global_ps_context["ProgAttributesDWTDWM"]["MaxProgrammDuration"])
        print("Remaining Time: %d min " % ((global_ds_devicestate["RemainingTime"]) / 60))
        print("Spinning Speed: %d rpm " % global_ds_devicestate["SpinningSpeed"])
        assert global_ps_context["ContextParaWM"]["DryingTime"]["MinVisible"] == 15
        W32COMUSBDEV.Disconnect(optical_interface)

    @categories("WT1f")
    @id("575270")
    def test_WT_Waschen_FMU(self):
        """
        -System hochfahren
            WT Modus 3 anwaelen
            WT Prog. 3  auswaehlen
                Singel anwaelen
        """
        time.sleep(sleep_time)
        msg["ProgId"] = 3
        msg["SelectionParaWM"]["ProgramMode"] = 3
        print("ich bin jetzt hier!!!")
        doper.write_part(st.GLOBAL_PS_Select, msg)
        time.sleep(sleep_time)
        global_ds_devicestate = doper.get(st.GLOBAL_DS_DeviceState)
        time.sleep(sleep_time)
        global_ps_context = doper.get(st.GLOBAL_PS_Context)
        time.sleep(sleep_time)
        # global_cs_devicecontext = doper.get(st.GLOBAL_CS_DeviceContext)
        print("nun bin ich hier!!!")
        # pprint(global_cs_devicecontext)
        print('\n')
        # Starten
        start_program()
        # print((global_ds_devicestate["RemainingTime"]) + 2 * 15)
        # time.sleep((global_ds_devicestate["RemainingTime"]) + 2 * 15)
        # assert wait_for(lambda: global_cs_devicecontext["ServiceAttributesWM"]["WaterLevel"]["CurrentValue"], True,
        #                 60 * 5)
        time.sleep(3 * 15)
        print("ProgId = %d " % global_ps_context["ProgAttributesDWTDWM"]["ProgId"])
        print("MinVisible = %d " % global_ps_context["ContextParaWM"]["DryingTime"]["MinVisible"])
        print("MaxProgrammDuration = %d " % global_ps_context["ProgAttributesDWTDWM"]["MaxProgrammDuration"])
        print("Remaining Time: %d min " % ((global_ds_devicestate["RemainingTime"]) / 60))
        print("Spinning Speed: %d rpm " % global_ds_devicestate["SpinningSpeed"])
        assert global_ps_context["ContextParaWM"]["DryingTime"]["MinVisible"] == 15
        W32COMUSBDEV.Disconnect(optical_interface)

    @categories("WT1f")
    @id("611140")
    def test_WT_Waschen_x(self):
        """
        -System hochfahren
            WT Modus 3 anwaelen
            WT Prog. 3  auswaehlen
                Singel anwaelen
        """
        time.sleep(sleep_time)
        global_program_list = doper.get(st.GLOBAL_ProgramList)
        # global_program_list["ProgramIds"]
        msg["ProgId"] = 1
        doper.write_part(st.GLOBAL_PS_Select, msg)
        time.sleep(sleep_time)
        global_ds_devicestate = doper.get(st.GLOBAL_DS_DeviceState)
        time.sleep(sleep_time)
        global_ps_context = doper.get(st.GLOBAL_PS_Context)
        time.sleep(sleep_time)
        global_cs_devicecontext = doper.get(st.GLOBAL_CS_DeviceContext)
        # pprint(global_cs_devicecontext)
        print('\n')
        # Starten
        start_program()
        # print((global_ds_devicestate["RemainingTime"]) + 2 * 15)
        # time.sleep((global_ds_devicestate["RemainingTime"]) + 2 * 15)
        # assert wait_for(lambda: global_cs_devicecontext["ServiceAttributesWM"]["WaterLevel"]["CurrentValue"], True,
        #                 60 * 5)
        time.sleep(1 * 15)
        print("ProgId = %d " % global_ps_context["ProgAttributesDWTDWM"]["ProgId"])
        print("MinVisible = %d " % global_ps_context["ContextParaWM"]["DryingTime"]["MinVisible"])
        print("MaxProgrammDuration = %d " % global_ps_context["ProgAttributesDWTDWM"]["MaxProgrammDuration"])
        print("Remaining Time: %d min " % ((global_ds_devicestate["RemainingTime"]) / 60))
        print("Spinning Speed: %d rpm " % global_ds_devicestate["SpinningSpeed"])
        assert global_ps_context["ContextParaWM"]["DryingTime"]["MinVisible"] == 15
        W32COMUSBDEV.Disconnect(optical_interface)

    def tearDown(self):
        self.rec.stop()
        unplug(optical_interface)
        _plot_relevant_data_nvd3(self.rec.file_name)


class DopXTest(TestCase):

    def setUp(self):
        init_device_for_test(optical_interface)
        dopx_read_name = self._testMethodName + self.__module__
        print(dopx_read_name)
        self.rec = ProcessDataRecorder(self._testMethodName, "helpers.test_record.DopXRead")
        self.rec.start()

    @categories("WT1f")
    @id("1408268")
    def test_WT_Waschen(self):
        """
        -System hochfahren
            Manuel ein Programm anwählen und STARTEN
        """
        print('\n')
        time.sleep(1 * 15)
        # Starten
        # device.start_program()
        # pprint(doper.get(st.GLOBAL_ProgramList))
        time.sleep(9 * 15)
        W32COMUSBDEV.Disconnect(optical_interface)

    def tearDown(self):
        self.rec.stop()
        unplug(optical_interface)
        time.sleep(sleep_time)
        _plot_relevant_data_nvd3(self.rec.file_name)


class SimpleIoRead(TestCase):
    def test_get_blpm(self):
        print(AnalogLine.myBlpmModelNtcTemperature.get_value())

    def test_rec(self):
        rec = ProcessDataRecorder(self._testMethodName, [AnalogLine.myBlpmModelNtcTemperature.name])
        rec.start()
        time.sleep(10)
        rec.stop()

    def test_rec_expr(self):
        init_device_for_test(optical_interface)
        time.sleep(sleep_time)
        rec = ProcessDataRecorder(self._testMethodName, "helpers.test_record.DopRead")
        rec.start()
        time.sleep(30)
        rec.stop()


# Test specific helper methods #########################################################################################
def _plot_relevant_data_nvd3(file_name):
    df, properties = read_tdms(file_name, "data")
    html_str = create_nvd3_plot(df, channels=["WaterLevel", "WaterInletWay", "DrumSpeedRpm"])
    # TestExecutor.AddRawHtml(html_str)
    Report.add_raw_html(html_str)


def _plot_relevant_data_nvd3_gmt(file_name):
    df, properties = read_tdms(file_name, "data")
    html_str = DyPlot("Test", )
    # TestExecutor.
    print(df)


# class WaterLevel(object):
#     def get_value(self):
#         return doper.get(st.GLOBAL_CS_DeviceContext)["ServiceAttributesWM"]["WaterLevel"]["CurrentValue"]
#
# class DrumSpeedRpm(object):
#     def get_value(self):
#         return doper.get(st.GLOBAL_CS_DeviceContext)["ServiceAttributesWM"]["DrumSpeedRpm"]["CurrentValue"]
#
# sigs_to_log = ["WaterLevel",
#                "DrumSpeedRpm"]

myCic = {'ServiceAttributesWM': {'ActuatorLevel': {'CurrentValue': 0,
                                                   'IntType': 0,
                                                   'RequestMask': 0},
                                 'CondensatPump': {'CurrentValue': 0,
                                                   'IntType': 0,
                                                   'RequestMask': 0},
                                 'DetectedCap': {'CurrentValue': 0,
                                                 'IntType': 0,
                                                 'RequestMask': 0},
                                 'DispenserDrawerSwitch': {'CurrentValue': False,
                                                           'IntType': 0,
                                                           'RequestMask': 0},
                                 'DoorLockSwitch': {'CurrentValue': False,
                                                    'IntType': 0,
                                                    'RequestMask': 0},
                                 'DoorSwitch': {'CurrentValue': True,
                                                'IntType': 0,
                                                'RequestMask': 0},
                                 'DrumSpeedRpm': {'CurrentValue': 0,
                                                  'IntType': 0,
                                                  'RequestMask': 0},
                                 'Heater1': {'CurrentValue': False,
                                             'IntType': 0,
                                             'RequestMask': 0},
                                 'Heater2': {'CurrentValue': False,
                                             'IntType': 0,
                                             'RequestMask': 0},
                                 'IntensiveFlowPump': {'CurrentValue': False,
                                                       'IntType': 0,
                                                       'RequestMask': 0},
                                 'LanceContact': {'CurrentValue': False,
                                                  'IntType': 0,
                                                  'RequestMask': 0},
                                 'LyePump': {'CurrentValue': False,
                                             'IntType': 0,
                                             'RequestMask': 0},
                                 'MIPCalibration': {'CurrentValue': False,
                                                    'IntType': 0,
                                                    'RequestMask': 0},
                                 'NtcTemperature': {'CurrentValue': 22,
                                                    'IntType': 0,
                                                    'RequestMask': 0},
                                 'NtcTemperature2': {'CurrentValue': 0,
                                                     'IntType': 0,
                                                     'RequestMask': 0},
                                 'PaidSignal': {'CurrentValue': False,
                                                'IntType': 0,
                                                'RequestMask': 0},
                                 'PeakLoadSignal': {'CurrentValue': False,
                                                    'IntType': 0,
                                                    'RequestMask': 0},
                                 'ResidualMoisture': {'CurrentValue': 57856,
                                                      'IntType': 0,
                                                      'RequestMask': 0},
                                 'ServiceTestState': 0,
                                 'SteamHeater': {'CurrentValue': False,
                                                 'IntType': 0,
                                                 'RequestMask': 0},
                                 'SteamPump': {'CurrentValue': False,
                                               'IntType': 0,
                                               'RequestMask': 0},
                                 'SteamUnitTemperature': {'CurrentValue': 0,
                                                          'IntType': 0,
                                                          'RequestMask': 0},
                                 'TwinDosPump1': {'CurrentValue': False,
                                                  'IntType': 0,
                                                  'RequestMask': 0},
                                 'TwinDosPump2': {'CurrentValue': False,
                                                  'IntType': 0,
                                                  'RequestMask': 0},
                                 'TwinDosSwitchContainer1': {'CurrentValue': True,
                                                             'IntType': 0,
                                                             'RequestMask': 0},
                                 'TwinDosSwitchContainer2': {'CurrentValue': True,
                                                             'IntType': 0,
                                                             'RequestMask': 0},
                                 'Valve1': {'CurrentValue': False,
                                            'IntType': 0,
                                            'RequestMask': 0},
                                 'Valve2': {'CurrentValue': False,
                                            'IntType': 0,
                                            'RequestMask': 0},
                                 'ValveCoolingWater': {'CurrentValue': 0,
                                                       'IntType': 0,
                                                       'RequestMask': 0},
                                 'WaterDistributorMotor': {'CurrentValue': False,
                                                           'IntType': 0,
                                                           'RequestMask': 0},
                                 'WaterInletWay': {'CurrentValue': 1,
                                                   'IntType': 0,
                                                   'RequestMask': 0},
                                 'WaterLevel': {'CurrentValue': 0,
                                                'IntType': 0,
                                                'RequestMask': 0},
                                 'WpsSwitch': {'CurrentValue': True,
                                               'IntType': 0,
                                               'RequestMask': 0}},
         'SupportedServiceRequests': [0, 0, 0, 0, 0]}
