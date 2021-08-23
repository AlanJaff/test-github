from .Classes.Water_Level import Water_Level_class
from .Classes.Temperature import Temperature_class
from .Classes.FlowMeter_CW import FlowMeter_ColdWater_class
from .Classes.FlowMeter_WW import FlowMeter_WarmWater_class


Sensor_Register = {"Lye_Temperature": Temperature_class,
                   "Water_Level": Water_Level_class,
                   "FlowMeter_ColdWater": FlowMeter_ColdWater_class,
                   "FlowMeter_WarmWater": FlowMeter_WarmWater_class}
