from .Classes.Heater import Heater_class
from .Classes.Lye_Pump import Lye_Pump_class
from .Classes.Valve_CW import Valve_CW_class
from .Classes.Valve_WW import Valve_WW_class
from .Classes.Water_Inlet_Valve import Water_Inlet_class
from .Classes.Circulation_Pump import Circulation_Pump_class
from .Classes.Waterproof_Switch import Waterproof_Switch_class


Actuator_Register = {"Heat_Actuator": Heater_class,
                     "Lye_Pump_Actuator": Lye_Pump_class,
                     "Circulation_Pump_Actuator": Circulation_Pump_class,
                     "Water_Inlet_Valve": Water_Inlet_class,
                     "Valve_CW_Actuator": Valve_CW_class,
                     "Valve_WW_Actuator": Valve_WW_class,
                     "Waterproof_Switch": Waterproof_Switch_class}
