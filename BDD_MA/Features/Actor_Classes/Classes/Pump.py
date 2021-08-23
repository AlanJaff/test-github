from .Actuator import Actuator_template


class Pump_class(Actuator_template):
    interface = "Lye_Pump"

    def get_actuator(self):
        self.connect(self.interface)
