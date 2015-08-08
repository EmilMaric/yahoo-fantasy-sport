import pdb
import json
import logging
import unittest

from xml.etree import cElementTree as ctree

from yahoo_oauth import OAuth1

from fantasy_sport import FantasySport
from fantasy_sport.roster import Player, Roster, Transaction
from fantasy_sport.utils import pretty_json, pretty_xml

logging.getLogger('yahoo_oauth').setLevel(logging.WARNING)

logging.basicConfig(level=logging.DEBUG,format="[%(asctime)s %(levelname)s] [%(name)s.%(module)s.%(funcName)s] %(message)s \n")
logging.getLogger('test-fantasy-sports')

class TestFantasySportGame(unittest.TestCase):

    def setUp(self,):
        oauth = OAuth1(None, None, from_file='oauth.json',base_url='http://fantasysports.yahooapis.com/fantasy/v2/')
        self.yfs = FantasySport(oauth)
    
    def test_get_games_info(self,):
        response = self.yfs.get_games_info(['346'])
        #response = self.yfs.get_games_info(['nfl'])
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
        
    def test_get_games_withleague(self,):
        response = self.yfs.get_games_info(['328'], leagues='328.l.56628')
        self.assertEqual(response.status_code, 200)
        #logging.debug(pretty_json(response.content))
        
    def test_get_games_withplayer(self,):
        response = self.yfs.get_games_info(['328'], players='328.p.8180')
        self.assertEqual(response.status_code, 200)
        #logging.debug(pretty_json(response.content))
        
    def test_get_games_with_login_teams(self,):
        self.yfs.use_login = True
        response = self.yfs.get_games_info(['346'], teams=True)
        self.yfs.use_login = False
        self.assertEqual(response.status_code, 200)
        #logging.debug(pretty_json(response.content))          
        
    def test_get_games_info_with_login(self,):
        self.yfs.use_login = True
        response = self.yfs.get_games_info(['mlb'])
        self.yfs.use_login = False
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
        
class TestFantasySportLeague(unittest.TestCase):

    def setUp(self,):
        oauth = OAuth1(None, None, from_file='oauth.json',base_url='http://fantasysports.yahooapis.com/fantasy/v2/')
        self.yfs = FantasySport(oauth)

    def test_get_leagues(self):
        response = self.yfs.get_leagues(['346.l.1328'])
        self.assertEqual(response.status_code, 200)
        #logging.debug(pretty_json(response.content))

    def test_get_leagues_with_multiple_keys(self,):
        self.yfs.fmt = 'xml'
        response = self.yfs.get_leagues(('238.l.627060','238.l.627062'))
        self.yfs.fmt = 'json'
        self.assertEqual(response.status_code, 200)
        #logging.debug(pretty_xml(response.content))

    def test_get_leagues_scoreboard(self):
        response = self.yfs.get_leagues_scoreboard(['346.l.1328'])
        self.assertEqual(response.status_code, 200)
        #logging.debug(pretty_json(response.content))

    def test_get_leagues_scoreboard_week_2(self):
        response = self.yfs.get_leagues_scoreboard(['238.l.178574'], week=2)
        self.assertEqual(response.status_code, 200)
        #logging.debug(pretty_json(response.content))

    def test_get_leagues_settings(self):
        response = self.yfs.get_leagues_settings(['238.l.627060','238.l.627062'])
        self.assertEqual(response.status_code, 200)
        #logging.debug(pretty_json(response.content))

    def test_get_leagues_standings(self):
        response = self.yfs.get_leagues_standings(['346.l.1328'])
        self.assertEqual(response.status_code, 200)
        #logging.debug(pretty_json(response.content))
        
    def test_get_leagues_standings_withteam_androsterplayers(self):
        response = self.yfs.get_leagues_standings(['346.l.1328'], teams='roster', players='ownership')
        self.assertEqual(response.status_code, 200)
        #logging.debug(pretty_json(response.content))

    def test_get_leagues_transactions(self):
        response = self.yfs.get_leagues_transactions(['238.l.627060','238.l.627062'])
        self.assertEqual(response.status_code, 200)
        #logging.debug(pretty_json(response.content))

    def test_get_leagues_teams(self,):
        response = self.yfs.get_leagues_teams(['238.l.627060'])
        self.assertEqual(response.status_code, 200)
        #logging.debug(pretty_json(response.content))

    def test_get_leagues_draftresults(self,):
        response = self.yfs.get_leagues_draftresults(['238.l.627060'])
        self.assertEqual(response.status_code, 200)
        #logging.debug(pretty_json(response.content))

    def test_get_collections(self,):
        response = self.yfs.get_collections('leagues;league_keys', ['238.l.627060','238.l.627062'],['settings','standings'])
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
        
