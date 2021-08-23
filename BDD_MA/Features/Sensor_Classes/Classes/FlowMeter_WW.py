from .Sensor import Sensor_template


class FlowMeter_WarmWater_class(Sensor_template):
    interface = "VerbraucherVentilWW"

    def Increase(self, sensor, status, value, unit, period):
        # global_cdv_ProcessData = self.doper.get(self.st.CDV_ProcessData)  # get the required variable form DopX interface
        # self.Sensor_StartValue = global_cdv_ProcessData[self.interface]\
        #                                                ["CurrentValue"]
        self.compareAndWait(sensor, status, value, unit, period, self.interface)

    def Decrease(self, sensor, status, value, unit, period):
        # global_cdv_ProcessData = self.doper.get(self.st.CDV_ProcessData)  # get the required variable form DopX interface
        # self.Sensor_StartValue = global_cdv_ProcessData[self.interface]\
        #                                                ["CurrentValue"]
        self.compareAndWait(sensor, status, value, unit, period, self.interface)

    def getValueInterface(self):
        self.DataInterface = self.st.CDV_ProcessData
