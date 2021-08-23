from behave import *
from device import init_device_for_test, unplug, start_program
import Report
from helpers.data_recorder import ProcessDataRecorder
import time
from proj_config import st, bt, doper, sleep_time, optical_interface, msg, connecting_time, Report_heading
from Tests.Features.Actor_Classes.Actuators import Actuator_Register
from Tests.Features.Sensor_Classes.Sensors import Sensor_Register
from chilly import wait_for
use_step_matcher("re")


@given("Hil Test Bench Setup is initialized")
def step_impl(context):
    """    Testfall-Setup    """
    init_device_for_test(optical_interface, connecting_time, sleep_time)
    print("Behave BDD Test-Framework is applied")
    print(context)
    context.rec = ProcessDataRecorder("test_toDo", "helpers.test_record.DopXRead")
    context.rec.start()

@step("the physical model, relevant software and simulations have started up")
def step_impl(context):
    """    Wolle waschen mit Anwahl Single    """
    # pprint(AnalogLine.GLOBAL_PS_Context__ContextParaWM.get_value())
    msg["ProgId"] = 8  # Display the program ID
    msg["SelectionParaWM"]["Extras"]["Single"] = True  # Enable the settings of the program variables
    doper.write_part(st.GLOBAL_PS_Select, msg)  # Display selected program on SBAE (System Bedienanzeige-Einheit)
    time.sleep(sleep_time / 2)  # Pause 3 sec
    print("The physical Model has started")
    print("The EFL280 Simulation has started")
    print("DThe ELFU-HiL Simulation has started")
    print("The EZL166 Simulation has started")
    print("The MBUS-Monitor und the Record Process have started")

@step("information from the DopX Communication interface is read out")
def step_impl(context):
    """    Infomationen aus den DopX Elementen auslesen    """
    global_ps_context = doper.get(st.GLOBAL_PS_Context)
    print('\n')
    print("Collect information of the read up variables from the DopX communication interface")
    print("ProgId = %d " % global_ps_context["ProgAttributesDWTDWM"]["ProgId"])
    print("MaxProgrammDuration = %d " % global_ps_context["ProgAttributesDWTDWM"]["MaxProgrammDuration"])
    global_ds_devicestate = doper.get(st.GLOBAL_DS_DeviceState)
    print("Remaining Time: %d min " % ((global_ds_devicestate["RemainingTime"]) / 60))  # 1740 min/60 = 29 min
    print("Spinning Speed: %d rpm " % global_ds_devicestate["SpinningSpeed"])

@step("the Reporting for Test Case is developed")
def step_impl(context):
    """    Reporting zusammenstellen    """
    Report.add_heading(1, "Begin/Start von Test " + str("test_toDo"))
    tR = Report_heading()
    tR.Kategorie(str("test_toDo"))
    tR.SimZeitpunkt("Starte die Test-Umgebung und wähle 'Wolle' an")
    tR.Beeinflussung("Starte den Programmablauf für x-Zeit")
    tR.Beeinflussung("Aufnahme des Testest in deine TDMS Datei")
    tR.Besonderheiten("zur Zeit keine")
    Report.add_table(tR.get_table(), True)
    Report.add_paragraph("ENDE des Tests " + str("test_toDo"))
    print("Reporting for the Test Case is developed")

@when("the electronic_Finger is automatically triggered")
def step_impl(context):
    """    Starting the Simulation of the selected program    """
    print("Start the Simulation of the Program by triggering the electronic Finger")
    start_program()
    time.sleep(10)
    global_ds_devicestate = doper.get(st.GLOBAL_DS_DeviceState)
    context.global_ds_devicestate = global_ds_devicestate

@then("start the Simulation and assert Remaining Time of WT_Wolle")
def step_impl(context):
    """    Asserting the Remaining time     """
    assert ((context.global_ds_devicestate["RemainingTime"]) / 60 == 39)
    time.sleep(sleep_time / 2)
    context.rec.stop()
    print("The asserted Remaining Time = 39 min")
    print("The shutdown process for the physical model, software and simulation is started")
    unplug(optical_interface)


"""""""""""""""""""""" The Second Scenario """""""""""""""""""""""


@given("Hil-Test Bench Setup is initialized")
def step_impl(context):
    """    Testfall-Setup    """
    init_device_for_test(optical_interface, connecting_time, sleep_time)
    print()  # print a blank line
    print("Behave BDD Test-Framework is applied")
    print(context)
    context.rec = ProcessDataRecorder("test_toDo", "helpers.test_record.DopXRead")
    context.rec.start()

