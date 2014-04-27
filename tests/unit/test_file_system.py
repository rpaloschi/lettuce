# -*- coding: utf-8 -*-
import sys
import mock
import platform
from io import StringIO
from nose.tools import assert_equals
from nose.tools import assert_raises
from lettuce import fs as io

def test_has_a_stack_list():
    "FileSystem stack list"
    assert hasattr(io.FileSystem, 'stack'), \
           'FileSystem should have a stack'
    assert isinstance(io.FileSystem.stack, list), \
           'FileSystem.stack should be a list'

def test_instance_stack_is_not_the_same_as_class_level():
    "FileSystem stack list has different lifecycle in FileSystem objects"
    class MyFs(io.FileSystem):
        pass

    MyFs.stack.append('foo')
    MyFs.stack.append('bar')
    assert_equals(MyFs().stack, [])

def test_pushd_appends_current_dir_to_stack_if_empty():
    "Default behaviour of pushd() is adding the current dir to the stack"
    old_os = io.os
    io.os = mock.Mock(spec=io.os)

    class MyFs(io.FileSystem):
        stack = []

        @classmethod
        def current_dir(cls):
            return 'should be current dir'

    try:
        assert len(MyFs.stack) is 0
        MyFs.pushd('somewhere')
        assert len(MyFs.stack) is 2
        assert_equals(MyFs.stack, ['should be current dir',
                                   'somewhere'])
    finally:
        io.os = old_os

def test_pushd():
    "FileSystem.pushd"
    old_os = io.os
    io.os = mock.Mock(spec=io.os)

    class MyFs(io.FileSystem):
        stack = ['first']

    try:
        assert len(MyFs.stack) is 1
        MyFs.pushd('second')
        assert len(MyFs.stack) is 2
        assert_equals(MyFs.stack, ['first',
                                   'second'])
    finally:
        io.os = old_os

def test_pop_with_more_than_1_item():
    "FileSystem.popd with more than 1 item"
    old_os = io.os
    io.os = mock.Mock(spec=io.os)

    class MyFs(io.FileSystem):
        stack = ['one', 'two']

    try:
        assert len(MyFs.stack) is 2
        MyFs.popd()
        assert len(MyFs.stack) is 1
        assert_equals(MyFs.stack, ['one'])
    finally:
        io.os = old_os

def test_pop_with_1_item():
    "FileSystem.pop behaviour with only one item"
    old_os = io.os
    io.os = mock.Mock(spec=io.os)

    class MyFs(io.FileSystem):
        stack = ['one']

    try:
        assert len(MyFs.stack) is 1
        MyFs.popd()
        assert len(MyFs.stack) is 0
        assert_equals(MyFs.stack, [])        
    finally:
        io.os = old_os

def test_pop_with_no_item():
    "FileSystem.pop behaviour without items in stack"
    old_os = io.os
    io.os = mock.Mock(spec=io.os)

    class MyFs(io.FileSystem):
        stack = []

    try:
        assert len(MyFs.stack) is 0
        MyFs.popd()
        assert len(MyFs.stack) is 0
        assert_equals(MyFs.stack, [])
    finally:
        io.os = old_os

def test_filename_with_extension():
    "FileSystem.filename with extension"
    got = io.FileSystem.filename('/path/to/filename.jpg')
    assert_equals(got, 'filename.jpg')

def test_filename_without_extension():
    "FileSystem.filename without extension"
    got = io.FileSystem.filename('/path/to/filename.jpg', False)
    assert_equals(got, 'filename')

def test_dirname():
    "FileSystem.dirname"
    if platform.system() == 'Windows':
        expected = 'd:\\path\\to'
    else:
        expected = '/path/to'
    
    got = io.FileSystem.dirname('/path/to/filename.jpg').lower()
    assert_equals(got, expected)

def test_exists():
    "FileSystem.exists"
    old_exists = io.exists
    io.exists = mock.Mock(return_value='should be bool')
    try:
        got = io.FileSystem.exists('some path')
        assert_equals(got, 'should be bool')
    finally:
        io.exists = old_exists

