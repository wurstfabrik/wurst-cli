import getpass
from urllib.parse import urlparse

import click

from wurstc.cli.utils import get_site_from_context, success
from wurstc.conf import user_config
from wurstc.net import WurstSession


def _validate_url(ctx, param, value):
    try:
        url = urlparse(value)
        assert url.scheme, "No scheme (http/https)"
        assert url.netloc, "No netloc"
        return value
    except Exception as exc:
        raise click.BadParameter("%s is not a valid URL: %s" % (value, exc))


@click.command()
@click.pass_context
@click.option('--site', default=click.pass_context(get_site_from_context), prompt=True, callback=_validate_url)
@click.option('username', '-u', '--user', default=getpass.getuser, prompt=True)
@click.password_option('-p', '--password')
def login(ctx, site, username, password):
    """
    Exchange explicit user credentials for a token for a Wurst installation.
    """
    if not site.endswith("/"):
        site += "/"
    if ctx.meta["wurst.cli"].yes or click.confirm("Post your credentials to %s?" % site):
        resp = WurstSession(site).post("api/v1/tokens/", data={
            "username": username,
            "password": password
        })
        token = resp.token
        assert token
        user_config.logins[site] = {"username": username, "token": token}
        user_config.save()
        success("Saved token for %s." % site)
