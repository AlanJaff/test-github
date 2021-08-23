from Skylab.Signal import DigitalLine, AnalogLine, DiscreteLine
from Skylab.Statement import SimulationNET, W32COMUSBDEV
import pytest
from doper import build_optic_monitor_sky, build_optic_doper
from Process.Doper.ST import ST
from time import sleep
from DataAnalysis.Record import TdmsRecord
from Time import wait_for
from Skytest import TestCase
from pprint import pprint

optical_interface = "OPT_SIM"
# "OPT_TARGET"

msg = {"ProgId": 1,
       "SelectionType": 4,
       "SelectionParaWM": {
           "DelayedStart": 0,
           "DelayedStartMode": 0,
           "Temperature": 60,
           "TemperatureInfo": 0,
           "SpinSpeed": 80,
           "SoilingDegree": 2,
           "MasterCare": 0,
           "Cap": 0,
           "PreparationSpinLevel": 0,
           "SpinDuration": 0,
           "AutoDosing": {
               "Container": [0, 2],
               "NoLaundryDetergent": False,
               "NoFabricConditioner": False,
               "NoAdditive": False
           },
           "Extras": {
               "Quick": False,
               "Single": False,
               "WaterPlus": False,
               "RinsingPlus": False,
               "PreWash": False,
               "Soak": False,
               "RinseHold": False,
               "ExtraQuiet": False,
               "SteamSmoothing": False,
               "PreRinse": False,
               "Microfibre": False,
               "Gentle": False,
               "AllergoWash": False,
               "Eco": False,
               "Intensive": False,
               "StarchHold": False
           },
           "Load": 0,
           "ProgramAssistent": 0,
           "StainsSelection": 0,
           "ProgramMode": 1,
           "ResidualMoisture": 16,
           "DryingTime": 0
       }
       }

