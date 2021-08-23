from behave import *

use_step_matcher("re")


@given("HiL Test Bench Setup is initialized and Startup is prepared")
def HiLStartupRoutine(context):
    """    HiL Test Bench - Setup    """
    # ToDo: set up the HiL-Startup Routine


@step("the Programs and Software Environments are equipped")
def ProgramEquip(context):
    """    Wool wash program with Single selection    """
    # ToDo: prepare Software Environment s Program selection


@step("the Simulation has started")
def StartSimulation(context):
    """    Reading information from the DopX elements    """
    # ToDo: starting the Simulation


@when("the Heat_Actuator has been activated")
def ActuatorActivation(context, actuator_name, condition):
    """    Check switching-ON of the actuator     """
    # ToDo: checking the Heat Actuator activation status


@step("the Valve_CW_Actuator has been activated")
def ActuatorActivation(context, actuator_name, condition):
    """    Check switching-ON of the actuator     """
    # ToDo: checking the Waster Valve Actuator activation status


@then("assert the Lye_Temperature Increase of 3 °C within 180 seconds")
def SensorAsserion(context, sensor, status, value, unit, period):
    """    Assertion status of teh Sensor     """
    # ToDo: checking and asserting the Sensor status
