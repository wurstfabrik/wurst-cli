# -- encoding: UTF-8 --
import logging
import os

import click

from wurstc.conf import Config
from wurstc.context import find_project_config


class CliConfig(object):
    def __init__(self, debug=False, yes=False):
        self.debug = debug
        self.yes = yes


@click.group()
@click.option('--project', envvar='WURST_PROJECT', default=None)
@click.option('--debug/--no-debug', default=False, envvar='WURST_DEBUG')
@click.option('--yes/--no-yes', '-y', default=False)
@click.pass_context
def cli(ctx, project, debug, yes):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    if project:
        project = Config(project)
    else:
        project = find_project_config(os.getcwd())
    ctx.meta["wurst.project"] = project
    ctx.meta["wurst.cli"] = CliConfig(debug=debug, yes=yes)
