# -*- coding: utf-8 -*-
from lettuce import step

@step('Given I do nothing')
def given_i_do_nothing(step):
    pass

@step('Then I see that the test passes')
def then_i_see_that_the_test_passes(step):
    pass

@step('Then I should not see "([^"]+)"')
def then_should_not_see(step, email):
    pass

@step('Given some email addresses')
def given_email_addresses(step):
    pass