@step("the physical model, relevant software, and simulations started up")
def step_impl(context):
    """    Wolle waschen    """
    msg["ProgId"] = 8
    msg["SelectionParaWM"]["Extras"]["Single"] = False  # Enable the settings of the program variables
    doper.write_part(st.GLOBAL_PS_Select, msg)  # Display selected program on SBAE (System Bedienanzeige-Einheit)
    time.sleep(sleep_time / 2)
    print()  # print a blank line
    print("The physical Model has started")
    print("The EFL280 Simulation has started")
    print("DThe ELFU-HiL Simulation has started")
    print("The EZL166 Simulation has started")
    print("The MBUS-Monitor und the Record Process have started")

@step("information from the Communication interface ist read out")
def step_impl(context):
    """    Informationen aus den DopX Elementen auslesen    """
    global_ps_context = doper.get(st.GLOBAL_PS_Context)
    print()  # print a blank line
    print("Collect information of the read up variables from the DopX communication interface")
    # print("ProgId = %d " % global_ps_context["ProgAttributesDWTDWM"]["ProgId"])
    print("Program ID = %d " % global_ps_context["ProgAttributesDWTDWM"]["ProgId"])
    print("Maximum Program Duration = %d " % global_ps_context["ProgAttributesDWTDWM"]["MaxProgrammDuration"])
    global_ds_devicestate = doper.get(st.GLOBAL_DS_DeviceState)
    print("Spinning Speed: %d rpm " % global_ds_devicestate["SpinningSpeed"])
    print("Remaining Time: %d min " % ((global_ds_devicestate["RemainingTime"]) / 60))

@step("the Reporting of the Test Case is developed")
def step_impl(context):
    """    Reporting zusammenstellen    """
    Report.add_heading(1, str("test_toDo"))
    tR = Report_heading()
    tR.Kategorie(str("test_toDo"))
    tR.SimZeitpunkt("Start die Test-Umgebung und wähle 'Wolle' an")
    tR.Beeinflussung("Programmabbruch mit Abpumpen")
    tR.Beeinflussung("Abpumpzeit verlaengern (um den Wert N6), erneute Abfrage")
    tR.Besonderheiten("zur Zeit keine")
    Report.add_table(tR.get_table(), True)
    Report.add_paragraph("ENDE des Tests " + str("test_toDo"))
    print("Reporting for the Test Case is developed")

@when("the electronic_Finger is automatically triggered")
def step_impl(context):
    """    Simulation des angewählten Programms starten    """
    print("Start the Simulation of the Program by triggering the electronic Finger")
    start_program()
    time.sleep(10)
    global_ds_devicestate = doper.get(st.GLOBAL_DS_DeviceState)
    context.global_ds_devicestate = global_ds_devicestate
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
    # assert (global_ds_devicestate["RemainingTime"]) / 60 == 39

@then("start the Simulation and assert Remaining Time of WT_Wolle")
def step_impl(context):
    """    Asserting the Remaining time     """
    assert ((context.global_ds_devicestate["RemainingTime"]) / 60 == 39)
    time.sleep(sleep_time / 2)
    context.rec.stop()
    print("The asserted Remaining Time = 39 min")
    print("The shutdown process for the physical model,"
          "software and simulation is started")
    unplug(optical_interface)


"""""""""""""""""""""" The Third Scenario """""""""""""""""""""""


@given("HiL Test Bench Setup is initialized and Startup is prepared")
def step_impl(context):
    """    Testfall-Setup    """

    init_device_for_test(optical_interface, connecting_time, sleep_time)
    print()  # print a blank line
    print("Behave BDD Test-Framework is applied")
    context.rec = ProcessDataRecorder("test_toDo", "helpers.test_record.DopXRead")
    context.rec.start()


@step("the Program and Software Environment equipped")
def step_impl(context):
    """    Wolle waschen mit Anwahl Single    """

    # global Heater1, StartTemp
    msg["ProgId"] = 8  # Display the program ID
    msg["SelectionParaWM"]["Extras"]["Single"] = True  # Enable the settings of the program variables
    doper.write_part(st.GLOBAL_PS_Select, msg)  # Display selected program on SBAE (System Bedienanzeige-Einheit)
    time.sleep(sleep_time / 2)  # Pause 3 sec
    print()  # print a blank line
    print("The physical Model has started")
    print("The EFL280 Simulation has started")
    print("The ELFU-HiL Simulation has started")
    print("The EZL166 Simulation has started")
    print("The MBUS-Monitor und the Record Process have started")


