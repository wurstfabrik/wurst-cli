# -- encoding: UTF-8 --
import os
from tempfile import gettempdir

from wurstc.context import find_project_config
from wurstc_tests.consts import test_root_dir, test_project_root_dir


def test_finds_wurstc_project():
    assert (
        os.path.dirname(find_project_config(test_root_dir)._path) ==
        os.path.realpath(test_root_dir + os.sep + os.pardir)
    )


def test_finds_test_project():
    config = find_project_config(test_project_root_dir)
    assert os.path.dirname(config._path) == test_project_root_dir
    assert config.site == "http://example.com/"


def test_doesnt_find_bogus_project():
    assert not find_project_config(gettempdir())