class TestFantasySportPlayer(unittest.TestCase):

    def setUp(self,):
        oauth = OAuth1(None, None, from_file='oauth.json',base_url='http://fantasysports.yahooapis.com/fantasy/v2/')
        self.yfs = FantasySport(oauth)
        
    def test_get_players(self,):
        response = self.yfs.get_players(['223.p.5479'])
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
        
    def test_get_playerswithfilter(self,):
        response = self.yfs.get_players(['346.p.8180', '346.p.8544'], filters='position=P')
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
        
    def test_get_players_stats(self,):
        response = self.yfs.get_players_stats(['223.p.5479'], week=3)
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)    
        
    def test_get_players_draft_analysis(self,):
        response = self.yfs.get_players_draft_analysis(['44.p.6619'])
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
    
    def test_get_players_percent_owned(self,):
        response = self.yfs.get_players_percent_owned(['253.p.6619'])
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
        
class TestFantasySportTeam(unittest.TestCase):

    def setUp(self,):
        oauth = OAuth1(None, None, from_file='oauth.json',base_url='http://fantasysports.yahooapis.com/fantasy/v2/')
        self.yfs = FantasySport(oauth)
        
    def test_get_teams(self,):
        response = self.yfs.get_teams(['346.l.1328.t.12'])
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
        
    def test_get_teams_players(self,):
        response = self.yfs.get_teams_players(['346.l.1328.t.12'])
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
        
    def test_get_teams_stats(self,):
        response = self.yfs.get_teams_stats(['238.l.627062.t.1'], week=10)
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
        
    def test_get_teams_standings(self,):
        response = self.yfs.get_teams_standings(['346.l.1328.t.12'])
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
        
    def test_get_teams_roster(self,):
        response = self.yfs.get_teams_roster(['346.l.1328.t.12'])
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)

    #def test_get_teams_roster_with_filter(self,):
    #    response = self.yfs.get_teams_roster(['346.l.1328.t.12'], players='draft_analysis', filters='position=3B')
    #    #logging.debug(pretty_json(response.content))
    #    self.assertEqual(response.status_code, 200)
        
    def test_get_teams_roster_week(self,):
        response = self.yfs.get_teams_roster(['223.l.431.t.9'], week=1)
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
        
    def test_get_teams_roster_weekplayer(self,):
        response = self.yfs.get_teams_roster(['223.l.431.t.9'], week=1, players='draft_analysis')
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)    
                
    def test_get_teams_roster_players(self,):
        response = self.yfs.get_teams_roster(['346.l.1328.t.12'], players='metadata')
        logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
        
    def test_get_teams_roster_filter(self,):
        response = self.yfs.get_teams_roster(['346.l.1328.t.12'], filters='position=3B')
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
   
    def test_get_teams_draftresults(self,):
        response = self.yfs.get_teams_draftresults(['346.l.1328.t.12'])
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
        
    def test_get_teams_matchups(self,):
        response = self.yfs.get_teams_matchups(['238.l.627062.t.1'], weeks=['1,2'])
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)

