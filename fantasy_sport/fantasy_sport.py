from __future__ import absolute_import
from fantasy_sport.roster import Player, Roster, Transaction


class FantasySport(object):
    """FantasySport Class
    """

    url = 'http://fantasysports.yahooapis.com/fantasy/v2/'

    def __init__(self, oauth, fmt=None, use_login=False):
        """Initialize a FantasySport object
        """
        self.oauth = oauth
        self.fmt = 'json' if not fmt else fmt  # JSON as default format
        self.use_login = use_login


    def __repr__(self,):
        return "<{0}> <{1}>".format(self.url, self.fmt)

    def _check_token_validity(self,):
        """Check wether or not the access token is still valid, if not, renews it
        """
        if not self.oauth.token_is_valid():
            self.oauth.refresh_access_token
        return True

    def _get(self, uri):
        """
        """

        if not self.oauth.oauth.base_url :
            self.oauth.oauth.base_url = self.url
        
        self._check_token_validity()

        response = self.oauth.session.get(uri, params={'format': self.fmt})

        return response

    def _put(self, uri, transaction):
        """
        - uri : roster resource uri
        - roster : roster object
        """
        headers = {'Content-Type':'application/xml'}
        #data = roster.to_json() if self.fmt == 'json' else roster.to_xml() # Getting roster xml or json according to self.fmt
        data = transaction.to_xml()
        print data
        
        response = self.oauth.session.put(uri, data=data, headers=headers)
        print response.status_code
        print response.reason
        
        return response
        
    def _rosterput(self, uri, roster):
        """
        - uri : roster resource uri
        - roster : roster object
        """
        headers = {'Content-Type':'application/xml'}
        #data = roster.to_json() if self.fmt == 'json' else roster.to_xml() # Getting roster xml or json according to self.fmt
        data = roster.to_xml()
        print data
        
        response = self.oauth.session.put(uri, data=data, headers=headers)
        print response.status_code
        print response.reason
        
        return response
        
    def _post(self, uri, transaction):
        """
        - uri : roster resource uri
        - transaction : roster object
        """
        headers = {'Content-Type':'application/xml'}
        data = transaction.to_xml()
        
        response = self.oauth.session.post(uri, data=data, headers=headers)
        print response.status_code
        print response.reason
        
        return response
        
    def _delete(self, uri, transaction):
        """
        - uri : roster resource uri
        - transaction : roster object
        """
        headers = {'Content-Type':'application/xml'}
        data = transaction.to_xml()
        
        response = self.oauth.session.delete(uri, data=data, headers=headers)
        print response.status_code
        print response.reason
        
        return response

    def _add_login(self, uri):
        """Add users;use_login=1/ to the uri
        """
        uri = "users;use_login=1/{0}".format(uri)

        return uri

    def _format_resources_key(self, keys):
        """Format resources keys 
        """
        if isinstance(keys, str):
            return keys
        else:
            return ','.join(str(e) for e in keys)
        
    def _build_uri(self, resources, keys, sub=None):
        """Build uri
        """
        if resources:
            uri = "{0}={1}".format(resources, self._format_resources_key(keys))
        elif not resources and not keys:
            uri = self.url
        else:
           uri = '{0}'.format(self._format_resources_key(keys))
       
        if sub and not resources and not keys:
            uri +="{0}".format(sub)
        elif sub and isinstance(sub, str):
            uri += "/{0}".format(sub)
        elif sub and not isinstance(sub, str):
            uri += ";out={0}".format(','.join([e for e in sub]))

        if self.use_login:
            uri = self._add_login(uri)
            
        print "uri is %s" % uri
        return uri

    def get_collections(self, resource_type, resource_ids, sub_resources):
        """Generic method to get collections
        """
        uri = self._build_uri(resource_type, resource_ids, sub=sub_resources)
        response = self._get(uri)
        return response

    #################################
    #
    #           GAMES
    #
    #################################

    def get_games_info(self, game_keys, leagues=None, teams=False, players=None):
        """Return game info
        >>> yfs.get_games_info('mlb')
        Must set use_login to True to pull teams data
        """
        uri = self._build_uri('games;game_keys', game_keys)
        
        if leagues:
            uri += '/leagues;league_keys={0}'.format(leagues)
        
        if teams:
            uri += '/teams'
            
        if players:
            uri += '/players;player_keys={0}'.format(players)
            
        response = self._get(uri)

        return response


    ####################################
    #
    #           LEAGUES 
    #
    ####################################
    def get_leagues(self, league_keys):
        """Return league data
        >>> yfs.get_leagues(['league_key'])
        """     
        uri = self._build_uri('leagues;league_keys',league_keys)
        response = self._get(uri)
        return response

    def get_leagues_teams(self, league_keys):
        """Return leagues teams
        >>> yfs.get_leagues_teams(['238.l.627062'])
        """
        uri = self._build_uri('leagues;league_keys', league_keys, sub='teams')
        response = self._get(uri)
        return response
        
    def get_leagues_players(self, league_keys):
        """Return leagues players
        >>> yfs.get_leagues_teams(['238.l.627062'])
        """
        uri = self._build_uri('leagues;league_keys', league_keys, sub='players')
        response = self._get(uri)
        return response    

    def get_leagues_scoreboard(self, league_keys, week=None):
        """Return leagues scoreboard
        >>> yfs.get_leagues_scoreboard(['league_key'])
        """
        uri = self._build_uri('leagues;league_keys',league_keys, sub='scoreboard')

        if week:
            uri += ';week={0}'.format(week)

        response = self._get(uri)
        return response

    def get_leagues_settings(self, league_keys):
        """Return leagues settings
        >>> yfs.get_leagues_settings(['238.l.627062','238.l.627062'])
        """
        uri = self._build_uri('leagues;league_keys', league_keys, sub='settings')
        response = self._get(uri)
        return response

    def get_leagues_standings(self, league_keys, teams=None, players=None):
        """Return leagues settings
        >>> yfs.get_leagues_settings(['238.l.627062','238.l.627062'])
        """
        uri = self._build_uri('leagues;league_keys', league_keys, sub='standings')
        
        if teams:
            uri += '/teams/{0}'.format(teams)
            
        if teams=='roster' and players:
            uri += '/players/{0}'.format(players)
        
        response = self._get(uri)
        return response

    def get_leagues_transactions(self, league_keys):
        """Return leagues settings
        >>> yfs.get_leagues_transactions(['238.l.627062'])
        """
        uri = self._build_uri('leagues;league_keys', league_keys, sub='transactions')
        response = self._get(uri)
        return response

    def get_leagues_draftresults(self, league_keys):
        """Return leagues draftresults
        >>> yfs.get_leagues_draftresults(['238.l.627062'])
        """
        uri = self._build_uri('leagues;league_keys', league_keys, sub='draftresults')
        response = self._get(uri)
        return response


    #########################################
    #
    #       PLAYERS (not league specific)
    #
    #########################################
    
    def get_players(self, player_keys, filters=None):
        """Return player data
        >>> yfs.get_players(['player_key'])
        """     
        uri = self._build_uri('players;player_keys', player_keys)
        
        if filters and isinstance(filters, str):
            uri += ';{0}'.format(filters)
        if filters and not isinstance(filters, str):
            uri += ";{0}".format(','.join([e for e in filters]))

        response = self._get(uri)
        return response
        
    def get_players_stats(self, player_keys, week=None):
        """Return player stats (not league specific)
        >>> yfs.get_players_stats(['223.p.5479'], week=3)
        """     
        uri = self._build_uri('players;player_keys', player_keys, sub='stats')
        
        if week:
            uri += ';type=week;week={0}'.format(week)
        
        response = self._get(uri)
        return response
        
    def get_players_percent_owned(self, player_keys):
        """Return ownership percentage of player (not league specific)
        >>> yfs.get_players_percent_owned([223.p.5479])
        """     
        uri = self._build_uri('players;player_keys', player_keys, sub='percent_owned')
        response = self._get(uri)
        return response
          
    def get_players_draft_analysis(self, player_keys):
        """Return draft metrics for player (not league specific)
        >>> yfs.get_players_draft_analysis([223.p.5479])
        """     
        uri = self._build_uri('players;player_keys', player_keys, sub='draft_analysis')
        response = self._get(uri)
        return response

    ###################################
    #
    #           TEAMS
    #   
    ###################################
    
    
    def get_teams(self, team_keys):
        """Return team data
        >>> yfs.get_teams(['league_key'])
        """     
        uri = self._build_uri('teams;team_keys',team_keys)
        response = self._get(uri)
        return response
        
    def get_teams_players(self, team_keys):
        """Return teams players
        >>> yfs.get_teams_players(['238.l.627062'])
        """
        uri = self._build_uri('teams;team_keys', team_keys, sub='players')
        response = self._get(uri)
        return response        
        
    def get_teams_stats(self, team_keys, week=None):
        """Return team stats (week only for H2H league)
        >>> yfs.get_teams_stats(['238.l.627062.t.1'], week=3)
        """     
        uri = self._build_uri('teams;team_keys',team_keys, sub='stats')
        
        if week:
            uri += ';type=week;week={0}'.format(week)
        
        response = self._get(uri)
        return response
    
    def get_teams_standings(self, team_keys):
        """Return team standings
        >>> yfs.get_teams_standings(['238.l.627062.t.1'])
        """     
        uri = self._build_uri('teams;team_keys',team_keys, sub='standings')
        response = self._get(uri)
        return response
        
    def get_teams_roster(self, team_keys, week=None, players=None, filters=None):
        """Return team roster
        >>> yfs.get_teams_roster(['238.l.627062.t.1'], week=3)
        """     
        uri = self._build_uri('teams;team_keys',team_keys, sub='roster')
            
        if week:
            uri += ';week={0}'.format(week)
        
        if players and filters:
            uri += '/players;{1}/{0}'.format(filters, players)
            
        elif filters and not players:
            uri += '/players;{0}'.format(filters) 
            
        elif players and not filters:
             uri += '/players/{0}'.format(players)    
        
        response = self._get(uri)
        return response
        
    def get_teams_draftresults(self, team_keys):
        """Return a team's draft results
        >>> yfs.get_teams_draftresults(['238.l.627062.t.1'])
        """     
        uri = self._build_uri('teams;team_keys',team_keys, sub='draftresults')
        response = self._get(uri)
        return response
        
    def get_teams_matchups(self, team_keys, weeks=None):
        """Return team matchups (H2H leagues only)
        >>> yfs.get_teams_matchups(['238.l.627062.t.1'], weeks='1,3,6')
        """     
        uri = self._build_uri('teams;team_keys',team_keys, sub='matchups')
        
        if weeks and isinstance(weeks, str):   
            uri += ';weeks={0}'.format(weeks)    
        if weeks and not isinstance(weeks, str):
            uri += ";weeks{0}".format(','.join([e for e in weeks]))
            
        response = self._get(uri)
        return response
        
        
        
    ##############################################
    #
    #    ROSTERS (team specific player info)
    #
    ##############################################
    
    def get_roster_players(self, team_keys, week=None, date=None):
        """Access roster info, with player sub option
        >>> yfs.get_roster_players(['238.l.627062'])
        """
        
        uri = self._build_uri(None, team_keys, sub='roster')
        uri = 'team/{0}'.format(uri) # Done to avoid having 'team=238.l.627062', which doesn't work for this resource

        if week: 
            uri += ';week={0}'.format(week)
        if date:
            uri += ';date={0}'.format(date)

        response = self._get(uri)
        return response 

    #def set_roster_players(self, team_keys, roster):
        """
        >>> from fantasy_sport import Roster, Player
        >>> p1 = Player('242.p.8332','WR')
        >>> p2 = Player('242.p.8334','WL')
        >>> roster = Roster([p1, p2], date='2015-01-11')
        >>> yfs.set_roster_players(['238.l.627062.t.1'], roster)
        """
        #uri = self._build_uri(None, team_keys, sub='roster')
        #uri = 'team/{0}'.format(uri)

        #response = self._put(uri, roster)
        #return response 
        
    def set_roster_players(self, player_key1, pos1, player_key2, pos2, team_keys, date):
        """
        >>> Description to follow
        """
        uri = self._build_uri(None, team_keys, sub='roster')
        uri = 'team/{0}'.format(uri)
        
        p1 = Player(player_key1, position=pos1)
        p2 = Player(player_key2, position=pos2)
        
        roster = Roster(players=[p1,p2], date=date)
        
        response = self._rosterput(uri, roster)
        return response
        
        
    ##############################################
    #
    #    TRANSACTIONS
    #
    ##############################################
    
    ### GET Functions
    
    def get_transactions(self, transaction_keys, players=None):
        """Return transaction data
        >>> yfs.get_transaction(['transaction_key'])
        """ 
        
        if players:
            subtext = 'players/{0}'.format(players)    
            uri = self._build_uri('transactions;transaction_keys', transaction_keys, sub=subtext)
        else:
            uri = self._build_uri('transactions;transaction_keys', transaction_keys)
            
        response = self._get(uri)
        return response
        
    def get_all_completed_leagues_transactions(self, league_keys):
        """Return all transactions from multiple leagues
        >>>yfs.get_all_completed_leagues_transactions(['league_key1', 'leaguekey2'])
        """
        
        uri = self._build_uri('leagues;league_keys', league_keys, sub='transactions')
        response = self._get(uri)
        return response
        
    def get_teams_pending_transactions(self, league_key, team_key):
        """Return pending transactions for a specific team
        >>> yfs.get_teams_pending_transactions('league_key', 'team_key')
        """
        
        uri = self._build_uri(None, 'league/{0}'.format(league_key), sub='transactions')
        uri += ';types=waiver,pending_trade;team_key={0}'.format(team_key)
        
        response = self._get(uri)
        return response
        
        
    ### PUT Functions
        
    def edit_waiver(self, transaction_key, priority, faab_bid):
        """
        Adjust the priority or faab_bid of a pending waiver
        >>> from fantasy_sport import Transaction
        >>> yfs.edit_waiver(transaction_key='248.l.55438.w.c.2_6093', priority='1', faab_bid='20')
        """
        uri = self._build_uri(None, None, sub='transaction')
        
        transaction = Transaction(type='waiver', transaction_key=transaction_key, priority=priority, faab_bid=faab_bid)

        response = self._put(uri, transaction)
        return response
        
    def accept_trade(self, transaction_key, trade_note=None):
        """
        Accept a trade
        >>> from fantasy_sport import Transaction
        >>> yfs.accept_trade(transaction_key='248.l.55438.pt.11', trade_note='Great offer')
        """
        uri = self._build_uri(None, None, sub='transaction')
        
        transaction = Transaction(type='pending_trade', transaction_key=transaction_key, action='accept', trade_note=trade_note)

        response = self._put(uri, transaction)
        return response
        
    def reject_trade(self, transaction_key, trade_note=None):
        """
        Reject a trade
        >>> from fantasy_sport import Transaction
        >>> yfs.reject_trade(transaction_key='248.l.55438.pt.11', trade_note='Terrible offer')
        """
        uri = self._build_uri(None, None, sub='transaction')
        
        transaction = Transaction(type='pending_trade', transaction_key=transaction_key, action='reject', trade_note=trade_note)

        response = self._put(uri, transaction)
        return response
        
    def allow_trade(self, transaction_key):
        """
        Allow a trade
        >>> from fantasy_sport import TransactionPut
        >>> yfs.allow_trade(transaction_key='248.l.55438.pt.11')
        """
        uri = self._build_uri(None, None, sub='transaction')
        
        transaction = Transaction(type='pending_trade', transaction_key=transaction_key, action='allow')

        response = self._put(uri, transaction)
        return response
        
    def disallow_trade(self, transaction_key):
        """
        Disallow a trade
        >>> from fantasy_sport import TransactionPut
        >>> yfs.disallow_trade(transaction_key='248.l.55438.pt.11')
        """
        uri = self._build_uri(None, None, sub='transaction')
        
        transaction = TransactionPut(type='pending_trade', transaction_key=transaction_key, action='disallow')

        response = self._put(uri, transaction)
        return response
        
    def vote_against_trade(self, transaction_key, voter_team_key):
        """
        Vote against a trade
        >>> from fantasy_sport import TransactionPut
        >>> yfs.vote_against_trade(transaction_key='248.l.55438.t.2', voter_team_key='248.l.55438.t.2')
        """
        uri = self._build_uri(None, None, sub='transaction')
        
        transaction = Transaction(type='pending_trade', transaction_key=transaction_key, action='vote_against', voter_team_key=voter_team_key)

        response = self._put(uri, transaction)
        return response
        
    ### POST Functions
    
    def make_roster_move(self, league_keys, roster):
        """
        Add, drop, or add & drop a player
        >>> from fantasy_sport import Transaction
        >>> roster = Transaction(type='add/drop', add_player_key='346.p.9171')
        >>> yfs.make_roster_move(['346.l.1328'], roster)
        """
        uri = self._build_uri(None, league_keys, sub='roster')
        uri = 'league/{0}'.format(uri)
        return response 
    
    def add_player(self, player_keys, team_key, league_key):
        """
        Add a player to your team
        Three things to specify are player key, team key, league key
        yfs.add_player('346.p.9171', '346.l.1328.t.12', ['346.l.1328'])
        """
        uri = self._build_uri(None, league_key, sub='transactions')
        uri = 'league/{0}'.format(uri)
        
        p1 = Player(player_keys, type='add', destination_team_key=team_key)
        transaction = Transaction('add', players=[p1])
        
        response = self._post(uri, transaction)
        return response
        
    def drop_player(self, player_keys, team_key, league_key):
        """
        Drop a player from your team
        Three things to specify are player key, team key, league key
        yfs.drop_player('346.p.9171', '346.l.1328.t.12', ['346.l.1328'])
        """
        uri = self._build_uri(None, league_key, sub='transactions')
        uri = 'league/{0}'.format(uri)
        
        p1 = Player(player_keys, type='drop', source_team_key=team_key)
        transaction = Transaction('drop', players=[p1])
        
        response = self._post(uri, transaction)
        return response
    
    def add_and_drop_player(self, add_player_key, drop_player_key, team_key, league_key, faab_bid=None):
        """
        Add and drop a player from your team
        Three things to specify are player key, team key, league key
        and optionally a faab_bid if player is on waivers
        yfs.add_and_drop_player('346.p.9171', '346.l.1328.t.12', ['346.l.1328'], faab_bid='20')
        """
        uri = self._build_uri(None, league_key, sub='transactions')
        uri = 'league/{0}'.format(uri)
        
        p1 = Player(add_player_key, type='add', destination_team_key=team_key)
        p2 = Player(drop_player_key, type='drop', source_team_key=team_key)
        transaction = Transaction('add/drop', players=[p1,p2], faab_bid=faab_bid)
        
        response = self._post(uri, transaction)
        return response
        
    def propose_trade(self, give_player_keys, get_player_keys, trader_team_key, tradee_team_key, league_key, trade_note=None):
        """
        Add and drop a player from your team
        Three things to specify are player key, team key, league key
        and optionally a faab_bid if player is on waivers
        yfs.add_and_drop_player('346.p.9171', '346.l.1328.t.12', ['346.l.1328'], faab_bid='20')
        """
        uri = self._build_uri(None, league_key, sub='transactions')
        uri = 'league/{0}'.format(uri)
        
        p1 = Player(give_player_keys, type='pending_trade', source_team_key=trader_team_key, destination_team_key=tradee_team_key)
        p2 = Player(get_player_keys, type='pending_trade', source_team_key=tradee_team_key, destination_team_key=trader_team_key)
        transaction = Transaction('pending_trade', players=[p1,p2], trader_team_key=trader_team_key, tradee_team_key=tradee_team_key, trade_note=trade_note)
        
        response = self._post(uri, transaction)
        return response
        
    ##  DELETE functions
    
    def delete_waiver(self, transaction_key, priority, faab_bid):
        """
        Delete a pending waiver
        >>> from fantasy_sport import Transaction
        >>> yfs.delete_waiver(transaction_key='248.l.55438.w.c.2_6093', priority='1', faab_bid='20')
        """
        uri = self._build_uri(None, None, sub='transaction')
        
        transaction = Transaction(type='waiver', transaction_key=transaction_key, priority=priority, faab_bid=faab_bid)

        response = self._delete(uri, transaction)
        return response
        
        
        