def test_extract_zip_non_verbose():
    "FileSystem.extract_zip non-verbose"
    filename = 'modafoca.zip'
    base_path = '../to/project'
    full_path = '/full/path/to/project'

    class MyFs(io.FileSystem):
        stack = []
        abspath = mock.Mock(return_value=full_path)
        pushd = mock.MagicMock()
        popd = mock.MagicMock()
        open_raw = mock.Mock()
        mkdir = mock.MagicMock()

    zipfile_mock = mock.MagicMock()
    io.zipfile = zipfile_mock

    MyFs.pushd(full_path)

    zip_mock = mock.MagicMock()
    io.zipfile.ZipFile = mock.Mock(return_value=zip_mock)

    file_list = [
        'settings.yml',
        'app',
        'app/controllers.py'
    ]
    zip_mock.namelist = mock.Mock(return_value=file_list)

    def read_side_effect(filename):
        if filename == 'settings.yml':
            return 'settings.yml content'
        elif filename == 'app/controllers.py':
            return 'controllers.py content'
        return ''
    zip_mock.read.side_effect = read_side_effect

    file_mock1 = mock.Mock()
    file_mock2 = mock.Mock()

    def myfs_open_raw_side_effect(filename, mode):
        if filename == 'settings.yml':
            return file_mock1
        elif filename == 'app':
            raise IOError('it is a directory, dumb ass!')
        elif filename == 'app/controllers.py':
            return file_mock2
        raise IOError("it shouldn't get here")
    MyFs.open_raw.side_effect = myfs_open_raw_side_effect

    try:
        MyFs.extract_zip('modafoca.zip', base_path)
        file_mock1.write.assert_called_once_with('settings.yml content')
        file_mock1.close.assert_called_once
        file_mock2.write.assert_called_once_with('controllers.py content')
        file_mock2.close.assert_called_once
    except:
        pass


def test_extract_zip_verbose():
    "FileSystem.extract_zip verbose"
    sys.stdout = StringIO()
    filename = 'modafoca.zip'
    base_path = '../to/project'
    full_path = '/full/path/to/project'

    class MyFs(io.FileSystem):
        stack = []
        abspath = mock.Mock(return_value=full_path)
        pushd = mock.MagicMock()
        popd = mock.MagicMock()
        open_raw = mock.Mock()
        mkdir = mock.MagicMock()

    zipfile_mock = mock.MagicMock()
    io.zipfile = zipfile_mock

    MyFs.pushd(full_path)

    zip_mock = mock.MagicMock()
    io.zipfile.ZipFile = mock.Mock(return_value=zip_mock)

    file_list = [
        'settings.yml',
        'app',
        'app/controllers.py'
    ]
    zip_mock.namelist = mock.Mock(return_value=file_list)

    def read_side_effect(filename):
        if filename == 'settings.yml':
            return 'settings.yml content'
        elif filename == 'app/controllers.py':
            return 'controllers.py content'
        return ''
    zip_mock.read.side_effect = read_side_effect

    file_mock1 = mock.Mock()
    file_mock2 = mock.Mock()

    def myfs_open_raw_side_effect(filename, mode):
        if filename == 'settings.yml':
            return file_mock1
        elif filename == 'app':
            raise IOError('it is a directory, dumb ass!')
        elif filename == 'app/controllers.py':
            return file_mock2
        raise IOError("it shouldn't get here")
    MyFs.open_raw.side_effect = myfs_open_raw_side_effect

    try:
        MyFs.extract_zip('modafoca.zip', base_path, verbose=True)
        assert_equals(sys.stdout.getvalue(),
                      'Extracting files to /full/path/to/project\n  ' \
                      '-> Unpacking settings.yml\n  -> Unpacking app' \
                      '\n---> Creating directory app\n  -> Unpacking' \
                      ' app/controllers.py\n')
        file_mock1.write.assert_called_once_with('settings.yml content')
        file_mock1.close.assert_called_once
        file_mock2.write.assert_called_once_with('controllers.py content')
        file_mock2.close.assert_called_once
    finally:
        sys.stdout = sys.__stdout__

