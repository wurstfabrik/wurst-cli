import site

import click

from wurstc.cli.utils import success
from wurstc.net import WurstSession


class RemoteCommand(click.Command):
    def parse_args(self, ctx, args):
        ctx.args = args  # Remote will deal with the args

    def invoke(self, ctx):
        project = ctx.meta.get("wurst.project")
        if not project.site:
            ctx.fail("A project context is required to run the command %r." % ctx.args[0])
        # TODO: This needs to add the rest of the context (current issue, etc.) somewhere:
        resp = WurstSession(project.site).post("api/v1/cli/", data={
            "args": ctx.args,
            "project": project.slug
        }, headers={
            "Accept": "text/vnd.wurst-cli;q=0.8, application/json, */*"
        })
        success(resp.content)
