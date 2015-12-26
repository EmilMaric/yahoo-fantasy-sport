from __future__ import absolute_import

from .resource import Resource
from .collection import Collection
from .errors import YahooFantasySportsError
from .utils import build_uri, yfs_request

import arrow

from requests import HTTPError


class GamesFactory(object):
    """
    Factory class for creating Games collections or Game resource objects.
    """

    def __init__(self, oauth):
        self._oauth = oauth

    def __call__(self, game_keys=None, is_available=None, game_types=None,
                 game_codes=None, seasons=None):
        # validate inputs
        if not isinstance(game_keys, list) and game_keys is not None:
            raise YahooFantasySportsError("'game_keys' must be a 'list'")

        if is_available is not True and is_available is not False and \
           is_available is not None:
            raise YahooFantasySportsError("'is_available' must be 'True'"
                                          "or 'False'")

        if not isinstance(game_types, list) and game_types is not None:
            raise YahooFantasySportsError("'game_types' must be a 'list'")

        if not isinstance(game_codes, list) and game_codes is not None:
            raise YahooFantasySportsError("'game_codes' must be a 'list'")

        if not isinstance(seasons, list) and seasons is not None:
            raise YahooFantasySportsError("'seasons' must be a 'list'")

        for key in game_keys:
            if not isinstance(key, str) and not isinstance(key, int):
                raise KeyError(
                    "'{0}' must be either a string or integer".format(key))

        return Games(self._oauth, game_keys=game_keys,
                     is_available=is_available, game_types=game_types,
                     game_codes=game_codes, seasons=seasons)


class Games(Collection):
    """
    Games Collection.
    """
    collection = "games"

    def __init__(self, oauth, game_keys=None, is_available=None,
                 game_types=None, game_codes=None, seasons=None):
        self._oauth = oauth
        self._games = {}

        # build up the parameters for the URI
        params = {}
        if game_keys:
            params['game_keys'] = ','.join(str(key) for key in game_keys)
        if is_available:
            params['is_available'] = 1
        if game_types:
            params['game_types'] = ','.join(game_types)
        if game_codes:
            params['game_codes'] = ','.join(game_codes)
        if seasons:
            params['seasons'] = ','.join(seasons)

        uri = build_uri(self.collection, parameters=params)
        games = yfs_request(self._oauth, uri)['fantasy_content']['games']

        # iterate through the resonse and build a Game resource object for
        # each returned Game
        for idx in games:
            if idx == 'count':
                continue

            game = games[idx]
            # the response does not always return the Game resource object
            # in the same format, so have a case to handle the different
            # response formats
            if isinstance(game['game'], list):
                game_key = game['game'][0]['game_key']
            elif isinstance(game['game'], dict):
                game_key = game['game']['game_key']
            else:
                raise YahooFantasySportsError('Invalid response.')

            game = Game(self._oauth, game_key)
            # if ``is_available`` is defined as ``False``, and game is
            # available, then do not add it
            if is_available is False and game.is_available:
                continue
            self._games[int(game_key)] = Game(self._oauth, game_key)

        self._last_updated = arrow.utcnow().format('YYYY-MM-DD HH:mm:ss ZZ')

    def __repr__(self):
        return "<{0} {1}>".format(
                self.__class__.__name__, str(self._games))

    def __getitem__(self, key):
        return self._games[key]

    def __len__(self):
        return len(self._games)

    def refresh(self):
        """
        Refreshes the entire object to contain the latest data from the Yahoo
        servers.
        """
        for game in self._games:
            game.refresh()

    @property
    def keys(self):
        return self._games.keys()

    @property
    def last_updated(self):
        return self._last_updated


