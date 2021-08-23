# from time import *
# from functools import partial
# import re
import math
# import datetime
# import doper
# from Process.Doper.ST import ST
# from Process.Doper.BT import BT
# __all__ = ["st", "bt", "doper", "sleep_time", "optical_interface", "conecting_time"]
#
# """Variables"""
# sleep_time = 6
# optical_interface = "OPT_TARGET"
# conecting_time = 10000
#
# """DopX Umgebung aktivieren"""
# st = ST()
# bt = BT()
#
# def get_heater_value():
#     # cdv_actuatorData = doper.get(st.CDV_ActuatorDat)  # get the required variable form DopX interface
#     # actuator = cdv_actuatorData["Heater1"]\
#     #                            ["CurrentValue"]  # read out "Heating Actuator" value from DopX interface
#     actuator = False
#     return actuator
#
#
# def get_lye_pump_value():
#     # cdv_actuatorData = doper.get(st.CDV_ActuatorDat)  # get the required variable form DopX interface
#     # actuator = cdv_actuatorData["LyePump"]\
#     #                            ["CurrentValue"]  # read out "Heating Actuator" value from DopX interface
#     actuator = True
#     return actuator
#
# def get_actuator():
#     dictionary = {"Heat_Actuator": get_heater_value(),
#                   "Lye_Pump_Actuator": get_lye_pump_value()}
#     print()  # print a blank line
#     print("Dictionary = ", dictionary)
#     Heat_Actuator = True
#     print(Heat_Actuator)
#
#
#     for key, value in dictionary.items():
#
#         if Heat_Actuator == True:
#
#             try:
#                 print("%s = %s" % (key, value))  # print for True & False values
#                 if not value:
#                     raise NotImplementedError("is not activated")  # when dictionary does not have the value=True
#                 print(key, "is activated")  # print for only True values
#                 print(value)
#                 return value
#             except Exception as inactive:
#                 print(key, inactive)  # print the raise Error
#
# if __name__ == '__main__':
#     get_actuator()
import time
# startTime = time.monotonic()
# time.sleep(1)
# value = 3
# elapsed = "elapsed second"
# lauf = 3
# Temp = "Temperature"
# Inc = "Increase"
# x = True
# for seconds in range(1, lauf+1):
#     # print(round(int(time.monotonic()-startTime)), "seconds elapsed")  # print the current elapsed seconds
#     print("test " + (str(round(time.monotonic()-startTime))) + " " + elapsed)
#     time.sleep(1)
#
# print("Temperature Increase of %d°C achieved in %d seconds elapsed"
#       % (seconds, (time.monotonic()-startTime)))
#
#
# print(str(Temp) + "is asserted ")
# # print("Sensor_IstValue at " + round(int(time.monotonic()-startTime)) +
# #       " sec = " + self.Sensor_IstValue + "°C")  # print the actual_IstTemp.
#
# print("Temperature Increase of %d°C achieved in %d seconds elapsed" % (int(value), round(int(time.monotonic() - startTime))))  # print reached Temperature increase
# print(Temp + "  " + str(Inc) + " = " + str(value))
# # print("Sensor_IstValue at " + str(round(int(time.monotonic()-startTime))) +" sec = " + str(20) + "°C")  # print the actual_IstTemp.
#
# print(str(Temp) + " Status " + str(x))

Actuator_Register = {"Heat_Actuator": 1,
                     "Lye_Pump_Actuator": 2,
                     "Circulation_Pump_Actuator": 3,
                     "Water_Inlet_Valve": 4,
                     "Valve_CW_Actuator": 5,
                     "Valve_WW_Actuator": 6,
                     "Waterproof_Switch": 7}
bla=list(Actuator_Register.keys())
# print(bla)

import matplotlib.pyplot as plt

T = [17,18,19,20,21,22,23,24,25,26,27]
t = [0,4.6,11.20,12.125,41.15,23.39,19.625,17.76,19.6,19.67,19.6]
expect = 20

with open('data.txt','w') as f:
    _str = ''

    for i2, t2 in enumerate(T):
          _str += "%s," % t2
    _str += '\n'
    for i, t1 in enumerate(t):
        _str += "%s," % t1
    f.write(_str)

bars = []
T = T[1:]
t = t[1:]
for _, temp in enumerate(T):
    # bars.append("%d°C-%d°C" % (temp, temp-1))
    bars.append("(%d-%d)°C" % (temp, temp-1))

def plotcheck(T, t, expect = None):
    expect = [expect] * len(t)
    fig, ax = plt.subplots()
    plt.bar(T, t, width=0.4)
    ax.plot(T, expect, color='red')
    ax.set(xlabel='ΔT(T2-T1) [°C]', ylabel='Δt(T2-T1) [s]', title='Dynamisches Verhalten des Temperaturanstiegs')
    plt.xticks(T, bars, fontsize=6.5)
    ax.grid(True)
    fig.savefig("test.png")
    plt.legend(['Erwartungshaltung', 'Temperaturdifferenz'])
    plt.show()
# plt.plot( 'x', 'y1', data=df, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
plotcheck(T, t, expect)

def plotcheck_verlauf(T, t, expect = None):
    expect = [expect] * len(t)
    fig, ax = plt.subplots()
    # plt.bar(T, t, width=0.4)
    ax.plot(T, t, marker='o', markersize=6, linewidth=2)
    # ax.plot(T, t, linewidth=2, color='orange')
    ax.plot(T, expect, color='red')
    ax.set(xlabel='Temperaturen [°C]', ylabel='Zeit [s]', title='Dynamisches Verhalten der Temperaturen')
    plt.xticks(T)
    ax.grid(True)
    fig.savefig("test.png")
    plt.legend(['Temperaturen', 'Erwartungshaltung'])
    plt.show()
    # plt.xlabel(fontsize=10)
# plt.plot( 'x', 'y1', data=df, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
# plotcheck_verlauf(T, t, expect)
