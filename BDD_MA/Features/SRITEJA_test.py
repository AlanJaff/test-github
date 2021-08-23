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
#
# print("Start time")
# start_time = time.time()
# print(start_time)
# stopper = input("press enter to stop")
# end_time = time.time()
# print("you have finished")
# print(end_time)
# print("-----------------------------")
# duration = int(end_time - start_time)
# print("%s seconds" % duration)
#
# if duration > 3:
#     print("too slow")
# else:
#     print("well done")

# ----------------------------------------------------------------------------------------
# TimeCounter = int(input("how many seconds do you want to count to?"))

# TimeCounter = 10
# for x in range(1, TimeCounter+1):
#     print(x, "seconds elapsed")
#     sleep(1)
# ----------------------------------------------------------------------------------------

# time_stop = datetime.datetime.now()
# print(time_stop)
# sleep(3)
# timeStop = str(datetime.datetime.now())
# print(timeStop)
# ----------------------------------------------------------------------------------------
#  Heater1 from CDV_ActuatorDat --------------------------------------------
# cdv_actuatorData = doper.get(st.CDV_ActuatorDat)
# print("Heater Element (Engage ON/OFF): %d " % cdv_actuatorData["Heater1"]["CurrentValue"])
#  NTC Temperature from CDV_SensorData --------------------------------------------
# cdv_sensorData = doper.get(st.CDV_SensorData)
# print("Sensor NTC Temperature: %d° C" % cdv_sensorData["NtcTemperature1"]["CurrentValue"])
#  NTC Temperature from GLOBAL_CS_DeviceContext --------------------------------------------
# global_cs_devicecontext = doper.get(st.GLOBAL_CS_DeviceContext)
# print("NTC Temperature (IstTemp.): %d° C" % global_cs_devicecontext["ServiceAttributesWM"]["NtcTemperature"]["CurrentValue"])
#  Variables from CDV_ProcessData --------------------------------------------
# cdv_ProcessData = doper.get(st.CDV_ProcessData)
# print("Ist Restlaufzeit: %d min" % cdv_ProcessData["IstRestlaufzeitMinuten"]["CurrentValue"])
# print("Ist Niveau: %d " % cdv_ProcessData["IstNiveau"]["CurrentValue"])
# print("MaxProgrammDuration = %d " % global_ps_context["ProgAttributesDWTDWM"]["MaxProgrammDuration"])
#  Variables from GLOBAL_CS_Context --------------------------------------------
# global_cs_context = doper.get(st.GLOBAL_CS_Context)
# print("ServiceContextDWTDWM: %d " % global_cs_context["ServiceContextDWTDWM"]["OnOff"]["CurrentValue"])

# a = True
# heater = bool(a)
# print("status", a)

# ---------------------------------------------------------------------------------
# import time
#
# def wait_until(somepredicate, timeout=5, period=0.25, *args, **kwargs):
#   mustend = time.time() + timeout
#   while time.time() < mustend:
#     if somepredicate(*args, **kwargs): return True
#     time.sleep(period)
#   return False
# wait_until(somepredicate, timeout=5, period=0.25, *args, **kwargs1)

# ---------------------------------------------------------------------------------
# txt = "The rain in Spain"
# x = re.search("^The.*Spain$", txt)
# x2 = re.findall("Portugal", txt)
# print(x2)
#
# if x2:
#     print("Yes, we have a match")
#     print(txt)
# else:
#     print("no match")
# ---------------------------------------------------------------------------------

# string1 = "June 15, 1987"
# regex = r"^(?P<month>\w+)\s(?P<day>\d+)\,?\s(?P<year>\d+)"
#
# matches= re.search(regex, string1)
#
# print("Month: ", matches.group('month'))
# print("Day: ", matches.group('day'))
# print("Year: ", matches.group('year'))
# ---------------------------------------------------------------------------------
# from functools import partial
# import time
#
# def wait_for(get_func, value=True, max_timeout_s=10, sleep_time_s=0.1):
#     """Wait on get_func returning the expected value [default: True]
#
#     :param get_func: Method or Function
#     :param value: same as rtype of get_func
#     :param sleep_time_s: Zeit, die zwischen zwei Funktionsaufrufen gewartet wird
#     :type max_timeout_s: int, float
#     :return: True, wenn der Wert erreicht wurde
#     :rtype: bool"""
#
#     nop = lambda: None
#     sleeper = nop if max_timeout_s <= 1.0 else partial(time.sleep, sleep_time_s)
#     start = time.perf_counter()
#     while start + max_timeout_s > time.perf_counter():
#         if value == get_func():
#             return True
#         sleeper()
#     return False
# wait_for(get_func=True, value=True, max_timeout_s=10, sleep_time_s=0.1)
# _unused = object()


