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
import lettuce
import lettuce.fs
import mock
from nose.tools import assert_equals
import imp


def test_has_version():
    "A nice python module is supposed to have a version"
    assert_equals(lettuce.version, '0.2.19')


def test_has_release():
    "A nice python module is supposed to have a release name"
    assert_equals(lettuce.release, 'kryptonite')


def test_import():
    "lettuce importer does import"
    import os
    module = lettuce.fs.FileSystem._import('os')
    assert_equals(os, module)


def test_terrain_import_exception():
    "lettuce error tries to import "

    string = 'Lettuce has tried to load the conventional environment ' \
        'module "terrain"\nbut it has errors, check its contents and ' \
        'try to run lettuce again.\n\nOriginal traceback below:\n\n'

    old_FileSystem = lettuce.fs.FileSystem
    old_traceback = lettuce.exceptions.traceback
    old_stderr = lettuce.sys.stderr

    lettuce.fs.FileSystem = mock.Mock(spec=lettuce.fs.FileSystem)
    lettuce.exceptions.traceback = mock.Mock(spec=lettuce.exceptions.traceback)
    lettuce.sys.stderr = mock.Mock(spec=lettuce.sys.stderr)
    lettuce.fs.FileSystem._import = mock.Mock(side_effect=Exception('foo bar'))
    lettuce.exceptions.traceback.format_exc = mock.Mock(\
        return_value='I AM THE TRACEBACK FOR IMPORT ERROR')

    try:
        imp.reload(lettuce)
    except SystemExit:
        lettuce.fs.FileSystem._import.assert_called_once_with('terrain')
    finally:
        lettuce.fs.FileSystem = old_FileSystem
        lettuce.exceptions.traceback = old_traceback
        lettuce.sys.stderr = old_stderr