class Game(Resource):
    """
    Game Resource
    """
    resource = "game"

    def __init__(self, oauth, game_key):
        self._oauth = oauth
        self._game_key = game_key
        self.refresh()

    def refresh(self):
        """
        Refreshes the entire object to contain the latest data from the Yahoo
        servers.
        """
        self._refresh_meta()
        self._refresh_game_weeks()
        self._refresh_stat_categories()
        self._refresh_position_types()
        self._refresh_roster_positions()
        self._refresh_is_available()
        self._last_updated = arrow.utcnow().format('YYYY-MM-DD HH:mm:ss ZZ')

    def _refresh_meta(self):
        uri = build_uri(self.resource, resource_key=self._game_key)

        metadata = yfs_request(self._oauth, uri)['fantasy_content']['game']
        if isinstance(metadata, list):
            metadata = metadata[0]

        self._game_key = int(metadata['game_key'])
        self._game_id = int(metadata['game_id'])
        self._code = metadata['code']
        self._name = metadata['name']
        self._url = metadata['url']
        self._season = metadata['season']
        self._is_registration_over = True if metadata['is_registration_over'] \
            else False
        self._type = metadata['type']

    def _refresh_game_weeks(self):
        self._game_weeks = {}
        uri = build_uri(self.resource, resource_key=self._game_key,
                        sub='game_weeks')

        try:
            weeks = yfs_request(self._oauth, uri)['fantasy_content']['game']
        except HTTPError:
            return

        if isinstance(weeks, list):
            weeks = weeks[1]

        weeks = weeks['game_weeks']

        for week_no, week in weeks.iteritems():
            # skip 'count' field
            if week_no == 'count':
                continue

            start = week['game_week']['start']
            end = week['game_week']['end']
            number = int(week['game_week']['week'])
            self._game_weeks[number] = GameWeek(number, start, end)

    def _refresh_stat_categories(self):
        self._stat_categories = []
        uri = build_uri(self.resource, resource_key=self._game_key,
                        sub='stat_categories')
        try:
            stats = yfs_request(self._oauth, uri)['fantasy_content']['game'][1]
        except HTTPError:
            return

        stats = stats['stat_categories']['stats']

        for stat in stats:
            stat_id = stat['stat']['stat_id']
            sort_order = stat['stat']['sort_order']
            display_name = stat['stat']['display_name']
            name = stat['stat']['name']

            position_types = []
            if 'position_types' in stat['stat']:
                for position_type in stat['stat']['position_types']:
                    position_types.append(position_type['position_type'])

            stat_category = GameStatCategory(stat_id, sort_order,
                                             display_name, name,
                                             position_types)
            self._stat_categories.append(stat_category)

    def _refresh_position_types(self):
        self._position_types = []
        uri = build_uri(self.resource, resource_key=self._game_key,
                        sub='position_types')
        try:
            position_types = yfs_request(self._oauth, uri)['fantasy_content']
        except HTTPError:
            return

        position_types = position_types['game'][1]['position_types']

        for position_type in position_types:
            type = position_type['position_type']['type']
            display_name = position_type['position_type']['display_name']
            player_position = GamePlayerPosition(type, display_name)
            self._position_types.append(player_position)

    def _refresh_roster_positions(self):
        self._roster_positions = []
        uri = build_uri(self.resource, resource_key=self._game_key,
                        sub='roster_positions')

        try:
            roster_positions = yfs_request(self._oauth, uri)['fantasy_content']
        except HTTPError:
            return

        roster_positions = roster_positions['game'][1]['roster_positions']

        for roster_position in roster_positions:
            rp = roster_position['roster_position']
            abbreviation = rp['abbreviation']
            position = rp['position']
            display_name = rp['display_name']
            position_type = rp['position_type'] \
                if 'position_type' in rp else None
            roster_position = GameRosterPosition(abbreviation, position,
                                                 display_name, position_type)
            self._roster_positions.append(roster_position)

    def _refresh_is_available(self):
        uri = build_uri(self.resource + 's',
                        parameters={'game_keys': self._game_key,
                                    'is_available': 1})
        response = \
            yfs_request(self._oauth, uri)['fantasy_content']['games']
        self._is_available = True if response else False

    @property
    def game_key(self):
        return self._game_key

    @property
    def game_id(self):
        return self._game_id

    @property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

    @property
    def season(self):
        return self._season

    @property
    def is_registration_over(self):
        return self._is_registration_over

    @property
    def type(self):
        return self._type

    @property
    def game_weeks(self):
        return self._game_weeks

    @property
    def stat_categories(self):
        return self._stat_categories

    @property
    def position_types(self):
        return self._position_types

    @property
    def roster_positions(self):
        return self._roster_positions

    @property
    def is_available(self):
        return self._is_available

    @property
    def last_updated(self):
        return self._last_updated


class GameWeek(object):
    """
    Represents a Yahoo Fantasy Sports Game Week.
    """

    def __init__(self, week, start, end):
        self._week = week
        self._start = start
        self._end = end

    def __repr__(self):
        return "<{0} '{1}'>".format(self.__class__.__name__, self._week)

    @property
    def week(self):
        return self._week

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end


class GameStatCategory(object):
    """
    Represents a Yahoo Fantasy Sports Stat Category.
    """

    def __init__(self, stat_id, sort_order, display_name, name,
                 position_types=None):
        self._stat_id = stat_id
        self._sort_order = sort_order
        self._display_name = display_name
        self._name = name
        self._position_types = position_types

    def __repr__(self):
        return "<{0} '{1}'>".format(self.__class__.__name__,
                                    self._display_name)

    @property
    def stat_id(self):
        return self._stat_id

    @property
    def sort_order(self):
        return self._sort_order

    @property
    def display_name(self):
        return self._display_name

    @property
    def name(self):
        return self._name

    @property
    def position_types(self):
        return self._position_types


class GamePlayerPosition(object):
    """
    Represents a Yahoo Fantasy Sports Player Position.
    """

    def __init__(self, type, display_name):
        self._type = type
        self._display_name = display_name

    def __repr__(self):
        return "<{0} '{1}'>".format(self.__class__.__name__, self._type)

    @property
    def type(self):
        return self._type

    @property
    def display_name(self):
        return self._display_name


class GameRosterPosition(object):
    """
    Represents a Yahoo Fantasy Sports Roster Position.
    """

    def __init__(self, abbreviation, position, display_name,
                 position_type=None):
        self._abbreviation = abbreviation
        self._position = position
        self._display_name = display_name
        self._position_type = position_type

    def __repr__(self):
        return "<{0} '{1}'>".format(self.__class__.__name__,
                                    self._abbreviation)

    @property
    def abbreviation(self):
        return self._abbreviation

    @property
    def position(self):
        return self._position

    @property
    def display_name(self):
        return self._display_name

    @property
    def position_type(self):
        return self._position_type