@step("the Simulation has started")
def step_impl(context):
    """    Infomationen aus den DopX Elementen auslesen    """

    print()  # print a blank line
    print("Collecting information of the variables from the DopX communication interface")
    global_ps_context = doper.get(st.GLOBAL_PS_Context)
    print("ProgId = %d " % global_ps_context["ProgAttributesDWTDWM"]["ProgId"])
    global_ds_devicestate = doper.get(st.GLOBAL_DS_DeviceState)
    print("Remaining Time: %d min " % ((global_ds_devicestate["RemainingTime"]) / 60))  # 1740 min/60 = 29 min
    print("Spinning Speed: %d rpm " % global_ds_devicestate["SpinningSpeed"])
    global_cs_devicecontext = doper.get(st.GLOBAL_CS_DeviceContext)
    print()  # print a blank line

    """    Reporting zusammenstellen    """
    Report.add_heading(1, "Begin/Start von Test " + str("test_toDo"))
    tR = Report_heading()
    tR.Kategorie(str("test_toDo"))
    tR.SimZeitpunkt("Starte die Test-Umgebung und wähle 'Wolle' an")
    tR.Beeinflussung("Starte den Programmablauf für x-Zeit")
    tR.Beeinflussung("Aufnahme des Testest in deine TDMS Datei")
    tR.Besonderheiten("zur Zeit keine")
    Report.add_table(tR.get_table(), True)
    Report.add_paragraph("ENDE des Tests " + str("test_toDo"))
    print("Reporting for the scenario is developed")
    print()  # print a blank line

    """    Simulation des angewählten Programms starten    """
    print("Starting the Program by triggering the electronic Finger")
    print()  # print a blank line
    time.sleep(sleep_time)
    start_program()  # pressing the electronic Finger the start the program


@when("the (?P<actuator_name>[\W\w]+) has been (?P<condition>[\W\w]+)")
def activate_heatElement(context, actuator_name, condition):
    """    Check switching-ON of the actuator     """
    actuator = Actuator_Register[actuator_name](actuator_name, condition)
    actuator.get_actuator()
    print(str(actuator_name) + " Status (Engage ON/OFF) = " +
          str(bool(actuator.Engaged)))
    # Saving Sensor_StartValue at 0 sec
    if actuator.Engaged:  # if actuator == True
        global_cs_devicecontext = actuator.doper.get(st.GLOBAL_CS_DeviceContext)  # get the required variable form DopX interface
        Sensor_StartValue = global_cs_devicecontext["ServiceAttributesWM"]\
                                                   ["NtcTemperature"]\
                                                   ["CurrentValue"]  # read out "Sensor_StartValue" value from DopX interface
        print("Sensor_StartValue = %d" % Sensor_StartValue)  # print the "Sensor_StartValue"
        print()  # print a blank line

@step("the (?P<sensor>[\W\w]+) reach (?P<soll>[\W\w]+) (?P<unit>[\W\w]+) with "
      "Dynamic Behaviour complies (?P<expect_value>[\W\w]+) °C per (?P<expect_time>[\W\w]+) seconds")
def step_impl(context, sensor, soll, unit, expect_value, expect_time):
    """    Regulation the Sensor inquired status within the given period     """
    Scenario = Sensor_Register[sensor](context, sensor)
    Scenario.CheckDynamicBehaviour(sensor, soll=soll, unit=unit, expect=[expect_value, expect_time])


@then("assert the (?P<sensor>[\W\w]+) after statues validation")
def step_impl(context, sensor):
    """    Sensor assertion after validation     """
    print(str(sensor) + " check is successfully asserted")
    print()  # print a blank line
    context.rec.stop()
    print("The shutdown process for the physical model, software and simulation is started")
    unplug(optical_interface)


@step("the (?P<sensor>[\W\w]+) is (?P<status>[\W\w]+) (?P<value>[\W\w]+)"
      " (?P<unit>[\W\w]+) within (?P<period>[\W\w]+) seconds")
def step_impl(context, sensor, status, value, unit, period):
    """    Controlling the Sensor inquired status within the given period      """
    Scenario = Sensor_Register[sensor](context, sensor, status, value, unit, period)
    if status == "below":
        Scenario.Below(sensor, status, value, unit, period)
    elif status == "above":
        Scenario.Above(sensor, status, value, unit, period)





@step("the (?P<sensor>[\W\w]+) reach (?P<soll>[\W\w]+) (?P<unit>[\W\w]+) with Dynamic Behaviour complies (?P<expect_value>[\W\w]+) °C per (?P<expect_time>[\W\w]+) sec")
def step_impl(context, sensor, soll, unit, expect_value, expect_time):
    Scenario = Sensor_Register[sensor](context, sensor)
    Scenario.CheckDynamicBehaviour(soll, unit=unit, expect=[expect_value, expect_time])



# actuator must be condition
@then("the (?P<actuator_name>[\W\w]+) must be (?P<condition>[\W\w]+)")
def step_impl(context, actuator_name, condition):
    """    Check on/off switching of the actuator    """

    actuator = Actuator_Register[actuator_name](actuator_name, condition)
    actuator.get_actuator()
    print(str(actuator_name) + " Status " + str(condition) +
          " = " + str(bool(actuator.Engaged)))
    context.rec.stop()
    print("The shutdown process for the physical model, software and simulation is started")
    unplug(optical_interface)


