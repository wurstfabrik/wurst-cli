# -- encoding: UTF-8 --
import os

import toml
from addict import Dict
from boltons.fileutils import atomic_save


def _get_config_dir():
    """
    Get the configuration root directory.

    See these URLs for reference:
    * http://blogs.msdn.com/b/patricka/archive/2010/03/18/where-should-i-store-my-data-and-configuration-files-if-i-target-multiple-os-versions.aspx
    * https://specifications.freedesktop.org/basedir-spec/basedir-spec-0.8.html

    :return: A directory path, guaranteed to exist
    """
    for dir in (
        os.environ.get("WURST_CONFIG_DIR"),
        "$APPDATA/Wurst",  # Windows (first, as some POSIX utilities may have created `.config` dirs even under Windows)
        "~/Library/Application Support/Wurst",  # OS X
        "$XDG_CONFIG_HOME/wurst",  # XDG Base Directory
        "~/.config/wurst",  # XDG Base Directory fallback
        "~/.wurst",  # Last resort :(
    ):
        if not dir:  # The envvar could be falsy.
            continue
        dir = os.path.expandvars(os.path.expanduser(dir))
        if "$" in dir:  # Not all variables were extracted; this is terrible
            continue
        if os.path.isdir(os.path.dirname(dir)):
            if not os.path.isdir(dir):
                os.makedirs(dir)
            return dir


class Config(object):
    """
    A wrapper object for a TOML format configuration file.

    To persist changes, call `.save()`.
    """

    __wrapped__ = False  # This makes doctest behave with our top-level Addict object.

    def __init__(self, path, data=None):
        self._path = path
        self._data = (Dict(data) if data else None)

    def __getitem__(self, item):
        if self._data is None:
            self._load()
        return self._data[item]

    def __getattr__(self, item):
        return self[item]

    def _load(self):
        if os.path.isfile(self._path):
            with open(self._path, "r") as infp:
                self._data = Dict(toml.load(infp))
        else:
            self._data = Dict()

    def save(self):
        if self._data is None:
            return

        with atomic_save(self._path) as outfp:
            self._data.prune()
            data = toml.dumps(self._data.to_dict()).encode("utf8")
            outfp.write(data)


#: The global per-user configuration.
user_config = Config(os.path.join(_get_config_dir(), "wurst.toml"))
