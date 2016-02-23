# -- encoding: UTF-8 --
import logging
import os

import click
from click.utils import make_str

from wurstc.cli.remote import RemoteCommand
from wurstc.conf import Config
from wurstc.context import find_project_config


class CliConfig(object):
    def __init__(self, debug=False, yes=False):
        self.debug = debug
        self.yes = yes


class WurstGroup(click.Group):
    def resolve_command(self, ctx, args):
        try:
            return super().resolve_command(ctx, args)
        except click.UsageError as usagi:
            # TODO: Might there perchance be a cleaner way to handle this?
            if usagi.args[0].startswith("No such command "):
                cmd_name = make_str(args[0])
                cmd_class = RemoteCommand(cmd_name)
                return (cmd_name, cmd_class, args)
            raise


@click.command(cls=WurstGroup)
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