@then("assert the (?P<sensor>[\W\w]+) (?P<status>[\W\w]+) of (?P<value>[\W\w]+) (?P<unit>[\W\w]+) within (?P<period>[\W\w]+) seconds")
def step_impl(context, sensor, status, value, unit, period):

    Scenario = Sensor_Register[sensor](context, sensor, status, value, unit, period)
    if status == "Increase":
        Scenario.Increase(sensor, status, value, unit, period)
    elif status == "Decrease":
        Scenario.Decrease(sensor, status, value, unit, period)
    elif status == "Difference":
        Scenario.Difference(sensor, status, value, unit, period)
    Scenario.shutdown()


# sensor is below/above value unit



# all actuator must be condition
@then("all (?P<actuators>[\W\w]+) must be (?P<condition>[\W\w]+)")
def step_impl(context, actuators, condition):

    all_Actuators = list(Actuator_Register.keys())
    for i in range(all_Actuators):
        actuator = Actuator_Register[all_Actuators[i]](all_Actuators[i], condition)
        actuator.get_actuator()


@given("SiL-Test Bench Setup is initialized")
def step_impl(context):
    """    Testfall-Setup    """
    init_device_for_test(optical_interface, connecting_time, sleep_time)
    print()  # print a blank line
    print("Behave BDD Test-Framework is applied")
    print(context)
    context.rec = ProcessDataRecorder("test_toDo", "helpers.test_record.DopXRead")
    context.rec.start()

@step("the physical model, relevant software and simulations have started up")
def step_impl(context):
    """    Wolle waschen mit Anwahl Single    """
    # pprint(AnalogLine.GLOBAL_PS_Context__ContextParaWM.get_value())
    msg["ProgId"] = 8  # Display the program ID
    msg["SelectionParaWM"]["Extras"]["Single"] = True  # Enable the settings of the program variables
    doper.write_part(st.GLOBAL_PS_Select, msg)  # Display selected program on SBAE (System Bedienanzeige-Einheit)
    time.sleep(sleep_time / 2)  # Pause 3 sec
    print("The physical Model has started")
    print("The EFL280 Simulation has started")
    print("DThe ELFU-HiL Simulation has started")
    print("The EZL166 Simulation has started")
    print("The MBUS-Monitor und the Record Process have started")

@step("information from the DopX Communication interface is read out")
def step_impl(context):
    """    Infomationen aus den DopX Elementen auslesen    """
    global_ps_context = doper.get(st.GLOBAL_PS_Context)
    print('\n')
    print("Collect information of the read up variables from the DopX communication interface")
    print("ProgId = %d " % global_ps_context["ProgAttributesDWTDWM"]["ProgId"])
    print("MaxProgrammDuration = %d " % global_ps_context["ProgAttributesDWTDWM"]["MaxProgrammDuration"])
    global_ds_devicestate = doper.get(st.GLOBAL_DS_DeviceState)
    print("Remaining Time: %d min " % ((global_ds_devicestate["RemainingTime"]) / 60))  # 1740 min/60 = 29 min
    print("Spinning Speed: %d rpm " % global_ds_devicestate["SpinningSpeed"])

@step("the Reporting for Test Case is developed")
def step_impl(context):
    """    Reporting zusammenstellen    """
    Report.add_heading(1, "Begin/Start von Test " + str("test_toDo"))
    tR = Report_heading()
    tR.Kategorie(str("test_toDo"))
    tR.SimZeitpunkt("Starte die Test-Umgebung und wähle 'Wolle' an")
    tR.Beeinflussung("Starte den Programmablauf für x-Zeit")
    tR.Beeinflussung("Aufnahme des Testest in deine TDMS Datei")
    tR.Besonderheiten("zur Zeit keine")
    Report.add_table(tR.get_table(), True)
    Report.add_paragraph("ENDE des Tests " + str("test_toDo"))
    print("Reporting for the Test Case is developed")

@when("the electronic_Finger is automatically triggered")
def step_impl(context):
    """    Starting the Simulation of the selected program    """
    print("Start the Simulation of the Program by triggering the electronic Finger")
    start_program()
    time.sleep(10)
    global_ds_devicestate = doper.get(st.GLOBAL_DS_DeviceState)
    context.global_ds_devicestate = global_ds_devicestate

@then("start the Simulation and assert Remaining Time of WT_Wolle")
def step_impl(context):
    """    Asserting the Remaining time     """
    assert ((context.global_ds_devicestate["RemainingTime"]) / 60 == 7)
    time.sleep(sleep_time / 2)
    context.rec.stop()
    print("The asserted Remaining Time = 7 min")
    unplug(optical_interface)
