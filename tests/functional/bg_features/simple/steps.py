# -*- coding: utf-8 -*-
from lettuce import step

# TODO [rpaloschi]: the tests fail randomly if this is not commented...
# that is caused because of the order the steps are iterated.
#@step('Given the variable "([^"]*)" is equal to 2')
#def given_the_variable_group1_is_equal_to_2(step, group1):
#   pass

@step('When the variable "([^"]*)" holds 10')
def when_the_variable_group1_holds_10(step, group1):
    pass

@step('Then the variable "([^"]*)" times 5 is equal to 50')
def then_the_variable_group1_times_5_is_equal_to_50(step, group1):
    pass

@step('And the variable "([^"]*)" is equal to 10')
def and_the_variable_group1_is_equal_to_10(step, group1):
    pass

@step('Then the variable "([^"]*)" times 5 is equal to 10')
def then_the_variable_group1_times_5_is_equal_to_10(step, group1):
    pass

@step('And the variable "([^"]*)" is equal to 2')
def and_the_variable_group1_is_equal_to_2(step, group1):
    pass
