
Feature: In this Hardware-in-the-Loop Test Bench the applicable test cases
         in the first scenario will be tested and simulated successively in the described scenarios,
         in order the check and verify the portability of the BDD-Methodology on mechatronics systems
         The second scienaro is formulated to test a Use Case for the Control of the System Behaviour
         Use Case for the Regulation of the Dynamic Behaviour is formulated and performed
         in the third scenario
# -----------------------------------------------------------------------------
# Background: Hil Test Bench Setup & initialization for the Test Case execution
# -----------------------------------------------------------------------------
  Scenario: Testing and simulating the Test Case "WT_Wolle" Program
    Given Hil-Test Bench Setup is initialized
    And the physical model, relevant software and simulations have started up
    And information from the DopX Communication interface is read out
    And the Reporting for Test Case is developed
    When the electronic_Finger is automatically triggered
    Then start the Simulation and assert Remaining Time of WT_Wolle
# -----------------------------------------------------------------------------
# Background: SiL Test Bench Setup & initialization for the Test Case execution
# -----------------------------------------------------------------------------
  Scenario: Testing and simulating the Test Case "WT_Wolle" Program
    Given SiL-Test Bench Setup is initialized
    And the physical model, relevant software and simulations have started up
    And information from the DopX Communication interface is read out
    And the Reporting for Test Case is developed
    When the electronic_Finger is automatically triggered
    Then start the Simulation and assert Remaining Time of WT_Wolle
# ------------------------------------------------------------------------
# Background: Use Case for the Test Case execution
# ------------------------------------------------------------------------
  Scenario: Testing and simulating the Test Case of "WT_Wolle" Program
    Given Hil-Test Bench Setup is initialized
    And the physical model, relevant software, and simulations started up
    And information from the Communication interface ist read out
    And the Reporting of the Test Case is developed
    When the electronic_Finger is automatically triggered
    Then start the Simulation and assert Remaining Time of WT_Wolle
# --------------------------------------------------------------------
# Background: Use Case for the Control of the System Behaviour
# --------------------------------------------------------------------
  Scenario: Use case for the control of actuators and sensors behavior
    Given HiL Test Bench Setup is initialized and Startup is prepared
    And the Program and Software Environment equipped
    And the Simulation has started
    When the Heat_Actuator has been activated
    And the Lye_Pump_Actuator has been activated
    And the Water_Level is above 50 mmWS within 60 seconds
    Then assert the Water_Level after statues validation

# -------------------------------------------------------------------
# Background: Use Case for the Regulation of the Dynamic Behaviour
# -------------------------------------------------------------------
  Scenario: Use case for the regulation of the dynamic behavior
    Given HiL Test Bench Setup is initialized and Startup is prepared
    And the Program and Software Environment equipped
    And the Simulation has started
    When the Heat_Actuator has been activated
    And the Lye_Temperature reach 27 °C with Dynamic Behaviour complies 1 °C per 20 seconds
    Then assert the Lye_Temperature after statues validation

# ---------------------------------------------------------------------
# Background: Implemented Scenarios
# ---------------------------------------------------------------------
  Scenario: Lye Temperature Check

    When the Heat_Actuator has been activated
    And the Valve_CW_Actuator has been activated
    Then assert the Lye_Temperature Increase of 3 °C within 90 seconds

    When the Heat_Actuator has been activated
    And the Valve_CW_Actuator has been activated
    Then assert the Lye_Temperature Decrease of 3 °C within 60 seconds

    When the Heat_Actuator has been activated
    And the Valve_CW_Actuator has been activated
    Then assert the Lye_Temperature Difference of 4 °C within 180 seconds

    When the Heat_Actuator has been activated
    And the Lye_Temperature is above 21 °C within 80 seconds
    Then assert the Lye_Temperature after statues validation

    When the Heat_Actuator has been activated
    And the Lye_Temperature is below 25 °C within 60 seconds
    Then assert the Lye_Temperature after statues validation
# ---------------------------------------------------------------------
  Scenario: Water Level Check

    When the Lye_Pump_Actuator has been activated
    Then assert the Water_Level Increase of 5 mmWS within 90 seconds

    When the Lye_Pump_Actuator has been activated
    Then assert the Water_Level Decrease of 5 mmWS within 60 seconds

    When the Lye_Pump_Actuator has been activated
    Then assert the Water_Level Difference of 5 mmWS within 180 seconds

    When the Heat_Actuator has been activated
    And the Lye_Pump_Actuator has been deactivated
    And the Water_Level is above 50 mmWS within 60 seconds
    Then assert the Water_Level after statues validation

    When the Heat_Actuator has been activated
    And the Lye_Pump_Actuator has been deactivated
    And the Water_Level is below 40 mmWS within 60 seconds
    Then assert the Water_Level after statues validation

# ---------------------------------------------------------------------
  Scenario: Multiple Actuators Check

    When the Heat_Actuator has been activated
    And the Valve_CW_Actuator has been activated
    Then the Lye_Pump_Actuator must be deactivated

    When the Waterproof_Switch has been activated
    Then the Water_Inlet_Valve must be halted

    When the Door_Emergency has been activated
    Then all Actuators must be halted

    When the Heat_Actuator has been activated
    When the Valve_WW_Actuator has been activated
    Then the Lye_Pump_Actuator must be deactivated

    When the Circulation_Pump_Actuator has been activated
    Then the Water_Inlet_Valve must be deactivated
