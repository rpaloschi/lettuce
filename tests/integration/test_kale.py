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
import subprocess
from lettuce.fs import FileSystem
from nose.tools import assert_equals
from tests.util import run_scenario

current_directory = FileSystem.dirname(__file__)


@FileSystem.in_directory(current_directory, 'django', 'kale')
def test_harvest_uses_test_runner():
    'harvest uses LETTUCE_TEST_SERVER specified in settings'

    status, out = run_scenario('leaves', 'modification')

    assert_equals(status, 0, out)