class TestFantasySportRoster(unittest.TestCase):

    def setUp(self,):
        oauth = OAuth1(None, None, from_file='oauth.json', base_url='http://fantasysports.yahooapis.com/fantasy/v2/')
        self.yfs = FantasySport(oauth)

    def test_get_roster_players(self,):
        response = self.yfs.get_roster_players(['346.l.1328.t.12'])
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)

    def test_get_roster_players_by_week(self,):
        response = self.yfs.get_roster_players(['346.l.1328.t.12'], week=10)
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
        
    def test_get_roster_players_by_date(self,):
        response = self.yfs.get_roster_players(['346.l.1328.t.12'], date='2011-05-01')
        #logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)   

    #def test_set_roster_players(self,):
    #    response = self.yfs.set_roster_players(['346.l.1328.t.12'])
    #    self.assertEqual(response.status_code, 200)
        
"""
class TestFantasySportTransaction(unittest.TestCase):

    def setUp(self,):
        oauth = OAuth1(None, None, from_file='oauth.json',base_url='http://fantasysports.yahooapis.com/fantasy/v2/')
        self.yfs = FantasySport(oauth)
        
    def test_get_transactions(self,):
        response = self.yfs.get_transactions(['346.l.1328.tr.100'], players=None)
        logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
        
    def test_get_all_completed_leagues_transactions(self,):
        response = self.yfs.get_all_completed_leagues_transactions(['346.l.1328'])
        logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
        
    def test_add_player(self,):
        response = self.yfs.add_player('346.p.9723', '346.l.1328.t.12', ['346.l.1328'])
        logging.debug(pretty_xml(response.content))
        self.assertEqual(response.status_code, 201)
"""        
        
class TestFantasySportRoster(unittest.TestCase):

    def setUp(self,):
        oauth = OAuth1(None, None, from_file='oauth.json', base_url='http://fantasysports.yahooapis.com/fantasy/v2/')
        self.yfs = FantasySport(oauth)

    def test_get_roster_players(self,):
        response = self.yfs.get_roster_players(['346.l.1328.t.12'])
        logging.debug(pretty_json(response.content))
        self.assertEqual(response.status_code, 200)
        

class TestPlayer(unittest.TestCase):

    def setUp(self,):
        self.player = Player('242.p.8332','WR')

    def test_player_in_xml(self,):
        expected = b'<player><player_key>242.p.8332</player_key><position>WR</position></player>'
        logging.debug(pretty_xml(self.player.to_xml()))
        self.assertEqual(expected, self.player.to_xml())

    def test_player_in_json(self,):
        expected = {"player_key": "242.p.8332","position":"WR"}
        logging.debug(pretty_json(self.player.to_json()))
        self.assertEqual(expected, self.player.json)


class TestRoster(unittest.TestCase):

    def setUp(self,):
        players = [Player('242.p.8332', 'WR'), Player('242.p.8334','WL')]
        self.roster = Roster(players, date='2015-01-01')

    def test_roster_in_json(self,):
        expected = {
            'fantasy_content': {
                'roster': {
                    'coverage_type':'date',
                    'date':'2015-01-01',
                    'players':[
                        {"player_key": "242.p.8332","position":"WR"},
                        {"player_key": "242.p.8334","position":"WL"}
                    ]
                }
            }
        }
        logging.debug(pretty_json(self.roster.to_json()))
        self.assertEqual(expected, self.roster.json)

    def test_roster_in_xml(self,):
        expected = b'<fantasy_content><roster><coverage_type>date</coverage_type><date>2015-01-01</date><players><player><player_key>242.p.8332</player_key><position>WR</position></player><player><player_key>242.p.8334</player_key><position>WL</position></player></players></roster></fantasy_content>'
        logging.debug(pretty_xml(self.roster.to_xml()))
        self.assertEqual(expected, self.roster.to_xml())
