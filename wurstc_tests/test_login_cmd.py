# -- encoding: UTF-8 --
import uuid

import requests_mock
from click.testing import CliRunner

from wurstc.cli import cli
from wurstc.conf import Config, user_config


def test_login_gets_tokens():
    runner = CliRunner()
    with requests_mock.mock() as m:
        gen_token = str(uuid.uuid4())
        m.post(
            'http://example.com/api/v1/tokens/',
            json={'token': gen_token},
            headers={'Content-Type': 'application/json; charset=UTF-8'}
        )
        result = runner.invoke(cli, [
            '-y',
            'login',
            '--site', 'http://example.com',  # Missing the slash on purpose.
            '-u', 'root',
            '-p', 'gibson'
        ])
        assert result.exit_code == 0
        cfg = Config(user_config._path)
        assert cfg.logins["http://example.com/"].token == gen_token
