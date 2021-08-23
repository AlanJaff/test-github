from behave import *
import re

@given("I'm on Google search page")
def step_impl(context):
    print("I'm on Google search page")

@step("I type in the text field to search")
def step_impl(context):
    print("I type in the text field to search")

@when("I click the search button")
def step_impl(context):
    print("I click the search button")

@then("I should be on on the results page")
def step_impl(context):
    print("Search results should appear on search page")
