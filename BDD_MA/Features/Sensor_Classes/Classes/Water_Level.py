from .Sensor import Sensor_template


class Water_Level_class(Sensor_template):
    interface = "WaterLevel"

    def Increase(self, sensor, status, value, unit, period):
        global_cs_devicecontext = self.doper.get(self.st.GLOBAL_CS_DeviceContext)  # get the required variable form DopX interface
        self.Sensor_StartValue = (round(global_cs_devicecontext["ServiceAttributesWM"]\
                                                        [self.interface]\
                                                        ["CurrentValue"])) / 10
        print("Sensor_StartValue = " + str(round(self.Sensor_StartValue)) + " mmWS")
        self.compareAndWait_WL_Increase(self, sensor, status, value, unit)

    def Decrease(self, sensor, status, value, unit, period):
        global_cs_devicecontext = self.doper.get(self.st.GLOBAL_CS_DeviceContext)  # get the required variable form DopX interface
        self.Sensor_StartValue = (round(global_cs_devicecontext["ServiceAttributesWM"]\
                                                         [self.interface]\
                                                         ["CurrentValue"])) / 10
        self.compareAndWait_WL_Decrease(self, sensor, status, value, unit)

    def Difference(self, sensor, status, value, unit, period):
        global_cs_devicecontext = self.doper.get(self.st.GLOBAL_CS_DeviceContext)  # get the required variable form DopX interface
        self.Sensor_StartValue = (round(global_cs_devicecontext["ServiceAttributesWM"]\
                                                         [self.interface]\
                                                         ["CurrentValue"])) / 10
        self.compareAndWait_WL_Difference(self, sensor, status, value, unit)

    def Above(self, sensor, status, value, unit, period):
        global_cs_devicecontext = self.doper.get(self.st.GLOBAL_CS_DeviceContext)  # get the required variable form DopX interface
        self.Sensor_StartValue = (round(global_cs_devicecontext["ServiceAttributesWM"]\
                                                         [self.interface]\
                                                         ["CurrentValue"])) / 10
        self.verifyAndWait_WL_Above(self, sensor, status, value, unit)

    def Below(self, sensor, status, value, unit, period):
        global_cs_devicecontext = self.doper.get(self.st.GLOBAL_CS_DeviceContext)  # get the required variable form DopX interface
        self.Sensor_StartValue = (round(global_cs_devicecontext["ServiceAttributesWM"]\
                                                         [self.interface]\
                                                         ["CurrentValue"])) / 10
        self.verifyAndWait_WL_Below(self, sensor, status, value, unit)

    def getValueInterface(self):
        self.DataInterface = self.st.GLOBAL_CS_DeviceContext

