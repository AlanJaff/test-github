from doper import build_optic_monitor_sky, build_optic_doper
from Process.Doper.ST import ST
from Process.Doper.BT import BT
from device import unplug
import time


class Sensor_template:
    _all_ = ["st", "bt", "doper", "sleep_time", "optical_interface", "conecting_time", "msg"]
    """Variables"""
    sleep_time = 6
    optical_interface = "OPT_TARGET"
    conecting_time = 10000
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
    programmList = {'ProgramIds': [1, 133, 3, 146, 4, 23, 76, 149, 8, 37, 24, 50, 69, 122, 27, 29, 77, 9, 129, 39],
                    'ProgramMode': [3, 3, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                    'RemainingTime': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    'RemainingTimeMode1': [157, 184, 103, 49, 69, 69, 0, 0, 7, 15, 66, 88, 144, 5, 9, 58, 12, 10, 26,
                                           27],
                    'RemainingTimeMode2': [94, 0, 0, 0, 0, 0, 85, 40, 3, 0, 0, 0, 0, 0, 0, 0, 30, 3, 15, 15],
                    'RemainingTimeMode3': [247, 184, 103, 149, 69, 69, 0, 0, 10, 15, 66, 88, 144, 5, 9, 58, 42, 13, 45,
                                           46],
                    'ValidElements': 20}
    TimeCounter = 1800  # Time counter for 30 min
    sleep_time = 6  # Pause for 6 sec

    def __init__(self, context, sensor, status=None, value=None, unit=None, period=None):  # Initialization of (sensor and status)
        self.sensor = sensor
        self.status = status
        self.value = value
        self.unit = unit
        self.period = period
        self.context = context
        """DopX Umgebung aktivieren"""
        self.st = ST()
        self.bt = BT()
        monitor = build_optic_monitor_sky(self.optical_interface)
        self.doper = build_optic_doper(rx_id=14, rx_unit=254, optic_monitor=monitor)
        self.getValueInterface()

    def getValueInterface(self):
        pass

    " Lye Temperature Check ------------------------------------------------"
    " ----------------------------------------------------------------------"
    def compareAndWait_TempIncrease(self, sensor, status, value, unit, period, interface):
        startTime = time.monotonic()
        for seconds in range(1, self.TimeCounter + 1):
            # run time counter
            print()  # print a blank line
            print(round(time.monotonic()-startTime), "seconds elapsed")  # print the current elapsed seconds
            # Saving Sensor_IstValue ---------------------------------------------------
            Acquired_DataInterface = self.doper.get(self.DataInterface)  # DataInterface is overwritten
            Sensor_IstValue = Acquired_DataInterface["ServiceAttributesWM"]\
                                                    [self.interface]\
                                                    ["CurrentValue"]
            print("Sensor_IstValue = " + str(Sensor_IstValue) + str(self.unit))  # print Sensor_IstValue variable

            if round(int(time.monotonic()-startTime)) >= int(period):  # check if elapsed seconds equals to 180 sec
                print(time.monotonic()-startTime)  # print the actual seconds status
                if Sensor_IstValue - self.Sensor_StartValue >= int(value):  # check if the required increase is achieved
                    print("Sensor_StartValue at 0 sec = %d°C" % self.Sensor_StartValue)  # print the saved Sensor_StartValue
                    print("Sensor_IstValue = " + Sensor_IstValue + "°C")  # print the Sensor_IstValue
                    assert ((Acquired_DataInterface["ServiceAttributesWM"]\
                                                   [self.interface]\
                                                   ["CurrentValue"]) == self.Sensor_StartValue + int(value))  # assert Sensor_IstValue int(value)
                    print(time.monotonic()-startTime, "seconds elapsed")  # print the current elapsed seconds
                    print(str(self.sensor) + " " + str(self.status) + " of " + str(value) + str(unit) +
                          " achieved in " + str(round(time.monotonic() - startTime)) + " seconds")
                    print()  # print a blank line
                break

            elif abs(Sensor_IstValue - self.Sensor_StartValue) >= int(value):
                print()  # print a blank line
                print("Sensor_StartValue at 0 sec = " + str(self.Sensor_StartValue) + str(unit))  # print the saved Sensor_StartValue
                print("Sensor_IstValue at " + str(round(int(time.monotonic()-startTime))) +
                      " sec = " + str(Sensor_IstValue) + str(unit))  # print the Sensor_IstValue
                assert (Acquired_DataInterface["ServiceAttributesWM"]
                                              [self.interface]
                                              ["CurrentValue"] == self.Sensor_StartValue + int(value))
                print(str(self.sensor) + " " + str(self.status) + " of " + str(value) + str(unit) +
                      " achieved in " + str(round(time.monotonic()-startTime)) + " seconds")
                print()  # print a blank line
                break

    def compareAndWait_TempDecrease(self, sensor, status, value, unit, period, interface):
        startTime = time.monotonic()
        for seconds in range(1, self.TimeCounter + 1):  # run time counter
            print()  # print a blank line
            print(round(time.monotonic()-startTime), "seconds elapsed")  # print the current elapsed seconds
            # Saving Sensor_IstValue ---------------------------------------------------
            Acquired_DataInterface = self.doper.get(self.DataInterface)  # DataInterface is overwritten
            Sensor_IstValue = Acquired_DataInterface["ServiceAttributesWM"]\
                                                    [self.interface]\
                                                    ["CurrentValue"]
            print("Sensor_IstValue = " + str(Sensor_IstValue) + str(unit))  # print Sensor_IstValue variable

            if round(int(time.monotonic()-startTime)) >= int(period):  # check if elapsed seconds equals to 180 sec
                print(time.monotonic()-startTime)  # print the actual seconds status
                if abs(Sensor_IstValue - self.Sensor_StartValue) >= int(value):  # check if the required increase is achieved
                    print("Sensor_StartValue at 0 sec = %d°C" % self.Sensor_StartValue)  # print the saved Sensor_StartValue
                    print("Sensor_IstValue = " + Sensor_IstValue + "°C")  # print the Sensor_IstValue
                    assert ((Acquired_DataInterface["ServiceAttributesWM"]\
                                                   [self.interface]\
                                                   ["CurrentValue"]) == self.Sensor_StartValue + int(value))  # assert Sensor_IstValue int(value)
                    print(time.monotonic()-startTime, "seconds elapsed")  # print the current elapsed seconds
                    print(str(self.sensor) + " " + str(self.status) + " of " + str(value) + str(unit) +
                          " achieved in " + str(round(time.monotonic() - startTime)) + " seconds")
                    print()  # print a blank line
                break

            elif abs(Sensor_IstValue - self.Sensor_StartValue) >= int(value):
                print()  # print a blank line
                print("Sensor_StartValue at 0 sec = " + str(self.Sensor_StartValue) + str(unit))  # print the saved Sensor_StartValue
                print("Sensor_IstValue at " + str(round(int(time.monotonic()-startTime))) +
                      " sec = " + str(Sensor_IstValue) + str(unit))  # print the Sensor_IstValue
                assert (Acquired_DataInterface["ServiceAttributesWM"]
                                              [self.interface]
                                              ["CurrentValue"] == self.Sensor_StartValue + int(value))
                print(str(self.sensor) + " " + str(self.status) + " of " + str(value) + str(unit) +
                      " achieved in " + str(round(time.monotonic() - startTime)) + " seconds")
                print()  # print a blank line
                break

    def compareAndWait_TempDifference(self, sensor, status, value, unit, period, interface):
        startTime = time.monotonic()
        for seconds in range(1, self.TimeCounter + 1):  # run time counter
            print()  # print a blank line
            print(round(time.monotonic()-startTime), "seconds elapsed")  # print the current elapsed seconds
            # Saving Sensor_IstValue ---------------------------------------------------
            Acquired_DataInterface = self.doper.get(self.DataInterface)  # DataInterface is overwritten
            Sensor_IstValue = Acquired_DataInterface["ServiceAttributesWM"]\
                                                    [self.interface]\
                                                    ["CurrentValue"]
            print("Sensor_IstValue = " + str(Sensor_IstValue) + str(unit))  # print Sensor_IstValue variable

            if round(int(time.monotonic()-startTime)) >= int(period):  # check if elapsed seconds equals to 180 sec
                print(time.monotonic()-startTime)  # print the actual seconds status
                if abs(Sensor_IstValue - self.Sensor_StartValue) >= int(value):  # check if the required increase is achieved
                    print("Sensor_StartValue at 0 sec = %d°C" % self.Sensor_StartValue)  # print the saved Sensor_StartValue
                    print("Sensor_IstValue = " + Sensor_IstValue + "°C")  # print the Sensor_IstValue
                    assert ((Acquired_DataInterface["ServiceAttributesWM"]\
                                                   [self.interface]\
                                                   ["CurrentValue"]) == self.Sensor_StartValue + int(value))  # assert Sensor_IstValue int(value)
                    print(time.monotonic()-startTime, "seconds elapsed")  # print the current elapsed seconds
                    print(str(self.sensor) + " " + str(self.status) + " of " + str(value) + str(unit) +
                          " achieved in " + str(round(time.monotonic() - startTime)) + " seconds")
                    print()  # print a blank line
                break

            elif abs(Sensor_IstValue - self.Sensor_StartValue) >= int(value):
                print()  # print a blank line
                print("Sensor_StartValue at 0 sec = " + str(self.Sensor_StartValue) + str(unit))  # print the saved Sensor_StartValue
                print("Sensor_IstValue at " + str(round(int(time.monotonic()-startTime))) +
                      " sec = " + str(Sensor_IstValue) + str(unit))  # print the Sensor_IstValue
                assert (Acquired_DataInterface["ServiceAttributesWM"]
                                              [self.interface]
                                              ["CurrentValue"] == self.Sensor_StartValue + int(value))
                print(str(self.sensor) + " " + str(self.status) + " of " + str(value) + str(unit) +
                      " achieved in " + str(round(time.monotonic()-startTime)) + " seconds")
                print()  # print a blank line
                break

    def verifyAndWait_TempAbove(self, sensor, status, value, unit, period):
        startTime = time.monotonic()
        for seconds in range(1, self.TimeCounter + 1):  # run time counter
            print()  # print a blank line
            print(round(time.monotonic()-startTime), "seconds elapsed")  # print the current elapsed seconds
            # Saving Sensor_IstValue ---------------------------------------------------
            Acquired_DataInterface = self.doper.get(self.DataInterface)  # DataInterface is overwritten
            Sensor_IstValue = Acquired_DataInterface["ServiceAttributesWM"] \
                                                    [self.interface] \
                                                    ["CurrentValue"]
            print("Sensor_IstValue = " + str(Sensor_IstValue) + str(self.unit))  # print Sensor_IstValue variable
            print()  # print a blank line

            if round(int(time.monotonic()-startTime)) >= int(period):  # check if elapsed seconds equals to 180 sec
                if Sensor_IstValue >= int(value):
                    print("Sensor_IstValue at " + str(round(int(time.monotonic() - startTime))) +
                          " sec = " + str(Sensor_IstValue) + str(unit))  # print the Sensor_IstValue
                    assert (Acquired_DataInterface["ServiceAttributesWM"]
                                                  [self.interface]
                                                  ["CurrentValue"] == int(value))
                    print(str(self.sensor) + " " + str(self.status) + " of " + str(value) + str(unit) +
                          " achieved in " + str(round(time.monotonic()-startTime)) + " seconds")
                    print()  # print a blank line
                    break
            elif Sensor_IstValue >= int(value):
                print("Sensor_StartValue at 0 sec = " + str(self.Sensor_StartValue) + str(unit))  # print the saved Sensor_StartValue
                print("Sensor_IstValue at " + str(round(int(time.monotonic() - startTime))) +
                      " sec = " + str(Sensor_IstValue) + str(unit))  # print the Sensor_IstValue
                assert (Acquired_DataInterface["ServiceAttributesWM"]
                                              [self.interface]
                                              ["CurrentValue"] == int(value))
                print(str(self.sensor) + " " + str(self.status) + " of " + str(value) + str(unit) +
                      " achieved in " + str(round(time.monotonic()-startTime)) + " seconds")
                print()  # print a blank line
                break

    def verifyAndWaite_TempBelow(self, sensor, status, value, unit, period):
        startTime = time.monotonic()
        for seconds in range(1, self.TimeCounter + 1):  # run time counter
            print()  # print a blank line
            print(round(time.monotonic()-startTime), "seconds elapsed")  # print the current elapsed seconds
            # Saving Sensor_IstValue ---------------------------------------------------
            Acquired_DataInterface = self.doper.get(self.DataInterface)  # DataInterface is overwritten
            Sensor_IstValue = Acquired_DataInterface["ServiceAttributesWM"]\
                                                    [self.interface]\
                                                    ["CurrentValue"]
            print("Sensor_IstValue = " + str(Sensor_IstValue) + str(unit))  # print Sensor_IstValue variable
            if round(int(time.monotonic()-startTime)) >= int(period):  # check if elapsed seconds equals to 180 sec
                if Sensor_IstValue <= int(value):
                    print("Sensor_IstValue at " + str(round(int(time.monotonic() - startTime))) +
                          " sec = " + str(Sensor_IstValue) + str(unit))  # print the Sensor_IstValue
                    assert (Acquired_DataInterface["ServiceAttributesWM"]
                                                  [self.interface]
                                                  ["CurrentValue"] == Sensor_IstValue)
                    print(str(self.sensor) + " " + str(self.status) + " of " + str(value) + str(unit) +
                          " achieved in " + str(round(time.monotonic() - startTime)) + " seconds")
                    print()  # print a blank line
                    break
            elif Sensor_IstValue <= int(value):
                print("Sensor_IstValue at " + str(round(int(time.monotonic() - startTime))) +
                      " sec = " + str(Sensor_IstValue) + str(unit))  # print the Sensor_IstValue
                assert (Acquired_DataInterface["ServiceAttributesWM"]
                                              [self.interface]
                                              ["CurrentValue"] == Sensor_IstValue)
                print(str(self.sensor) + " " + str(self.status) + " of " + str(value) + str(unit) +
                      " achieved in " + str(round(time.monotonic()-startTime)) + " seconds")
                print()  # print a blank line
                break

    def controlAndWait(self, sensor, soll, unit, expect):
        startTime = time.monotonic()
        startime = None
        startTemp = None
        lastTempStamp = None
        T = []  # Temp. values
        t = []  # time stamps
        while True:
            print()  # print a blank line
            print(round(time.monotonic() - startTime), "seconds elapsed")  # print the current elapsed seconds
            # Saving Sensor_IstValue ---------------------------------------------------
            Acquired_DataInterface = self.doper.get(self.DataInterface)  # DataInterface is overwritten
            Sensor_IstValue = Acquired_DataInterface["ServiceAttributesWM"]\
                                                    [self.interface]\
                                                    ["CurrentValue"]
            if startTemp is None:  # == None
                startime = startTime
                startTemp = Sensor_IstValue
                T.append(startTemp)
                t.append(0)
                print("Sensor_StartValue = " + str(Sensor_IstValue) + str(unit))  # print Sensor_IstValue variable

            else:
                print("Sensor_IstValue = " + str(Sensor_IstValue) + str(unit))  # print Sensor_IstValue variable
                if lastTempStamp != Sensor_IstValue and lastTempStamp != None:
                    if abs(lastTempStamp - Sensor_IstValue) >= int(expect[0]):  # .. >= 1°C
                        newTime = time.monotonic()
                        T.append(Sensor_IstValue)  # append Temp. values to Temp. list
                        elapsedTime = newTime-startime  # calculate time difference between Temperatures
                        t.append(elapsedTime)  # append time stamps to time list
                        startime = newTime  # set a new time stamp
                        _str = "from {0}°C to {1}°C in {2} sec".format(Sensor_IstValue-1, Sensor_IstValue, elapsedTime)
                        print(_str)
                        if elapsedTime > int(expect[1]):  # actual elapsed time >= 20 sec
                            print("NOT EXPECTED DYNAMIC BEHAVIOUR")

                if abs(Sensor_IstValue) >= int(soll):
                    print()  # print a blank line
                    print("Sensor_StartValue at 0 sec = " + str(self.Sensor_StartValue) + str(unit))  # print the saved Sensor_StartValue
                    print("Sensor_IstValue at " + str(round(int(time.monotonic() - startTime))) +
                          " sec = " + str(Sensor_IstValue) + str(unit))  # print the Sensor_IstValue
                    print(sensor)
                    print(soll)
                    print(unit)
                    print(expect)
                    print(Acquired_DataInterface["ServiceAttributesWM"]
                                                [self.interface]
                                                ["CurrentValue"])
                    assert (Acquired_DataInterface["ServiceAttributesWM"]
                                                             [self.interface]
                                                             ["CurrentValue"] == int(soll))
                    print(str(self.sensor) + " of " + str(soll) + str(unit) +
                          " achieved in " + str(round(time.monotonic() - startTime)) + " seconds")
                    print()  # print a blank line
                    return T, t
            lastTempStamp = Sensor_IstValue

    " Water Level Check ----------------------------------------------------"
    " ----------------------------------------------------------------------"
    def compareAndWait_WL_Increase(self, sensor, status, value, unit, period):
        startTime = time.monotonic()
        for seconds in range(1, self.TimeCounter + 1):  # run time counter
            print()  # print a blank line
            print(round(time.monotonic()-startTime), "seconds elapsed")  # print the current elapsed seconds
            Acquired_DataInterface = self.doper.get(self.DataInterface)  # DataInterface is overwritten
            Sensor_IstValue = round((Acquired_DataInterface["ServiceAttributesWM"]\
                                                           [self.interface]\
                                                           ["CurrentValue"]) / 10)
            print("Sensor_IstValue = " + str(Sensor_IstValue) + str(self.unit))  # print Sensor_IstValue variable

            if round(int(time.monotonic()-startTime)) >= int(self.period):  # check if elapsed seconds equals to 180 sec
                print(time.monotonic()-startTime)  # print the actual seconds status
                if round(self.Sensor_StartValue) - round(Sensor_IstValue) <= int(self.value):
                    print("Sensor_StartValue at 0 sec = %d°C" % round(self.Sensor_StartValue))  # print the saved Sensor_StartValue
                    print("Sensor_IstValue after = " + str(round(Sensor_IstValue)) + "°C")  # print the Sensor_IstValue
                    assert (round(Acquired_DataInterface["ServiceAttributesWM"]
                                                        [self.interface]
                                                        ["CurrentValue"]/10) == round(Sensor_IstValue))  # assert Sensor_IstValue int(value)
                    print(time.monotonic()-startTime, "seconds elapsed")  # print the current elapsed seconds
                    print(str(self.sensor) + " " + str(self.status) + " of " + str(self.value) + " " + str(self.unit) +
                          " achieved in " + str(round(time.monotonic() - startTime)) + " seconds")
                    print()  # print a blank line
                break
            elif round(self.Sensor_StartValue) - round(Sensor_IstValue) <= int(self.value):
                print()  # print a blank line
                print("Sensor_StartValue at 0 sec = " + str(self.Sensor_StartValue) + str(unit))  # print the saved Sensor_StartValue
                print("Sensor_StartValue at 0 sec = " + str(round(self.Sensor_StartValue)) + " " + str(self.unit))  # print the saved Sensor_StartValue
                print("Sensor_IstValue at " + str(round(int(time.monotonic()-startTime))) +
                      " sec = " + str(round(Sensor_IstValue)) + str(self.unit))  # print the Sensor_IstValue
                assert (round(Acquired_DataInterface["ServiceAttributesWM"]
                                                    [self.interface]
                                                    ["CurrentValue"]/10) == round(Sensor_IstValue))
                print(str(self.sensor) + " " + str(self.status) + " of " + str(self.value) + " " + str(self.unit) +
                      " achieved in " + str(round(time.monotonic() - startTime)) + " seconds")
                print()  # print a blank line
                break

    def compareAndWait_WL_Decrease(self, sensor, status, value, unit, period):
        startTime = time.monotonic()
        for seconds in range(1, self.TimeCounter + 1):  # run time counter
            print()  # print a blank line
            print(round(time.monotonic()-startTime), "seconds elapsed")  # print the current elapsed seconds
            Acquired_DataInterface = self.doper.get(self.DataInterface)  # DataInterface is overwritten
            Sensor_IstValue = round(Acquired_DataInterface["ServiceAttributesWM"]\
                                                           [self.interface]\
                                                           ["CurrentValue"] / 10)
            print("Sensor_IstValue = " + str(round(Sensor_IstValue)) + " " + str(self.unit))  # print Sensor_IstValue variable

            if round(int(time.monotonic()-startTime)) >= int(self.period):  # check if elapsed seconds equals to 180 sec
                print(time.monotonic()-startTime)  # print the actual seconds status
                if round(self.Sensor_StartValue) - round(Sensor_IstValue) >= int(self.value):
                    print("Sensor_StartValue at 0 sec = %d°C" % round(self.Sensor_StartValue))  # print the saved Sensor_StartValue
                    print("Sensor_IstValue after = " + str(round(Sensor_IstValue)) + "°C")  # print the Sensor_IstValue
                    assert (round(Acquired_DataInterface["ServiceAttributesWM"]
                                                         [self.interface]
                                                         ["CurrentValue"]/10) == round(Sensor_IstValue))  # assert Sensor_IstValue int(value)
                    print(time.monotonic()-startTime, "seconds elapsed")  # print the current elapsed seconds
                    print(str(self.sensor) + " " + str(self.status) + " of " + str(self.value) + str(self.unit) +
                          " achieved in " + str(round(time.monotonic() - startTime)) + " seconds")
                    print()  # print a blank line
                break
            elif round(self.Sensor_StartValue) - round(Sensor_IstValue) >= int(self.value):
                print()  # print a blank line
                print("Sensor_StartValue at 0 sec = " + str(round(self.Sensor_StartValue)) + " " + str(self.unit))  # print the saved Sensor_StartValue
                print("Sensor_IstValue at " + str(round(int(time.monotonic()-startTime))) +
                      " sec = " + str(round(Sensor_IstValue)) + str(self.unit))  # print the Sensor_IstValue
                assert (round(Acquired_DataInterface["ServiceAttributesWM"]
                                              [self.interface]
                                              ["CurrentValue"]/10) == round(Sensor_IstValue))
                print(str(self.sensor) + " " + str(self.status) + " of " + str(self.value) + " " + str(self.unit) +
                      " achieved in " + str(round(time.monotonic() - startTime)) + " seconds")
                print()  # print a blank line
                break

    def compareAndWait_WL_Difference(self, sensor, status, value, unit, period):
        startTime = time.monotonic()
        for seconds in range(1, self.TimeCounter + 1):  # run time counter
            print()  # print a blank line
            print(round(time.monotonic()-startTime), "seconds elapsed")  # print the current elapsed seconds
            Acquired_DataInterface = self.doper.get(self.DataInterface)  # DataInterface is overwritten
            Sensor_IstValue = round(Acquired_DataInterface["ServiceAttributesWM"]\
                                                           [self.interface]\
                                                           ["CurrentValue"] / 10)

            if round(int(time.monotonic()-startTime)) >= int(self.period):  # check if elapsed seconds equals to 180 sec
                print(time.monotonic()-startTime)  # print the actual seconds status
                if abs(round(self.Sensor_StartValue) - round(Sensor_IstValue)) >= int(self.value):
                    print("Sensor_StartValue at 0 sec = %d°C" % round(self.Sensor_StartValue))  # print the saved Sensor_StartValue
                    print("Sensor_IstValue after = " + str(round(Sensor_IstValue)) + "°C")  # print the Sensor_IstValue
                    assert (round(Acquired_DataInterface["ServiceAttributesWM"]
                                                   [self.interface]
                                                   ["CurrentValue"]/10) == round(Sensor_IstValue))  # assert Sensor_IstValue int(value)
                    print(time.monotonic()-startTime, "seconds elapsed")  # print the current elapsed seconds
                    print(str(self.sensor) + " " + str(self.status) + " of " + str(self.value) + " " + str(self.unit) +
                          " achieved in " + str(round(time.monotonic() - startTime)) + " seconds")
                    print()  # print a blank line
                break
            elif abs(round(self.Sensor_StartValue) - round(Sensor_IstValue)) >= int(self.value):
                print()  # print a blank line
                print("Sensor_StartValue at 0 sec = " + str(round(self.Sensor_StartValue)) + str(self.unit))  # print the saved Sensor_StartValue
                print("Sensor_IstValue at " + str(round(int(time.monotonic()-startTime))) +
                      " sec = " + str(round(Sensor_IstValue)) + " " + str(self.unit))  # print the Sensor_IstValue
                assert (round(Acquired_DataInterface["ServiceAttributesWM"]
                                              [self.interface]
                                              ["CurrentValue"]/10) == round(Sensor_IstValue))
                print(str(self.sensor) + " " + str(self.status) + " of " + str(self.value) + " " + str(self.unit) +
                      " achieved in " + str(round(time.monotonic() - startTime)) + " seconds")
                print()  # print a blank line
                break

    def verifyAndWait_WL_Above(self, sensor, status, value, unit, period):
        startTime = time.monotonic()
        for seconds in range(1, self.TimeCounter + 1):  # run time counter
            print()  # print a blank line
            print(round(time.monotonic()-startTime), "seconds elapsed")  # print the current elapsed seconds
            # Saving Sensor_IstValue ---------------------------------------------------
            Acquired_DataInterface = self.doper.get(self.DataInterface)  # DataInterface is overwritten
            Sensor_IstValue = round(Acquired_DataInterface["ServiceAttributesWM"]\
                                                           [self.interface]\
                                                           ["CurrentValue"] / 10)
            print("Sensor_IstValue = " + str(round(Sensor_IstValue)) + " " + str(self.unit))  # print Sensor_IstValue variable
            print()  # print a blank line
            if round(int(time.monotonic()-startTime)) >= int(self.period):  # check if elapsed seconds equals to 180 sec
                if round(Sensor_IstValue) >= int(self.value):
                    print("Sensor_IstValue at " + str(round(int(time.monotonic() - startTime))) +
                          " sec = " + str(round(Sensor_IstValue)) + " " + str(self.unit))  # print the Sensor_IstValue
                    assert (round(Acquired_DataInterface["ServiceAttributesWM"]
                                                        [self.interface]
                                                        ["CurrentValue"] / 10) == int(self.value))
                    print(str(self.sensor) + " " + str(self.status) + " of " + str(self.value) + str(self.unit) +
                          " is achieved in " + str(round(time.monotonic()-startTime)) + " seconds")
                    print()  # print a blank line
                    break
            elif round(Sensor_IstValue) >= int(self.value):
                print("Sensor_StartValue at 0 sec = " + str(self.Sensor_StartValue) + str(unit))  # print the saved Sensor_StartValue
                print("Sensor_IstValue at " + str(round(int(time.monotonic() - startTime))) +
                      " sec = " + str(round(Sensor_IstValue)) + " " + str(self.unit))  # print the Sensor_IstValue
                assert (round(Acquired_DataInterface["ServiceAttributesWM"]
                                                    [self.interface]
                                                    ["CurrentValue"]/10) == int(self.value))
                print(str(self.sensor) + " " + str(self.status) + " of " + str(self.value) + " " + str(self.unit) +
                      " is achieved in " + str(round(time.monotonic()-startTime)) + " seconds")
                print()  # print a blank line
                break

    def verifyAndWait_WL_Below(self, sensor, status, value, unit, period):
        startTime = time.monotonic()
        for seconds in range(1, self.TimeCounter + 1):  # run time counter
            print()  # print a blank line
            print(round(time.monotonic()-startTime), "seconds elapsed")  # print the current elapsed seconds
            # Saving Sensor_IstValue ---------------------------------------------------
            Acquired_DataInterface = self.doper.get(self.DataInterface)  # DataInterface is overwritten
            Sensor_IstValue = round(Acquired_DataInterface["ServiceAttributesWM"]\
                                                    [self.interface]\
                                                    ["CurrentValue"] / 10)
            print("Sensor_IstValue = " + str(Sensor_IstValue) + " " + str(self.unit))  # print Sensor_IstValue variable
            print()  # print a blank line
            if round(int(time.monotonic()-startTime)) >= int(self.period):  # check if elapsed seconds equals to 180 sec
                if Sensor_IstValue <= int(self.value):
                    print("Sensor_IstValue at " + str(round(int(time.monotonic() - startTime))) +
                          " sec = " + str(Sensor_IstValue) + " " + str(self.unit))  # print the Sensor_IstValue
                    assert (round(Acquired_DataInterface["ServiceAttributesWM"]
                                                        [self.interface]
                                                        ["CurrentValue"] / 10) == round(Sensor_IstValue))
                    print(str(self.sensor) + " " + str(self.status) + " of " + str(self.value) + " " + str(self.unit) +
                          " is achieved in " + str(round(time.monotonic()-startTime)) + " seconds")
                    print()  # print a blank line
                    break
            elif Sensor_IstValue <= int(self.value):
                print("Sensor_IstValue at " + str(round(int(time.monotonic() - startTime))) +
                      " sec = " + str(Sensor_IstValue) + " " + str(self.unit))  # print the Sensor_IstValue
                assert (round(Acquired_DataInterface["ServiceAttributesWM"]
                                                    [self.interface]
                                                    ["CurrentValue"]/10) == round(Sensor_IstValue))
                print(str(self.sensor) + " " + str(self.status) + " of " + str(self.value) + " " + str(self.unit) +
                      " is achieved in " + str(round(time.monotonic()-startTime)) + " seconds")
                print()  # print a blank line
                break

    " Shutdown Routine -----------------------------------------------------"
    " ----------------------------------------------------------------------"
    def shutdown(self):
        time.sleep(self.sleep_time)
        self.context.rec.stop()
        unplug(self.optical_interface)