msg_context_para_wm = {
    'Extras': {
        'StarchHold': {
            'RequestMask': 0,
            'CurrentValue': False,
            'IntType': 0},
        'Quick': {
            'RequestMask': 0,
            'CurrentValue': False,
            'IntType': 0},
        'Single': {
            'RequestMask': 9,
            'CurrentValue': False,
            'IntType': 0},
        'WaterPlus': {
            'RequestMask': 0,
            'CurrentValue': False,
            'IntType': 0},
        'RinsingPlus': {
            'RequestMask': 0,
            'CurrentValue': False,
            'IntType': 0},
        'PreWash': {
            'RequestMask': 0,
            'CurrentValue': False,
            'IntType': 0},
        'Soak': {
            'RequestMask': 0,
            'CurrentValue': False,
            'IntType': 0},
        'RinseHold': {
            'RequestMask': 0,
            'CurrentValue': False,
            'IntType': 0},
        'ExtraQuiet': {
            'RequestMask': 9,
            'CurrentValue': False,
            'IntType': 0},
        'SteamSmoothing': {
            'RequestMask': 0,
            'CurrentValue': False,
            'IntType': 0},
        'PreRinse': {
            'RequestMask': 0,
            'CurrentValue': False,
            'IntType': 0},
        'Microfibre': {
            'RequestMask': 0,
            'CurrentValue': False,
            'IntType': 0},
        'Gentle': {
            'RequestMask': 0,
            'CurrentValue': False,
            'IntType': 0},
        'AllergoWash': {
            'RequestMask': 0,
            'CurrentValue': False,
            'IntType': 0},
        'Eco': {
            'RequestMask': 0,
            'CurrentValue': False,
            'IntType': 0},
        'Intensive': {
            'RequestMask': 0,
            'CurrentValue': False,
            'IntType': 0}},
    'Load': {
        'RequestMask': 0,
        'Min': 0,
        'Max': 0,
        'CurrentValue': 0,
        'StepSize': 0,
        'IntType': 0},
    'DelayedStart': {
        'IntType': 0,
        'RequestMask': 9,
        'Min': 0,
        'Max': 0,
        'CurrentValue': 0,
        'NumberOfElements': 0,
        'ParameterArray': [0],
        'ParameterArrayExt': [0]},
    'ProgramAssistant': {
        'RequestMask': 0,
        'VisibleBits': 0,
        'AdjustableBits': 0,
        'CurrentValue': 0,
        'IntType': 0},
    'DelayedStartMode': {
        'RequestMask': 9,
        'SupportedBits': 6,
        'CurrentValue': 0,
        'IntType': 0},
    'StainsSelection': {
        'RequestMask': 0,
        'VisibleBits': 0,
        'AdjustableBits': 0,
        'CurrentValue': 0,
        'IntType': 0},
    'Temperatures': {
        'RequestMask': 9,
        'CurrentValue': 30,
        'CurrentValueInfo': 0,
        'NumOfElements': 4,
        'ParameterArray': [0, 20, 30, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'ValueInfo': [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'IntType': 2},
    'ProgramMode': {
        'RequestMask': 9,
        'SupportedBits': 3,
        'CurrentValue': 3,
        'IntType': 0},
    'ResidualMoisture': {
        'RequestMask': 0,
        'VisibleBits': 0,
        'AdjustableBits': 0,
        'CurrentValue': 0,
        'IntType': 0},
    'SpinSpeeds': {
        'RequestMask': 9,
        'CurrentValue': 80,
        'CurrentValueInfo': 0,
        'NumOfElements': 3,
        'ParameterArray': [80, 100, 120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'ValueInfo': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'IntType': 0},
    'DryingTime': {
        'IntType': 0,
        'RequestMask': 9,
        'MinVisible': 3,
        'MinAdjustable': 3,
        'MaxVisible': 3,
        'MaxAdjustable': 3,
        'CurrentValue': 3,
        'StepSize': 1},
    'SoilingDegrees': {
        'RequestMask': 0,
        'CurrentValue': 0,
        'NumOfElements': 0,
        'ParameterArray': [0, 0, 0, 0, 0, 0],
        'IntType': 0},
    'MasterCareOptions': {
        'RequestMask': 0,
        'CurrentValue': 0,
        'NumOfElements': 0,
        'ParameterArray': [0, 0, 0, 0, 0, 0],
        'IntType': 0},
    'Caps': {
        'RequestMask': 9,
        'CurrentValue': 0,
        'NumOfElements': 3,
        'ParameterArray': [0, 1, 2, 0, 0, 0],
        'IntType': 0},
    'PreaparationSpinLevel': {
        'RequestMask': 0,
        'CurrentValue': 0,
        'NumOfElements': 0,
        'ParameterArray': [0, 0, 0, 0, 0, 0],
        'IntType': 0},
    'Powerwash': {
        'RequestMask': 0,
        'CurrentValue': False,
        'IntType': 0},
    'EcoFeedback': {
        'RequestMask': 0,
        'CurrentValue': False,
        'IntType': 0},
    'SpinDuration': {
        'RequestMask': 0,
        'Min': 0,
        'Max': 0,
        'CurrentValue': 0,
        'StepSize': 0,
        'IntType': 0},
    'AutoDosing': {
        'Container': [{'RequestMask': 0, 'SupportedBits': 0, 'CurrentValue': 0, 'IntType': 0},
                      {'RequestMask': 0, 'SupportedBits': 0, 'CurrentValue': 0, 'IntType': 0}],
        'NoLaundryDetergent': {
            'RequestMask': 0,
            'CurrentValue': False,
            'IntType': 0},
        'NoFabricConditioner': {
            'RequestMask': 0,
            'CurrentValue': False,
            'IntType': 0},
        'NoAdditive': {
            'RequestMask': 0,
            'CurrentValue': False,
            'IntType': 0},
        'NotAdjustableInfo': [2, 2]}}

msg_global = 4



# Bitmask for StainsSelection
GLOBAL_PS_STAIN_BLOOD = 1
GLOBAL_PS_STAIN_COLA = 2
GLOBAL_PS_STAIN_EGG = 4
GLOBAL_PS_STAIN_FAT = 8
GLOBAL_PS_STAIN_FRUIT_VEGETABLE_JUICE = 16
GLOBAL_PS_STAIN_VEGETABLE = 32
GLOBAL_PS_STAIN_GRASS = 64
GLOBAL_PS_STAIN_COFFEE = 128
GLOBAL_PS_STAIN_COCOA = 256
GLOBAL_PS_STAIN_KETCHUP = 512
GLOBAL_PS_STAIN_COLLAR_SOILING = 1024
GLOBAL_PS_STAIN_LIPSTICK = 2048
GLOBAL_PS_STAIN_MAKEUP = 4096
GLOBAL_PS_STAIN_MAYONNAISE = 8192
GLOBAL_PS_STAIN_FRUIT = 16384
GLOBAL_PS_STAIN_OIL_GREASE = 32768
GLOBAL_PS_STAIN_RED_WINE = 65536
GLOBAL_PS_STAIN_SAND_SOIL = 131072
GLOBAL_PS_STAIN_CHOCOLATE = 262144
GLOBAL_PS_STAIN_SWEAT = 524288
GLOBAL_PS_STAIN_TEA = 1048576
GLOBAL_PS_STAIN_URINE = 2097152
GLOBAL_PS_STAIN_UNIVERSAL = 4194304

@pytest.fixture
def simulation():
    if optical_interface == 'OPT_SIM':
        print("\n")
        print("OPT_SIM = ON")
        sleep_time = 6
        conecting_time = 10000
        SimulationNET.Start("EFL280", "")

        sleep(sleep_time)
        SimulationNET.Start("ELFU", "")

        sleep(sleep_time)
        SimulationNET.Start("EZL166", "")

        # sleep(sleep_time)
        # SimulationNET.Start("XKM", "")

        sleep(sleep_time)
        SimulationNET.Start("EPW", "")
        sleep(sleep_time)
        while not SimulationNET.IsConnected("EFL280"):
            SimulationNET.Connect("EFL280", conecting_time)
        # while not SimulationNET.IsConnected("ELFU"):
        #      SimulationNET.Connect("ELFU", conecting_time)
        # while not SimulationNET.IsConnected("EZL166"):
        #     SimulationNET.Connect("EZL166", conecting_time)
        while not SimulationNET.IsConnected("EPW"):
            SimulationNET.Connect("EPW", conecting_time)
        # while not SimulationNET.IsConnected("XKM"):
        #     SimulationNET.Connect("XKM", conecting_time)
        yield None
        SimulationNET.Disconnect("ELFU")
        SimulationNET.Stop("EFL280")
        SimulationNET.Stop("ELFU")
        SimulationNET.Stop("EZL166")
        # SimulationNET.Stop("XKM")
        SimulationNET.Stop("EPW")
        print("OPT_SIM = OFF")
    else:
        print("OPT_TARGET = ON")
        yield None
        print("OPT_TARGET = OFF")

@pytest.fixture
def recording(simulation):
    print("RCORDING = ON")
    # logfile_name = "Test" + "_" + _testMethodName + "_" + datetime.now().strftime(
    #     '%Y%m%d_%H%M%S') + ".tdms"
    # print(Logging.SignalsComplete.__module__ + "." + Logging.SignalsComplete.__name__)
    # self.rec = TdmsRecord(file_name=self.logfile_name,
    #                       group_name="Logging",
    #                       channels=Logging.SignalsComplete.__module__ + "." + Logging.SignalsComplete.__name__,
    #                       cycle_time_ms=500,
    #                       debug=False)

    class MyTestSingnals(object):
        def run(self):
            if not W32COMUSBDEV.IsConnected(optical_interface):
                W32COMUSBDEV.Connect(optical_interface)
            sleep(2)
            monitor = build_optic_monitor_sky(optical_interface)
            doper = build_optic_doper(rx_id=14, rx_unit=254, optic_monitor=monitor)
            st_unit = ST()
            sleep(2)
            global_ds_devicestate = doper.get(st_unit.GLOBAL_DS_DeviceState)
            sleep(2)
            global_ps_context = doper.get(st_unit.GLOBAL_PS_Context)
            sleep(2)
            signals = {"MaxVisible": global_ps_context["ContextParaWM"]["DryingTime"]["MaxVisible"],
                       "ProgId": (global_ps_context["ProgAttributesDWTDWM"]["ProgId"]),
                       "MinVisible": (global_ps_context["ContextParaWM"]["DryingTime"]["MinVisible"]),
                       "MaxProgrammDuration": (global_ps_context["ProgAttributesDWTDWM"]["MaxProgrammDuration"]),
                       "RemainingTime": global_ds_devicestate["RemainingTime"] / 60,
                       "SpinningSpeed": global_ds_devicestate["SpinningSpeed"]}
            return signals

    tdms_rec = TdmsRecord("test_record_pc_example.tdms", "exprGroup", "Tests.test_harmonic.recording.MyTestSingnals", 200)

    #         signals = [AnalogLine.LyeThetaSensorTemperature.name,
    #                    DiscreteLine.myBlpmModelIstNiveaux10.name,
    #            DigitalLine.myBlpmModelHeatingLIsActive.name,
    #            DigitalLine.myBlpmModelHeatingNIsActive.name,
    #            DigitalLine.Valve1IsActive.name,
    #            DiscreteLine.myBlpmModelIstDrehzahlUMin.name,
    #            DigitalLine.Valve3IsActive.name,
    #            DiscreteLine.myBlpmModelDruckwert.name]
    # tdms_rec = TdmsRecord("test_record_pc_example.tdms", "data", signals, 200)
    print("RECORDING = START")
    tdms_rec.start()
    yield None
    print("RECORDING = STOP")
    tdms_rec.stop()
    print("RECORDING = OFF")

@pytest.fixture
def startProgram(simulation):
    if not W32COMUSBDEV.IsConnected(optical_interface):
        W32COMUSBDEV.Connect(optical_interface)
    sleep(6)
    monitor = build_optic_monitor_sky(optical_interface)
    doper = build_optic_doper(rx_id=14, rx_unit=254, optic_monitor=monitor)
    st_unit = ST()

    # msg["ProgId"] = 146
    doper.write_part(st_unit.GLOBAL_PS_Select, msg)
    sleep(2)
    # sleep(250)
    DigitalLine.TASTE_START_STOP.set_value(True)
    # rec = TdmsRecord.channels
    # sleep(150)
    assert wait_for(DigitalLine.TASTE_START_STOP.get_value, True, )
    DigitalLine.TASTE_START_STOP.set_value(False)

    # assert wait_for(lambda: DigitalLine.myBlpmModelDruckwert.get_value(), 25)

    W32COMUSBDEV.Disconnect(optical_interface)

def test_doper(simulation):
    monitor = build_optic_monitor_sky(optical_interface)
    doper = build_optic_doper(rx_id=14, rx_unit=254, optic_monitor=monitor)
    st_unit = ST()
    context = doper.get(st_unit.GLOBAL_PS_Context)
    print('\n')
    pprint(context)
    global_cs_service_request = doper.get(st_unit.GLOBAL_CS_ServiceRequest)
    print('\n')
    pprint(global_cs_service_request)

def test_select_program(simulation):
    if not W32COMUSBDEV.IsConnected(optical_interface):
        W32COMUSBDEV.Connect(optical_interface)

    sleep(3)
    monitor = build_optic_monitor_sky(optical_interface)
    doper = build_optic_doper(rx_id=14, rx_unit=254, optic_monitor=monitor)
    st_unit = ST()
    doper.write_part(st_unit.GLOBAL_PS_Select, msg)
    res = doper.get(st_unit.GLOBAL_DS_DeviceState)
    print("Remaining Time: %d" % res["RemainingTime"])
    sleep(6)
    # DigitalLine.TASTE_START_STOP.set_value(True)
    # sleep(0.25)
    # DigitalLine.TASTE_START_STOP.set_value(False)
    sleep(30)
    # assert wait_for(lambda: DigitalLine.TASTE_START_STOP.get_value(), True, 15, "Warete bis Programm Startet", 0.5)
    # assert True
    W32COMUSBDEV.Disconnect(optical_interface)

def test_select_program_gmt(simulation):
    if not W32COMUSBDEV.IsConnected(optical_interface):
        W32COMUSBDEV.Connect(optical_interface)
    sleep(1)

    monitor = build_optic_monitor_sky(optical_interface)
    doper = build_optic_doper(rx_id=14, rx_unit=254, optic_monitor=monitor)
    st_unit = ST()
    res = doper.get(st_unit.GLOBAL_ProgramList)
    a = (res["ProgramIds"])
    b = a.__len__()
    print('\n')
    print(a.__len__())
    print(str(a))
    # print(a[3])
    i = 1
    while i < b - 1:
        msg["ProgId"] = a[i]
        doper.write_part(st_unit.GLOBAL_PS_Select, msg)
        sleep(2)
        res = doper.get(st_unit.GLOBAL_DS_DeviceState)
        # sleep(6)
        # global_ps_context = doper.get(st_unit.GLOBAL_PS_Context)
        # temperatre_array_av = global_ps_context["ContextParaWM"]["Temperatures"]["ParameterArray"]
        # print(str(temperatre_array_av))
        # print(global_ps_context)
        print("Remaining Time: %d" % res["RemainingTime"])
        print("Spinning Speed: %d" % res["SpinningSpeed"])
        sleep(5)
        i += 1
        # assert wait_for(lambda: DigitalLine.TASTE_START_STOP, True, 60*5)
    W32COMUSBDEV.Disconnect(optical_interface)

def test_select_programmList(simulation):
    if not W32COMUSBDEV.IsConnected(optical_interface):
        W32COMUSBDEV.Connect(optical_interface)
    sleep(3)
    monitor = build_optic_monitor_sky(optical_interface)
    doper = build_optic_doper(rx_id=14, rx_unit=254, optic_monitor=monitor)
    st_unit = ST()
    res = doper.get(st_unit.GLOBAL_ProgramList)
    a = (res["ProgramIds"])
    # print(a.__len__())
    # print(str(a))
    # print(a[3])
    cdv_process_data = doper.get(st_unit.CDV_ProcessData)
    global_ps_context = doper.get(st_unit.GLOBAL_PS_Context)
    print('\n')
    print('ProgrammPhase = %d ' % cdv_process_data["ProgPhase"]["CurrentValue"])
    print('ProgrammPhase = %d \n' % global_ps_context["ProgAttributesDWTDWM"]["ProgPhase"])
    # print("ProgrammPhase = %d" % myres["ProgAttributesCCA"])
    W32COMUSBDEV.Disconnect(optical_interface)

def test_ProgrammStart(simulation):
    if not W32COMUSBDEV.IsConnected(optical_interface):
        W32COMUSBDEV.Connect(optical_interface)
    sleep(6)
    monitor = build_optic_monitor_sky(optical_interface)
    doper = build_optic_doper(rx_id=14, rx_unit=254, optic_monitor=monitor)
    st_unit = ST()

    msg["ProgId"] = 146  # Progammauswahl
    doper.write_part(st_unit.GLOBAL_PS_Select, msg)  # Programm
    sleep(2)
    # sleep(250)
    DigitalLine.TASTE_START_STOP.set_value(True)
    # rec = TdmsRecord.channels
    # sleep(150)
    assert wait_for(DigitalLine.TASTE_START_STOP.get_value, True, )
    DigitalLine.TASTE_START_STOP.set_value(False)

    # assert wait_for(lambda: DigitalLine.myBlpmModelDruckwert.get_value(), 25)

    W32COMUSBDEV.Disconnect(optical_interface)

def test_WT_Wolle_Single(recording):
    """
    -System hochfahren
        WT Modus 3 anwaelen
        WT Prog. 8 fuer Wolle auswaehlen
            Singel anwaelen
    :param simulation:
    :return: -
    """
    if not W32COMUSBDEV.IsConnected(optical_interface):
        W32COMUSBDEV.Connect(optical_interface)
    sleep(6)
    monitor = build_optic_monitor_sky(optical_interface)
    doper = build_optic_doper(rx_id=14, rx_unit=254, optic_monitor=monitor)
    st_unit = ST()

    # pprint(AnalogLine.GLOBAL_PS_Context__ContextParaWM.get_value())
    msg["ProgId"] = 8
    msg["SelectionParaWM"]["ProgramMode"] = 3
    msg["SelectionParaWM"]["Extras"]["Single"] = True
    doper.write_part(st_unit.GLOBAL_PS_Select, msg)
    sleep(6)
    global_ds_devicestate = doper.get(st_unit.GLOBAL_DS_DeviceState)
    sleep(6)
    global_ps_context = doper.get(st_unit.GLOBAL_PS_Context)
    context_para_wm = global_ps_context["ContextParaWM"]
    prog_attributes_dwtdwm = global_ps_context["ProgAttributesDWTDWM"]
    # pprint(prog_attributes_dwtdwm)
    print('\n')
    # pprint(context_para_wm)
    print("DryingTime = %s" % str(global_ps_context["ContextParaWM"]["DryingTime"]))
    print("ProgId = %d " % global_ps_context["ProgAttributesDWTDWM"]["ProgId"])
    print("MinVisible = %d " % global_ps_context["ContextParaWM"]["DryingTime"]["MinVisible"])
    print("MaxProgrammDuration = %d " % global_ps_context["ProgAttributesDWTDWM"]["MaxProgrammDuration"])
    print("Remaining Time: %d min " % ((global_ds_devicestate["RemainingTime"]) / 60))
    print("Spinning Speed: %d rpm " % global_ds_devicestate["SpinningSpeed"])
    sleep(6)
    assert global_ps_context["ContextParaWM"]["DryingTime"]["MinVisible"] == 3
    W32COMUSBDEV.Disconnect(optical_interface)

def test_WT_Wolle(simulation):
    """
    -System hochfahren
        WT Modus 3 anwaelen
        WT Prog. 8 fuer Wolle auswaehlen
            Singel anwaelen
    :param simulation:
    :return: -
    """
    if not W32COMUSBDEV.IsConnected(optical_interface):
        W32COMUSBDEV.Connect(optical_interface)
    sleep(6)
    monitor = build_optic_monitor_sky(optical_interface)
    doper = build_optic_doper(rx_id=14, rx_unit=254, optic_monitor=monitor)
    st_unit = ST()

    msg["ProgId"] = 8
    msg["SelectionParaWM"]["ProgramMode"] = 3
    doper.write_part(st_unit.GLOBAL_PS_Select, msg)
    sleep(6)
    global_ds_devicestate = doper.get(st_unit.GLOBAL_DS_DeviceState)
    sleep(6)
    global_ps_context = doper.get(st_unit.GLOBAL_PS_Context)
    print('\n')
    DigitalLine.TASTE_START_STOP.set_value(True)
    sleep(0.25)
    DigitalLine.TASTE_START_STOP.set_value(False)
    sleep(3)
    sleep(10*15)
    print("DryingTime = %s" % str(global_ps_context["ContextParaWM"]["DryingTime"]))
    print("ProgId = %d " % global_ps_context["ProgAttributesDWTDWM"]["ProgId"])
    print("MinVisible = %d " % global_ps_context["ContextParaWM"]["DryingTime"]["MinVisible"])
    print("MaxProgrammDuration = %d " % global_ps_context["ProgAttributesDWTDWM"]["MaxProgrammDuration"])
    print("Remaining Time: %d min " % ((global_ds_devicestate["RemainingTime"]) / 60))
    print("Spinning Speed: %d rpm " % global_ds_devicestate["SpinningSpeed"])
    assert global_ps_context["ContextParaWM"]["DryingTime"]["MinVisible"] == 3
    W32COMUSBDEV.Disconnect(optical_interface)

def test_WT_Waschen(simulation):
    """
    -System hochfahren
        WT Modus 3 anwaelen
        WT Prog. 8 fuer Wolle auswaehlen
            Singel anwaelen
    :param simulation:
    :return: -
    """
    if not W32COMUSBDEV.IsConnected(optical_interface):
        W32COMUSBDEV.Connect(optical_interface)
    sleep(3)
    monitor = build_optic_monitor_sky(optical_interface)
    doper = build_optic_doper(rx_id=14, rx_unit=254, optic_monitor=monitor)
    st_unit = ST()

    msg["ProgId"] = 146
    # msg["SelectionParaWM"]["ProgramMode"] = 3
    doper.write_part(st_unit.GLOBAL_PS_Select, msg)
    sleep(3)
    global_ds_devicestate = doper.get(st_unit.GLOBAL_DS_DeviceState)
    sleep(3)
    global_ps_context = doper.get(st_unit.GLOBAL_PS_Context)
    print('\n')
    DigitalLine.TASTE_START_STOP.set_value(True)
    sleep(0.25)
    DigitalLine.TASTE_START_STOP.set_value(False)
    sleep((global_ds_devicestate["RemainingTime"]) + 2*15)
    print("DryingTime = %s" % str(global_ps_context["ContextParaWM"]["DryingTime"]))
    print("ProgId = %d " % global_ps_context["ProgAttributesDWTDWM"]["ProgId"])
    print("MinVisible = %d " % global_ps_context["ContextParaWM"]["DryingTime"]["MinVisible"])
    print("MaxProgrammDuration = %d " % global_ps_context["ProgAttributesDWTDWM"]["MaxProgrammDuration"])
    print("Remaining Time: %d min " % (global_ds_devicestate["RemainingTime"]) / 60)
    print("Spinning Speed: %d rpm " % global_ds_devicestate["SpinningSpeed"])
    assert global_ps_context["ContextParaWM"]["DryingTime"]["MinVisible"] == 15
    W32COMUSBDEV.Disconnect(optical_interface)

