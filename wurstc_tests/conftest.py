# -- encoding: UTF-8 --
import os
import tempfile
import uuid


def pytest_runtest_setup(item):
    from wurstc.conf import user_config
    user_config._path = os.path.join(tempfile.gettempdir(), "wurst-test-user-cfg-%s" % uuid.uuid4())
