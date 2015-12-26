from __future__ import absolute_import

import pytest

from yahoo_fantasy_sports import YahooFantasySportsError
from yahoo_fantasy_sports.games import Game, Games


class TestGames(object):
    """
    Test the Game Collection class.
    """

    @staticmethod
    @pytest.fixture(scope='class')
    def games(yfs):
        return yfs.games(game_keys=[212, 273, 323])

    def test_games_creation(self, games):
        """
        Verify that passing in more than one ``game_key`` creates a ``Games``
        collection object, rather than a ``Game`` resource object.
        """
        assert isinstance(games, Games)
        assert len(games) == 3
        assert games[212]
        assert games[273]
        assert games[323]

    def test_games_is_available(self, yfs):
        """
        Verify that passing ``True`` to ``is_available`` option returns only
        fantasy games that are currently available, and inversely, passing
        ``False`` returns fantasy games that have finished and are unavilable.
        Lastly, verify that passing something other than ``True`` or ``False``

        """
        games = yfs.games(game_keys=[212, 273, 'nba'], is_available=True)
        assert len(games) == 1

        games = yfs.games(game_keys=[212, 273, 'nba'], is_available=False)
        assert len(games) == 2

        with pytest.raises(YahooFantasySportsError):
            games = yfs.games(game_keys=[212, 273, 'nba'], is_available=1)

    def test_game_types(self, yfs):
        """
        Verify that ``game_types`` can be filtered for.
        """
        games = yfs.games(game_keys=[212, 273, 323], game_types=['full'])
        assert len(games) == 1

        games = yfs.games(game_keys=[212, 273, 323],
                          game_types=['pickem-team-list', 'full'])
        assert len(games) == 3

        games = yfs.games(game_keys=[212, 273, 323],
                          game_types=['pickem-team'])
        assert len(games) == 0

        with pytest.raises(YahooFantasySportsError):
            games = yfs.games(game_keys=[212, 273, 323], game_types=('full'))

    def test_game_codes(self, yfs):
        """
        Verify that ``game_codes`` can be filtered for.
        """
        games = yfs.games(game_keys=[212, 273, 323], game_codes=['nfl'])
        assert len(games) == 1

        games = yfs.games(game_keys=[212, 273, 323], game_codes=['ncaafb'])
        assert len(games) == 2

        games = yfs.games(game_keys=[212, 273, 323],
                          game_codes=['ncaafb', 'nfl'])
        assert len(games) == 3

        games = yfs.games(game_keys=[212, 273, 323],
                          game_codes=['nba'])
        assert len(games) == 0

        with pytest.raises(YahooFantasySportsError):
            games = yfs.games(game_keys=[212, 273, 323], game_codes=('nba'))

    def test_seasons(self, yfs):
        """
        Verify that ``seasons`` can be filtered for.
        """
        games = yfs.games(game_keys=[212, 273, 323], seasons=['2008'])
        assert len(games) == 1

        games = yfs.games(game_keys=[212, 273, 323], seasons=['2008', '2012'])
        assert len(games) == 2

        games = yfs.games(game_keys=[212, 273, 323], seasons=['2009'])
        assert len(games) == 0

        with pytest.raises(YahooFantasySportsError):
            games = yfs.games(game_keys=[212, 273, 323], seasons=('2008'))

    def test_multi_options(self, yfs):
        """
        Verify that multiple options, such as ``is_available=True`` and
        ``seasons=['2015']`` can be provided at once for filtering.
        """
        games = yfs.games(game_keys=[212, 273, 323], game_codes=['ncaafb'],
                          game_types=['pickem-team-list'])
        assert len(games) == 2

        games = yfs.games(game_keys=[212, 273, 323], game_codes=['ncaafb'],
                          game_types=['pickem-team-list'], seasons=['2008'])
        assert len(games) == 1

        games = yfs.games(game_keys=[212, 273, 323], game_codes=['ncaafb'],
                          game_types=['pickem-team-list'], seasons=['2008'],
                          is_available=True)
        assert len(games) == 0


class TestGame(object):
    """
    Test the Game Resource class.
    """

    @staticmethod
    @pytest.fixture(scope='class')
    def nba_game(yfs):
        games = yfs.games(game_keys=['nba'])
        assert len(games) == 1
        # extract single game_key from Games object
        game_key = games.keys[0]
        return games[game_key]

    @staticmethod
    @pytest.fixture(scope='class')
    def finished_game(yfs):
        return yfs.games(game_keys=[273])[273]

    def test_meta_string(self, nba_game):
        """
        Test Game meta information gets fetched correctly by providing
        a fantasy sport as a string name.
        """
        assert isinstance(nba_game, Game)
        assert nba_game.code == 'nba'
        # game_key/game_id changes every year for each fantasy sport to the
        # most current fantasy game. Testing for an explicit game_key will
        # eventually cause the test to fail. So we can only test that game_key
        # and game_id are identical
        assert nba_game.game_key == nba_game.game_id
        assert isinstance(nba_game.game_key, int)
        assert isinstance(nba_game.game_id, int)
        assert nba_game.name == 'Basketball'
        assert hasattr(nba_game, 'url')
        assert hasattr(nba_game, 'season')
        assert hasattr(nba_game, 'is_registration_over')
        assert hasattr(nba_game, 'type')

    def test_meta_int(self, finished_game):
        """
        Test Game meta information gets fetched correctly by providing
        a fantasy sport as an integer.
        """
        assert finished_game.game_key == 273
        assert finished_game.game_id == 273
        assert finished_game.code == 'nfl'
        assert finished_game.name == 'Football'
        assert finished_game.url == \
            'http://football.fantasysports.yahoo.com/archive/nfl/2012'
        assert finished_game.season == 2012
        assert finished_game.is_registration_over == 1
        assert finished_game.type == 'full'

    def test_game_weeks(self, nba_game):
        """
        Test 'game_weeks' attribute invocation.
        """
        assert len(nba_game.game_weeks) == 23
        assert nba_game.game_weeks[1].week == 1
        assert nba_game.game_weeks[1].start
        assert nba_game.game_weeks[1].end

    def test_stat_categories(self, nba_game):
        """
        Test 'stat_categories' attribute invocation.
        """
        assert nba_game.stat_categories[0].stat_id == 0
        assert nba_game.stat_categories[0].sort_order
        assert nba_game.stat_categories[0].display_name
        assert nba_game.stat_categories[0].name

    def test_position_types(self, nba_game):
        """
        Test 'position_types' attribute invocation.
        """
        assert nba_game.position_types[0].type
        assert nba_game.position_types[0].display_name

    def test_roster_positions(self, nba_game):
        """
        Test 'roster_positions' attribute invocation.
        """
        assert nba_game.roster_positions[0].abbreviation
        assert nba_game.roster_positions[0].position
        assert nba_game.roster_positions[0].display_name

    def test_is_available(self, finished_game):
        """
        Test 'is_available' attribute invocation.
        """
        assert finished_game.is_available is False

    def test_refresh(self, nba_game):
        """
        Test refresh of Game object.
        """
        old_last_updated = nba_game.last_updated
        nba_game.refresh()
        new_last_updated = nba_game.last_updated
        assert old_last_updated != new_last_updated