"""        
class TestPaulRoster(unittest.TestCase):    
    
    def setUp(self,):
        oauth = OAuth1(None, None, from_file='oauth.json', base_url='http://fantasysports.yahooapis.com/fantasy/v2/')
        self.yfs = FantasySport(oauth)
    
    def test_roster_fo_realz(self,):
        players = [Player('346.p.8171', 'OF'), Player('346.p.9719','BN')]
        self.roster = Roster(players, date='2015-07-21')
        response = self.yfs.set_roster_players(['346.l.1328.t.12'], self.roster)
        logging.debug(pretty_xml(response.content))
        self.assertEqual(response.status_code, 201)
        
    def test_add_with_waiver(self,):
        response = self.yfs.add_and_drop_player('346.p.8644', '346.p.9723', '346.l.1328.t.12', '346.l.1328', faab_bid='20')
        #logging.debug(pretty_xml(response.content))
        self.assertEqual(response.status_code, 201)
        
    def test_edit_waiver(self,):
        response = self.yfs.edit_waiver('346.l.1328.w.c.12_8644_9723', '1', faab_bid='40')
        self.assertEqual(response.status_code, 201)
        
    def test_get_pending_transactions(self,):
        response = self.yfs.get_teams_pending_transactions('346.l.1328', '346.l.1328.t.12')
        #logging.debug(pretty_xml(response.content))
        print response.content
        self.assertEqual(response.status_code, 200)
    
    def test_reject_trade(self,):
        response = self.yfs.reject_trade('346.l.1328.pt.61', 'what a terrible, horrible offer. Im so insulted')
        self.assertEqual(response.status_code, 201)
        
    def test_delete_waiver(self,):
        response = self.yfs.delete_waiver('346.l.1328.w.c.12_8922_9723', '1', '5')
        self.assertEqual(response.status_code, 201)
"""

        
class TestTransactionPut(unittest.TestCase):
        

    def test_edit_waiver(self,):
        self.transaction = Transaction(type='waiver', transaction_key='248.l.55438.w.c.2_6093', priority='1', faab_bid='20')
        expected = b'<fantasy_content><transaction><transaction_key>248.l.55438.w.c.2_6093</transaction_key><type>waiver</type><waiver_priority>1</waiver_priority><faab_bid>20</faab_bid></transaction></fantasy_content>'
        logging.debug(pretty_xml(self.transaction.to_xml()))
        self.assertEqual(expected, self.transaction.to_xml())
        
    def test_accept_trade(self,):
        self.transaction = Transaction(type='pending_trade', transaction_key='248.l.55438.pt.11', action='accept', trade_note='Great offer!')
        expected = b'<fantasy_content><transaction><transaction_key>248.l.55438.pt.11</transaction_key><type>pending_trade</type><action>accept</action><trade_note>Great offer!</trade_note></transaction></fantasy_content>'
        logging.debug(pretty_xml(self.transaction.to_xml()))
        self.assertEqual(expected, self.transaction.to_xml())
        
    def test_reject_trade(self,):
        self.transaction = Transaction(type='pending_trade', transaction_key='248.l.55438.pt.11', action='reject', trade_note='Terrible offer!')
        expected = b'<fantasy_content><transaction><transaction_key>248.l.55438.pt.11</transaction_key><type>pending_trade</type><action>reject</action><trade_note>Terrible offer!</trade_note></transaction></fantasy_content>'
        logging.debug(pretty_xml(self.transaction.to_xml()))
        self.assertEqual(expected, self.transaction.to_xml())
        
    def test_allow_trade(self,):
        self.transaction = Transaction(type='pending_trade', transaction_key='248.l.55438.pt.11', action='allow')
        expected = b'<fantasy_content><transaction><transaction_key>248.l.55438.pt.11</transaction_key><type>pending_trade</type><action>allow</action></transaction></fantasy_content>'
        logging.debug(pretty_xml(self.transaction.to_xml()))
        self.assertEqual(expected, self.transaction.to_xml())
        
    def test_vote_against_trade(self,):
        self.transaction = Transaction(type='pending_trade', transaction_key='248.l.55438.pt.11', action='vote_against', voter_team_key='248.l.55438.t.2')
        expected = b'<fantasy_content><transaction><transaction_key>248.l.55438.pt.11</transaction_key><type>pending_trade</type><action>vote_against</action><voter_team_key>248.l.55438.t.2</voter_team_key></transaction></fantasy_content>'
        logging.debug(pretty_xml(self.transaction.to_xml()))
        self.assertEqual(expected, self.transaction.to_xml())
        
