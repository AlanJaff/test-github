@when("the Heat Actuator has been activated")
def activate_heat(context):

    """    Simulation des angewählten Programms starten    """
    print()  # print an blank line
    print("Starting the Program by triggering the electronic Finger")
    time.sleep(sleep_time)
    start_program()  # E-Finger press # TASTE_START_STOP.set_value
    time.sleep(sleep_time / 2)
    # print("Remaining Time: %d min " % ((global_ds_devicestate["RemainingTime"]) / 60))
    # print("Spinning Speed: %d rpm " % global_ds_devicestate["SpinningSpeed"])
    print("The Heat Actuator will be activated at pressure value of 30 mmWS")
    print()  # print an blank line

    A = False
    while not A:  # i == False while not i
        # NTC-Temperature ---------------------------------------------------
        global_cs_devicecontext = doper.get(st.GLOBAL_CS_DeviceContext)
        IstTemperature = global_cs_devicecontext["ServiceAttributesWM"]\
                                                ["NtcTemperature"]\
                                                ["CurrentValue"]
        print("NTC Temperature (Soll-Temp.) = %d°C" % IstTemperature)

        # Actuator ----------------------------------------------------------
        cdv_actuatorData = doper.get(st.CDV_ActuatorDat)
        Heater1 = cdv_actuatorData["Heater1"]["CurrentValue"]
        print(f"Heat Actuator (Engage ON/OFF) = {bool(Heater1)}")  # convert to boolean value

        # Water Level -------------------------------------------------------
        WaterLevel = global_cs_devicecontext["ServiceAttributesWM"]\
                                            ["WaterLevel"]\
                                            ["CurrentValue"]
        print("Ist Water Level = %d mmWS" % (WaterLevel / 10))  # convert to mmWS

        #  NTC Temperature -------------------------------------------------------
        if IstTemperature >= 25:
            print("NTC Temperature (Soll-Temp.) = %d°C" % IstTemperature)
            print(f"Heat Actuator (Engage ON/OFF) = {bool(Heater1)}")  # convert to boolean value
            print("Ist Water Level = %d mmWS" % (WaterLevel / 10))  # convert to mmWS
            A = True
    activate_pump(context)


@then("Assert the (?P<sensor>.+) (?P<status>.+) of (?P<value>.+) within (?P<period>.+) seconds")
def step_impl(context, sensor, status, value, period):
    print(value)  # (?P<temp>.+)

    """    Asserting the Temperature increase & Water level     """
    global_cs_devicecontext = doper.get(st.GLOBAL_CS_DeviceContext)
    context.global_ds_devicestate = global_cs_devicecontext
    WaterLevel = global_cs_devicecontext["ServiceAttributesWM"]\
                                        ["WaterLevel"]\
                                        ["CurrentValue"]
    IstTemperature = global_cs_devicecontext["ServiceAttributesWM"]\
                                            ["NtcTemperature"]\
                                            ["CurrentValue"]
    assert ((context.global_ds_devicestate["ServiceAttributesWM"]["WaterLevel"]["CurrentValue"])/10 == (WaterLevel/10))
    assert ((context.global_ds_devicestate["ServiceAttributesWM"]["NtcTemperature"]["CurrentValue"]) == IstTemperature)
    time.sleep(sleep_time/2)
    context.rec.stop()
    print()  # print an blank line
    print("Temperature increase of 3°C is asserted in 180 seconds")
    time.sleep(sleep_time/2)
    print()  # print an blank line
    print("The shutdown process for the physical model, software and simulation has started")
    print()  # print an blank line
    unplug(optical_interface)


@when("the Lye pump has been activated")
def activate_pump(context):
    """    :type context: behave.runner.Context    """
    activate_heat(context)


@then("Assert the WaterLevel Decrease of x mmWS within 300 seconds")
def assert_WaterLevel(context):
    """    :type context: behave.runner.Context    """