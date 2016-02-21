# -- encoding: UTF-8 --
from addict import Dict
from requests import Session
from six.moves.urllib.parse import urljoin


class WurstSession(Session):
    """
    A "DWIM" requests session wrapper for sessions targeting the Wurst API.
    """

    def __init__(self, base_url):
        self.base_url = base_url
        super(WurstSession, self).__init__()

    def request(self, method, url, **kwargs):
        autoraise = kwargs.pop("raise", True)
        autocast = kwargs.pop("cast", True)

        if not (url.startswith("http://") or url.startswith("https://")):
            url = urljoin(self.base_url, url)
        kwargs["method"] = method
        kwargs["url"] = url

        response = super(WurstSession, self).request(**kwargs)

        if autoraise:
            response.raise_for_status()
        if autocast:
            if response.headers["content-type"].startswith("application/json"):
                return Dict(response.json())
        return response
