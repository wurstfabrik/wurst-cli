# -- encoding: UTF-8 --
import os

from wurstc.conf import Config


def find_project_config(start_dir):
    """
    Find project configuration.

    :param start_dir: Where to start looking.
    :return: A root directory, or None if one could not be found
    :rtype: wurstc.conf.Config|None
    """

    user_home = os.path.realpath(os.path.expanduser("~"))

    for depth in range(15):  # 15 directories up should hopefully be plenty.
        dir = os.path.realpath(start_dir + (os.sep + "..") * depth)
        wurstproject = os.path.join(dir, ".wurst-project")
        if os.path.isfile(wurstproject):  # Explicit project marker!
            return Config(wurstproject)
        if dir == user_home:  # Let's not transgress above user home, for sanity.
            break
