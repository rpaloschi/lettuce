# lettuce for python 3
> Version 0.0.01

## What is this

This is a fork of the wonderful BDD tool [Lettuce](http://lettuce.it/), an adventurous effort on porting lettuce to Python 3 + Django 1.6 :)
So... almost everything that is valid for the original lettuce is valid here.

# Motivation

1. Have this great tool working on python 3 and for new versions of django
2. The fact that I was unable to find any reasonable working port... so I decided to get my hands dirty.
3. Maybe get some help for doing this
4. If we think it is good... we can merge back (or contribute back) to the original lettuce project
5. Just for the sake of doing it!

# Status

* It was ported, initially using 2to3, than changed step by step using the tests as a reference.
* Python version 3.4.
* Django version 1.6.2.
* Mox was replaced by Mock. It made all of this possible.
* All the tests of the original lettuce passes except for one that was removed alongside the feature below.
* LETTUCE_SERVE_ADMIN_MEDIA has been removed because it was implemented based on django 1.3. The classes that it relied
doesn't exist anymore, so it was removed. In theory, this is the only missing feature on the original lettuce.
* It was done on Windows, but the convention was changed to use forward slashes for paths on all OS's.
* It wasn't tested on other OS's yet, I plan to do it as soon as I can, but hey! Clone it and help me!
* There is some work to do and some things to be checked yet, the fact that is usable, so grab your git client and clone
it! :)

# Dependencies

* Install the dependencies on requirements.txt (preferably on a virtualenv). The plan is to cut it into smaller chunks
separated by os, but this is enough to run all tests on windows.
* Some of the dependencies are not needed on other OS's. That will be fixed.
* fuzzywuzzy is not Python 3 compatible, so you will need to tweak it to make it work. Just two changes...
 I will post a patch here as soon as possible.

# License

    <Lettuce - Behaviour Driven Development for python>
    Copyright (C) <2010-2012>  Gabriel Falcão <gabriel@nacaolivre.org>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
