# -- encoding: UTF-8 --

from ._base import cli
from .init_cmd import init
from .login_cmd import login

cli.add_command(init)
cli.add_command(login)


def main():
    return cli()
