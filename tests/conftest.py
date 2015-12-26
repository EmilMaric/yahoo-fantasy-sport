from __future__ import absolute_import

import pytest

from yahoo_oauth import OAuth1
from yahoo_fantasy_sports import YahooFantasySports


base_url = "http://fantasysports.yahooapis.com/fantasy/v2/"


@pytest.fixture(scope="session", autouse=True)
def yfs():
    # TODO: remove the oauth file
    oauth = OAuth1(None, None, from_file="oauth.json", base_url=base_url)
    return YahooFantasySports(oauth)
