
Feature: Multiple actuators of the program will tested and proved
         along with indicated sensor status with the approved time

  Scenario: Actuators activation and Sensors status validation
    Given HiL Test Bench Setup is initialized and Startup is prepared
    And the Programs and Software Environments are equipped
    And the Simulation has started
    When the Heat_Actuator has been activated
    And the Valve_CW_Actuator has been activated
    Then assert the Lye_Temperature Increase of 3 °C within 180 seconds