def test_locate_non_recursive():
    "FileSystem.locate non-recursive"    
    old_glob = io.glob
    io.glob = mock.Mock()

    base_path = '../to/project'
    full_path = '/full/path/to/project'

    class MyFs(io.FileSystem):
        stack = []
        abspath = mock.Mock(return_value=full_path)

    try:
        MyFs.locate(base_path, '*match*.py', recursive=False)
    finally:
        io.glob = old_glob

def test_locate_recursive():
    "FileSystem.locate recursive"
    base_path = '../to/project'
    full_path = '/full/path/to/project'

    walk_list = [
        (None, None, ['file1.py', 'file2.jpg']),
        (None, None, ['path1/file3.png', 'path1/file4.html'])
    ]

    class MyFs(io.FileSystem):
        stack = []
        abspath = mock.Mock(return_value=full_path)
        walk = mock.Mock(return_value=walk_list)

    try:
        MyFs.locate(base_path, '*match*.py', recursive=True)
    except:
        pass

def test_mkdir_success():
    "FileSystem.mkdir with success"
    old_os = io.os
    io.os = mock.Mock(spec=io.os)

    class MyFs(io.FileSystem):
        pass

    try:
        MyFs.mkdir('/make/all/those/subdirs')
        io.os.makedirs.assert_called_once_with('/make/all/those/subdirs')
    finally:
        io.os = old_os

def test_mkdir_ignore_dirs_already_exists():
    "FileSystem.mkdir in an existent dir"
    
    old_os = io.os
    io.os = mock.Mock(spec=io.os)
    io.os.path = mock.Mock()
    
    class MyFs(io.FileSystem):
        pass

    def makedirs_side_effect(dir):
        oserror = OSError()
        oserror.errno = 17        
        raise oserror

    io.os.makedirs.side_effect = mock.Mock(side_effect=makedirs_side_effect)
    io.os.path.isdir = mock.Mock(return_value=True)

    try:
        MyFs.mkdir('/make/all/those/subdirs')
        io.os.makedirs.assert_called_once_with('/make/all/those/subdirs')
        io.os.path.isdir.assert_called_once_with('/make/all/those/subdirs')
    finally:
        io.os = old_os


def test_mkdir_raises_on_oserror_errno_not_17():
    "FileSystem.mkdir raises on errno not 17"

    old_os = io.os
    io.os = mock.Mock(spec=io.os)
    io.os.path = mock.Mock()
    
    class MyFs(io.FileSystem):
        pass

    def makedirs_side_effect(dir):
        oserror = OSError()
        oserror.errno = 0
        raise oserror

    io.os.makedirs.side_effect = mock.Mock(side_effect=makedirs_side_effect)

    try:
        assert_raises(OSError, MyFs.mkdir, '/make/all/those/subdirs')
        io.os.makedirs.assert_called_once_with('/make/all/those/subdirs')
    finally:
        io.os = old_os


def tes_mkdir_raises_when_path_is_not_a_dir():
    "Test mkdir raises when path is not a dir"
    old_os = io.os
    io.os = mock.Mock(spec=io.os)
    io.os.path = mock.Mock()
    
    class MyFs(io.FileSystem):
        pass

    def makedirs_side_effect(dir):
        oserror = OSError()
        oserror.errno = 17        
        raise oserror

    io.os.makedirs.side_effect = mock.Mock(side_effect=makedirs_side_effect)
    io.os.path.isdir = mock.Mock(return_value=False)
    try:
        assert_raises(OSError, MyFs.mkdir, '/make/all/those/subdirs')
        io.os.makedirs.assert_called_once_with('/make/all/those/subdirs')
    finally:
        io.os = old_os

