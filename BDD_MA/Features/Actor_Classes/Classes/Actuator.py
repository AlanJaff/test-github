from doper import build_optic_monitor_sky, build_optic_doper
from Process.Doper.ST import ST
from Process.Doper.BT import BT
from device import unplug
import time


class Actuator_template:
    actuator_name = None
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
    st = None
    bt = None
    doper = None
    DataInterface = None

    def __init__(self, actuator_name, condition):  # Initialization of (actuator_name, condition)
        self.actuator_name = actuator_name
        self.condition = condition
        """DopX Umgebung aktivieren"""
        self.st = ST()
        self.bt = BT()
        monitor = build_optic_monitor_sky(self.optical_interface)
        self.doper = build_optic_doper(rx_id=14, rx_unit=254, optic_monitor=monitor)
        self.getDataInterface()

    def getDataInterface(self):
        pass

    def step_impl(self):
        pass

    def get_actuator(self):
        pass

    " Check Actuator Connect -----------------------------------------------"
    " ----------------------------------------------------------------------"
    def connect(self, interface):  # check if required actuator is activated
        temp=0
        while not self.Engaged:
            Acquired_DataInterface = self.doper.get(self.DataInterface)  # DataInterface is overwritten
            actuator = Acquired_DataInterface[interface]["CurrentValue"]  # read out "Heat Actuator" status from DopX interface
            if not actuator:
                if temp == 0:
                    item ="{0} is not activated".format(self.actuator_name)
                    temp = 1
                else:
                    item = '.'
                print(item, sep=' ', end='', flush=True)
            if actuator:
                print(self.actuator_name, "is activated")
                self.Engaged = actuator

    " Check Actuator Disconnect --------------------------------------------"
    " ----------------------------------------------------------------------"
    def disconnect(self, interface):
        while self.Engaged:
            Acquired_DataInterface = self.doper.get(self.DataInterface)  # DataInterface is overwritten
            actuator = Acquired_DataInterface[interface]["CurrentValue"]  # read out "Heat Actuator" status from DopX interface
            if not actuator:
                print(self.actuator_name, "is not disconnected")
            if actuator:  # and self.condition
                print(self.actuator_name, "is disconnected")
                self.Engaged = actuator

    " Check Actuator Halt --------------------------------------------------"
    " ----------------------------------------------------------------------"
    def halted(self, interface):
        while not self.Engaged:
            Acquired_DataInterface = self.doper.get(self.DataInterface)  # DataInterface is overwritten
            actuator = Acquired_DataInterface[interface]["CurrentValue"]  # read out "Heat Actuator" status from DopX interface
            if not actuator:
                print(self.actuator_name, "is not halted")
            if actuator:
                print(self.actuator_name, "is halted")
                self.Engaged = actuator

    " Shutdown Routine -----------------------------------------------------"
    " ----------------------------------------------------------------------"
    def shutdown(self):
        time.sleep(self.sleep_time)
        self.context.rec.stop()
        unplug(self.optical_interface)
