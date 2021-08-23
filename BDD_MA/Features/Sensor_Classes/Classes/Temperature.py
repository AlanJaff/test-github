from .Sensor import Sensor_template
import matplotlib
import matplotlib.pyplot as plt

class Temperature_class(Sensor_template):
    interface = "NtcTemperature"  # GLOBAL_CS_DeviceContext

    def Increase(self, sensor, status, value, unit, period):
        global_cs_devicecontext = self.doper.get(self.st.GLOBAL_CS_DeviceContext)  # get the required variable form DopX interface
        self.Sensor_StartValue = global_cs_devicecontext["ServiceAttributesWM"]\
                                                        [self.interface]\
                                                        ["CurrentValue"]
        self.compareAndWait_TempIncrease(sensor, status, value, unit, period, self.interface)

    def Decrease(self, sensor, status, value, unit, period):
        global_cs_devicecontext = self.doper.get(self.st.GLOBAL_CS_DeviceContext)  # get the required variable form DopX interface
        self.Sensor_StartValue = global_cs_devicecontext["ServiceAttributesWM"]\
                                                        [self.interface]\
                                                        ["CurrentValue"]
        self.compareAndWait_TempDecrease(sensor, status, value, unit, period, self.interface)

    def Difference(self, sensor, status, value, unit, period):
        global_cs_devicecontext = self.doper.get(self.st.GLOBAL_CS_DeviceContext)  # get the required variable form DopX interface
        self.Sensor_StartValue = global_cs_devicecontext["ServiceAttributesWM"]\
                                                        [self.interface]\
                                                        ["CurrentValue"]
        self.compareAndWait_TempDifference(sensor, status, value, unit, period, self.interface)

    def Above(self, sensor, status, value, unit, period):
        global_cs_devicecontext = self.doper.get(self.st.GLOBAL_CS_DeviceContext)  # get the required variable form DopX interface
        self.Sensor_StartValue = global_cs_devicecontext["ServiceAttributesWM"]\
                                                        [self.interface]\
                                                        ["CurrentValue"]
        self.verifyAndWait_TempAbove(self, sensor, value, unit, period)

    def Below(self, sensor, status, value, unit, period):
        global_cs_devicecontext = self.doper.get(self.st.GLOBAL_CS_DeviceContext)  # get the required variable form DopX interface
        self.Sensor_StartValue = global_cs_devicecontext["ServiceAttributesWM"]\
                                                        [self.interface]\
                                                        ["CurrentValue"]
        self.verifyAndWaite_TempBelow(self, sensor, value, unit, period)

    def CheckDynamicBehaviour(self, sonsor, soll, unit, expect):
        global_cs_devicecontext = self.doper.get(self.st.GLOBAL_CS_DeviceContext)  # get the required variable form DopX interface
        self.Sensor_StartValue = global_cs_devicecontext["ServiceAttributesWM"]\
                                                        [self.interface]\
                                                        ["CurrentValue"]
        T, t = self.controlAndWait(sonsor, soll, unit, expect)
        print(T)
        print()
        print(t)
        self.plotDynamicBehaviour(T, t, int(expect[1]))
        print()

    def getValueInterface(self):
        self.DataInterface = self.st.GLOBAL_CS_DeviceContext

    def plotDynamicBehaviour(self, T, t, expect):
        expect = [expect] * len(t)  # expectation length = time stamps
        fig, ax = plt.subplots()
        ax.plot(T, t, marker='o', markersize=6, linewidth=2)
        ax.plot(T, expect)
        ax.set(xlabel='Temperatur (°C)', ylabel='Zeit (Δt(T2-T1)) s',
               title='Dynamic System Behaviour')
        ax.grid(True)
        fig.savefig("plot1.png")
        plt.legend(['Temperaturen', 'Erwartungshaltung'])
        plt.show()
