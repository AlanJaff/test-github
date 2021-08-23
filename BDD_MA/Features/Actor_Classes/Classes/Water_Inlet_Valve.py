from .Actuator import Actuator_template


class Water_Inlet_class(Actuator_template):
    interface = "VerbraucherVentilKW"  # CDV_ProcessData
    Engaged = None
    DataInterface = None

    def get_actuator(self):

        if self.condition == "activated":
            self.connect(self.interface)

        elif self.condition == "deactivated":
            self.disconnect(self.interface)

        elif self.condition == "halted":
            self.halted(self.interface)

    def getDataInterface(self):
        self.DataInterface = self.st.CDV_ProcessData