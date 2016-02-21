# -- encoding: UTF-8 --
import os

from click.testing import CliRunner

from wurstc.cli import cli
from wurstc.conf import Config


def test_init_creates_configuration():
    runner = CliRunner()
    with runner.isolated_filesystem() as d:
        result = runner.invoke(cli, [
            '-y',
            'init',
            '-d', '.',
            '-s', 'awesome-project'
        ])
        assert result.exit_code == 0
        cfg = Config(os.path.join(d, '.wurst-project'))
        assert cfg.slug == 'awesome-project'