class TestTransactionPost(unittest.TestCase):
    
    def test_add_player(self,):
        self.p1 = Player('248.p.522', type='add', destination_team_key='248.l.1328.t.12')
        self.transaction = Transaction('add', players=[self.p1])
        expected = b'<fantasy_content><transaction><type>add</type><player><player_key>248.p.522</player_key><transaction_data><type>add</type><destination_team_key>248.l.1328.t.12</destination_team_key></transaction_data></player></transaction></fantasy_content>'
        logging.debug(pretty_xml(self.transaction.to_xml()))
        self.assertEqual(expected, self.transaction.to_xml())
        
    def test_drop_player(self,):
        self.p1 = Player('248.p.522', type='drop', source_team_key='248.l.1328.t.12')
        self.transaction = Transaction('drop', players=[self.p1])
        expected = b'<fantasy_content><transaction><type>drop</type><player><player_key>248.p.522</player_key><transaction_data><type>drop</type><source_team_key>248.l.1328.t.12</source_team_key></transaction_data></player></transaction></fantasy_content>'
        logging.debug(pretty_xml(self.transaction.to_xml()))
        self.assertEqual(expected, self.transaction.to_xml())
        
    def test_adddrop_player(self,):
        self.p1 = Player('248.p.522', type='add', destination_team_key='248.l.1328.t.12')
        self.p2 = Player('248.p.523', type='drop', source_team_key='248.l.1328.t.12')
        self.transaction = Transaction('add/drop', players=[self.p1, self.p2])
        expected = b'<fantasy_content><transaction><type>add/drop</type><players><player><player_key>248.p.522</player_key><transaction_data><type>add</type><destination_team_key>248.l.1328.t.12</destination_team_key></transaction_data></player><player><player_key>248.p.523</player_key><transaction_data><type>drop</type><source_team_key>248.l.1328.t.12</source_team_key></transaction_data></player></players></transaction></fantasy_content>'
        logging.debug(pretty_xml(self.transaction.to_xml()))
        self.assertEqual(expected, self.transaction.to_xml())
        
    def test_propose_trade(self,):
        self.p1 = Player('248.p.4130', type='pending_trade', source_team_key='248.l.55438.t.11', destination_team_key='248.l.55438.t.4')
        self.p2 = Player('248.p.2415', type='pending_trade', source_team_key='248.l.55438.t.4', destination_team_key='248.l.55438.t.11')
        self.transaction = Transaction('pending_trade', players=[self.p1, self.p2], trader_team_key ='248.l.55438.t.11', tradee_team_key='248.l.55438.t.4', trade_note='Yo yo yo yo yo!!!', propose_trade=True)
        expected = b'<fantasy_content><transaction><type>pending_trade</type><trader_team_key>248.l.55438.t.11</trader_team_key><tradee_team_key>248.l.55438.t.4</tradee_team_key><trade_note>Yo yo yo yo yo!!!</trade_note><players><player><player_key>248.p.4130</player_key><transaction_data><type>pending_trade</type><source_team_key>248.l.55438.t.11</source_team_key><destination_team_key>248.l.55438.t.4</destination_team_key></transaction_data></player><player><player_key>248.p.2415</player_key><transaction_data><type>pending_trade</type><source_team_key>248.l.55438.t.4</source_team_key><destination_team_key>248.l.55438.t.11</destination_team_key></transaction_data></player></players></transaction></fantasy_content>'
        logging.debug(pretty_xml(self.transaction.to_xml()))
        self.assertEqual(expected, self.transaction.to_xml())       
        

