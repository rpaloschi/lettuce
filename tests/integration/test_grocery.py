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
import os
import sys
import subprocess

from lettuce.fs import FileSystem
from tests.asserts import assert_equals

current_directory = FileSystem.dirname(__file__)
lib_directory = FileSystem.join(current_directory,  'lib')


OLD_PYTHONPATH = os.getenv('PYTHONPATH', ':'.join(sys.path))


def teardown():
    os.environ['PYTHONPATH'] = OLD_PYTHONPATH


@FileSystem.in_directory(current_directory, 'django', 'grocery')
def test_django_admin_media_serving_on_django_13_and_up():
    'lettuce should serve admin static files properly on Django 1.3 and up'

    os.environ['PYTHONPATH'] = "%s:%s" % (
        FileSystem.join(lib_directory, 'Django-1.6.2'),
        OLD_PYTHONPATH,
    )

    status, out = subprocess.getstatusoutput(
        "%s manage.py harvest --verbosity=2 ./features/" % sys.executable)

    assert_equals(status, 0, out)

    lines = out.splitlines()

    assert "Preparing to serve django's admin site static files..." in lines
    assert 'Running on port 7000 ... OK' in lines
    assert 'Fetching admin media ... OK' in lines
    assert 'Fetching static files ... OK' in lines
    assert 'Fetching CSS files: ... OK' in lines
    assert 'Fetching javascript files: ... OK' in lines
    assert "Django's builtin server is running at 0.0.0.0:7000" in lines
