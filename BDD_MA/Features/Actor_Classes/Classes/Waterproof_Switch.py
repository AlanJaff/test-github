from .Actuator import Actuator_template


class Waterproof_Switch_class(Actuator_template):
    interface = "WpsSwitch"  # CDV_SensorData
    Engaged = None
    DataInterface = None

    def get_actuator(self):

        if self.condition == "activated":
            self.connect(self.interface)

        elif self.condition == "deactivated":
            self.disconnect(self.interface)

    def getDataInterface(self):
        self.DataInterface = self.st.CDV_SensorData

