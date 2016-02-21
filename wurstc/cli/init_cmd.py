# -- encoding: UTF-8 --
import os

import click

from wurstc.cli.utils import success
from wurstc.conf import Config


@click.command()
@click.pass_context
@click.option(
    '--directory', '-d', prompt=True, default=os.getcwd,
    type=click.Path(exists=True, file_okay=False, writable=True)
)
@click.option('site', '--url', '-u')
@click.option('--slug', '-s')
def init(ctx, directory, site, slug):
    """
    :type ctx: click.Context
    :return:
    """
    directory = os.path.realpath(directory)
    dest_file = os.path.join(directory, ".wurst-project")
    if os.path.isfile(dest_file):
        raise click.ClickException("The destination file %s already exists!" % dest_file)
    if not slug:
        slug = os.path.basename(directory)

    if ctx.meta["wurst.cli"].yes or click.confirm("Write project configuration to %s?" % dest_file):
        config = {
            "site": site,
            "slug": slug
        }
        Config(dest_file, config).save()
        success("Wrote configuration!")
