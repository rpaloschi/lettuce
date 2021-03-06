# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
# Copyright (C) <2010-2012>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys
from nose.tools import assert_equals

from lettuce import step
from lettuce.terrain import after
from lettuce.terrain import before
from lettuce.terrain import world
from lettuce.core import Feature, TotalResult
from lettuce.registry import CALLBACK_REGISTRY
import collections
import mock

FEATURE1 = '''
Feature: Before and After callbacks all along lettuce
    Scenario: Before and After steps
        Given I append "during" to states
'''

FEATURE2 = '''
Feature: Before and After callbacks all along lettuce
    Scenario: Before and After scenarios
        Given I append "during" to states

    Scenario: Again
        Given I append "during" to states
'''


FEATURE3 = '''
Feature: Before and After callbacks all along lettuce
    @tag1
    Scenario: Before and After scenarios
        Given I append "during" to states

    @tag2
    Scenario: Again
        Given I append "during" to states
'''

def test_world():
    "lettuce.terrain.world can be monkey patched at will"

    def set_world():
        world.was_set = True

    def test_does_not_have():
        from lettuce.terrain import world
        assert not hasattr(world, 'was_set')

    def test_does_have():
        from lettuce.terrain import world
        assert hasattr(world, 'was_set')

    test_does_not_have()
    set_world()
    test_does_have()


def test_after_each_step_is_executed_before_each_step():
    "terrain.before.each_step and terrain.after.each_step decorators"
    world.step_states = []

    @before.each_step
    def set_state_to_before(step):
        world.step_states.append('before')
        expected = 'Given I append "during" to states'
        if step.sentence != expected:
            raise TypeError('%r != %r' % (step.sentence, expected))

    @step('append "during" to states')
    def append_during_to_step_states(step):
        world.step_states.append("during")

    @after.each_step
    def set_state_to_after(step):
        world.step_states.append('after')
        expected = 'Given I append "during" to states'
        if step.sentence != expected:
            raise TypeError('%r != %r' % (step.sentence, expected))

    feature = Feature.from_string(FEATURE1)
    feature.run()

    assert_equals(world.step_states, ['before', 'during', 'after'])


def test_after_each_scenario_is_executed_before_each_scenario():
    "terrain.before.each_scenario and terrain.after.each_scenario decorators"
    world.scenario_steps = []

    @before.each_scenario
    def set_state_to_before(scenario):
        world.scenario_steps.append('before')

    @step('append "during" to states')
    def append_during_to_scenario_steps(step):
        world.scenario_steps.append("during")

    @after.each_scenario
    def set_state_to_after(scenario):
        world.scenario_steps.append('after')

    feature = Feature.from_string(FEATURE2)
    feature.run()

    assert_equals(
        world.scenario_steps,
        ['before', 'during', 'after', 'before', 'during', 'after'],
    )


def test_after_each_feature_is_executed_before_each_feature():
    "terrain.before.each_feature and terrain.after.each_feature decorators"
    world.feature_steps = []

    @before.each_feature
    def set_state_to_before(feature):
        world.feature_steps.append('before')

    @step('append "during" to states')
    def append_during_to_feature_steps(step):
        world.feature_steps.append("during")

    @after.each_feature
    def set_state_to_after(feature):
        world.feature_steps.append('after')

    feature = Feature.from_string(FEATURE2)
    feature.run()

    assert_equals(
        world.feature_steps,
        ['before', 'during', 'during', 'after'],
    )


def test_feature_hooks_not_invoked_if_no_scenarios_run():
    feature = Feature.from_string(FEATURE3)

    world.feature_steps = []
    feature.run(tags=['tag1'])
    assert_equals(
        world.feature_steps,
        ['before', 'during', 'after']
    )

    world.feature_steps = []
    feature.run(tags=['tag3'])
    assert_equals(
        world.feature_steps,
        []
    )


