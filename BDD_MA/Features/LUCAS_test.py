from time import *
from functools import partial
import re
import datetime
import doper
from Process.Doper.ST import ST
from Process.Doper.BT import BT
__all__ = ["st", "bt", "doper", "sleep_time", "optical_interface", "conecting_time"]

"""Variables"""
sleep_time = 6
optical_interface = "OPT_TARGET"
conecting_time = 10000

"""DopX Umgebung aktivieren"""
st = ST()
bt = BT()


def get_heater_value():
    # cdv_actuatorData = doper.get(st.CDV_ActuatorDat)  # get the required variable form DopX interface
    # actuator = cdv_actuatorData["Heater1"]\
    #                            ["CurrentValue"]  # read out "Heating Actuator" value from DopX interface
    actuator = 40
    return actuator

def get_lye_pump_value():
    # cdv_actuatorData = doper.get(st.CDV_ActuatorDat)  # get the required variable form DopX interface
    # actuator = cdv_actuatorData["LyePump"]\
    #                            ["CurrentValue"]  # read out "Heating Actuator" value from DopX interface
    actuator = 30
    return actuator


# def get_pressure_mmWS_value():
#     # global_cs_devicecontext = doper.get(st.GLOBAL_CS_DeviceContext)  # get the required variable form DopX interface
#     # actuator = global_cs_devicecontext["ServiceAttributesWM"]\
#     #                                     ["WaterLevel"]\
#     #                                     ["CurrentValue"]  # read out "Heating Actuator" value from DopX interface
#     actuator = 20
#     return actuator


def get_value():
    dic = {"Heat_Actuator": get_heater_value(),
           "Lye_Pump_Actuator": get_lye_pump_value()}

    print(dic)
    return dic


def alan_test():
    value = get_value()
    print(value[actuator])
    assert value["Heat_Actuator"] == 40
    assert value["Lye_Pump_Actuator"] == False
    value["i do not exist"] ## KeyError
    assert value.get("i do not exist!", "Lucas ist cool") == "Lucas ist cool"

# assert wait_for(get_actuator, value=True, max_timeout_s=300), "Kein actuator wurde innerhalb von 5 min aktiviert"
# print(value[actuator_name])
# assert value.get("i do not exit!", "Lucas ist cool") == "Lucas ist cool"


if __name__ == "__main__":
    get_value()
    alan_test()