# def get_func():
#     return True
# print(get_func())

# ---------------------------------------------------------------------------------
# def func(a=2, b=6, c=None):
#     print("A=", a)
#     print("B=", b)
#     print("C=",c)
#     val = a*b
#     return val, a, b, c
# wert, a, b, c = func(3, 12, 4)
# print(wert, a, b, c)
# ---------------------------------------------------------------------------------
# def foo(a, b, *args, **kwargs):
#     # print(a, b)
#     for arg in args:
#         print(arg)
#     for key in kwargs:
#         print(key, kwargs[key])
# foo(1, 2, 3, 4, 5, six=6, seven=7)
# ---------------------------------------------------------------------------------
# import time
# start = time.perf_counter()
# def do_something():
#     print("Sleeping 5 seconds...")
#     time.sleep(5)
#     print("done sleeping")
# do_something()
# finish = time.perf_counter()
# print(f"finished in {round(finish-start, 2)} second(s)")
# ---------------------------------------------------------------------------------
# predicate = lambda : True
# from waiting import wait, TimeoutExpired
# predicate = "test"
# wait(predicate, timeout_seconds = 10.5)
# print(predicate)
# ---------------------------------------------------------------------------------
# DICTIONARY ##########################################

# student = {"name": "Dan", "age": 32, "courses": ["MAth", "CompSci"], "phone": "444-4444"}
# print(student.get("location", "not found"))

# # student["name"] = "Marwa"  # update name
# # print(student)
# # student.update({"name": "Jane"})
# # print(student)
# # print(student["name"], student["age"])
# # print(student.get("name"))
# # print(student.get("phone", "not found"))
#
# # del student["age"]
# # print(student)
# # age = student.pop("age")
# # print(age)
# # print(len(student))  # how many keys
# # print(student.keys())
# # print((student.values()))
# # print(student.items())
# print(type(student))  # show which class type
#
# for key, value in student.items():
#     print(key, value)
#
# student2 = dict(name="Alan",age= 30)
# print(student2)
# try:
#     print(student2["Uni"])
# except KeyError:
#     print("no uni is given")
#
# print(dir(student2))  # list of available methods
# ---------------------------------------------------------------------------------

def get_heater_value():
    # cdv_actuatorData = doper.get(st.CDV_ActuatorDat)  # get the required variable form DopX interface
    # actuator = cdv_actuatorData["Heater1"]["CurrentValue"]  # read out "Heating Actuator" value from DopX interface
    actuator = True
    return actuator


def get_lye_pump_value():
    # cdv_actuatorData = doper.get(st.CDV_ActuatorDat)  # get the required variable form DopX interface
    # actuator = cdv_actuatorData["LyePump"]\
    #                            ["CurrentValue"]  # read out "Heating Actuator" value from DopX interface
    actuator = False
    return actuator

# def get_pressure_mmWS_value():
#     # global_cs_devicecontext = doper.get(st.GLOBAL_CS_DeviceContext)
#     # actuator = global_cs_devicecontext["ServiceAttributesWM"]\
#     #                                     ["WaterLevel"]\
#     #                                     ["CurrentValue"]
#     actuator = 30
#     return actuator


dictionary = {"Heat_Actuator": get_heater_value(),
             "Lye_Pump_Actuator": get_lye_pump_value()}
print(dictionary)


def get_actuator():
    for key, value in dictionary.items():
        try:
            if not value:
                raise NotImplementedError("Actuator is not defined: " + key)  # when dictionary does not have the value
            print(value)  # for True values
            return value
        except Exception as e:
            print(e)  # for False values


if __name__ == '__main__':
    get_actuator()

# def step(actuator):
#     dictionary.get(actuator, None)
#     print(actuator)

# dictionary = Heat_Actuator :  25, Lye_Pump: 40 , Water_Level: 30
# dictio = {"Lye_Pump": 44}
# print(dictio)
# print(dictio.get("Lye_Pump"))
# getter = dictio.get("Lye_Pump", None)
# if getter:
#     print("achieved")
# if getter is None:
#     raise NotImplementedError("Actuator is not defined")
# for key, value in dictio.items():
#     print(key, value)

# for key, value in dictionary.items():
#     value_getter = value()
#     if value_getter is None:
#         raise NotImplementedError("Actuator is not defined")  # when the dictionary does not have the value
#     value = value_getter
#     print(value_getter)
