from .Sensor import Sensor_template


class FlowMeter_ColdWater_class(Sensor_template):
    interface = "VerbraucherVentilKW"  # CDV_ProcessData

    def Increase(self, sensor, status, value, unit, period):
        # global_cdv_ProcessData = self.doper.get(self.st.CDV_ProcessData)  # get the required variable form DopX interface
        # self.Sensor_StartValue = global_cdv_ProcessData["VerbraucherVentilKW"]\
        #                                                ["CurrentValue"]
        self.compareAndWait(sensor, status, value, unit, period, self.interface)

    def Decrease(self, sensor, status, value, unit, period):
        # global_cdv_ProcessData = self.doper.get(self.st.CDV_ProcessData)  # get the required variable form DopX interface
        # self.Sensor_StartValue = global_cdv_ProcessData["VerbraucherVentilKW"]\
        #                                                ["CurrentValue"]
        self.compareAndWait(sensor, status, value, unit, period, self.interface)

    # def Below(self, sensor, status, value, unit):
    #
    #     self.verifyAndWait(self)
    #
    # def Above(self, sensor, status, value, unit):
    #
    #     self.verifyAndWait(self)

    def getValueInterface(self):
        self.DataInterface = self.st.CDV_ProcessData