def test_after_each_all_is_executed_before_each_all():
    "terrain.before.each_all and terrain.after.each_all decorators"
    import lettuce
    from lettuce.fs import FeatureLoader
    world.all_steps = []

    loader_mock = mock.Mock(spec=FeatureLoader)
    old_sys_path = lettuce.sys.path
    old_fs = lettuce.fs
    old_FileSystem = lettuce.fs.FileSystem
    old_Feature = lettuce.Feature

    lettuce.sys.path = mock.Mock(spec=old_sys_path)
    lettuce.sys.path.insert = mock.Mock()
    lettuce.sys.path.remove = mock.Mock()
    lettuce.fs = mock.Mock(spec=old_fs)
    lettuce.fs.FileSystem = mock.Mock(spec=old_FileSystem)
    lettuce.Feature = mock.Mock(spec=old_Feature)

    loader_mock.find_feature_files = mock.Mock(return_value=['some_basepath/foo.feature'])
    lettuce.fs.FeatureLoader = mock.Mock(return_value=loader_mock)    
    lettuce.Feature.from_file = mock.Mock(return_value=Feature.from_string(FEATURE2))

    runner = lettuce.Runner('some_basepath')
    CALLBACK_REGISTRY.clear()

    @before.all
    def set_state_to_before():
        world.all_steps.append('before')

    @step('append "during" to states')
    def append_during_to_all_steps(step):
        world.all_steps.append("during")

    @after.all
    def set_state_to_after(total):
        world.all_steps.append('after')
        isinstance(total, TotalResult)

    runner.run()

    lettuce.sys.path.insert.assert_called_with(0, 'some_basepath')
    lettuce.sys.path.remove.assert_called_with('some_basepath')
    loader_mock.find_and_load_step_definitions.assert_called_once
    lettuce.Feature.from_file.assert_called_once_with('some_basepath/foo.feature')

    assert_equals(
        world.all_steps,
        ['before', 'during', 'during', 'after'],
    )

    lettuce.sys.path = old_sys_path
    lettuce.fs = old_fs
    lettuce.fs.FileSystem = old_FileSystem
    lettuce.Feature = old_Feature


def test_world_should_be_able_to_absorb_functions():
    "world should be able to absorb functions"
    assert not hasattr(world, 'function1')

    @world.absorb
    def function1():
        return 'absorbed'

    assert hasattr(world, 'function1')
    assert isinstance(world.function1, collections.Callable)

    assert_equals(world.function1(), 'absorbed')

    world.spew('function1')

    assert not hasattr(world, 'function1')


def test_world_should_be_able_to_absorb_lambdas():
    "world should be able to absorb lambdas"
    assert not hasattr(world, 'named_func')

    world.absorb(lambda: 'absorbed', 'named_func')

    assert hasattr(world, 'named_func')
    assert isinstance(world.named_func, collections.Callable)

    assert_equals(world.named_func(), 'absorbed')

    world.spew('named_func')

    assert not hasattr(world, 'named_func')


def test_world_should_be_able_to_absorb_classs():
   "world should be able to absorb class"
   assert not hasattr(world, 'MyClass')

   if sys.version_info < (2, 6):
       return

   class MyClass:
       pass

   world.absorb(MyClass)

   assert hasattr(world, 'MyClass')
   assert_equals(world.MyClass, MyClass)

   assert isinstance(world.MyClass(), MyClass)

   world.spew('MyClass')

   assert not hasattr(world, 'MyClass')


def test_hooks_should_be_still_manually_callable():
    "terrain hooks should be still manually callable"

    @before.all
    def before_all():
        pass

    @before.harvest
    def before_harvest():
        pass

    @before.each_app
    def before_each_app():
        pass

    @before.each_step
    def before_each_step():
        pass

    @before.each_scenario
    def before_each_scenario():
        pass

    @before.each_feature
    def before_each_feature():
        pass

    @before.handle_request
    def before_handle_request():
        pass

    @before.outline
    def before_outline():
        pass

    @after.all
    def after_all():
        pass

    @after.harvest
    def after_harvest():
        pass

    @after.each_app
    def after_each_app():
        pass

    @after.each_step
    def after_each_step():
        pass

    @after.each_scenario
    def after_each_scenario():
        pass

    @after.each_feature
    def after_each_feature():
        pass

    @after.handle_request
    def after_handle_request():
        pass

    @after.outline
    def after_outline():
        pass

    assert isinstance(before_all, collections.Callable), \
        '@before.all decorator should return the original function'

    assert isinstance(before_handle_request, collections.Callable), \
        '@before.handle_request decorator should return the original function'

    assert isinstance(before_harvest, collections.Callable), \
        '@before.harvest decorator should return the original function'

    assert isinstance(before_each_feature, collections.Callable), \
        '@before.each_feature decorator should return the original function'

    assert isinstance(before_outline, collections.Callable), \
        '@before.outline decorator should return the original function'

    assert isinstance(before_each_scenario, collections.Callable), \
        '@before.each_scenario decorator should return the original function'

    assert isinstance(before_each_step, collections.Callable), \
        '@before.each_step decorator should return the original function'

    assert isinstance(after_all, collections.Callable), \
        '@after.all decorator should return the original function'

    assert isinstance(after_handle_request, collections.Callable), \
        '@after.handle_request decorator should return the original function'

    assert isinstance(after_harvest, collections.Callable), \
        '@after.harvest decorator should return the original function'

    assert isinstance(after_each_feature, collections.Callable), \
        '@after.each_feature decorator should return the original function'

    assert isinstance(after_outline, collections.Callable), \
        '@after.outline decorator should return the original function'

    assert isinstance(after_each_scenario, collections.Callable), \
        '@after.each_scenario decorator should return the original function'

    assert isinstance(after_each_step, collections.Callable), \
        '@after.each_step decorator should return the original function'
