# -- encoding: UTF-8 --
import sys

from click import echo
from colorama import Fore, Style

can_use_real_emoji = (
    sys.stdout.isatty() and
    sys.platform != "win32"
)


def success(msg):
    if can_use_real_emoji:
        sign = "\U0001F44C"
    else:
        sign = "[+] "
    echo(Fore.GREEN + Style.BRIGHT + sign + msg)


def get_site_from_context(ctx):
    try:
        return ctx.meta["wurst.project"].site or None
    except KeyError:
        pass
