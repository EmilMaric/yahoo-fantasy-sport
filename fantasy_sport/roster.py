from __future__ import absolute_import, unicode_literals

import six
import abc
import json

from xml.etree import cElementTree as ctree

@six.add_metaclass(abc.ABCMeta)
class Base(object):
    """Base class for Roster and Player
    """

    @abc.abstractmethod
    def xml_builder_player(self,):
        raise NotImplementedError
        
    @abc.abstractmethod
    def xml_builder_player_proposetrade(self,):
        raise NotImplementedError
    
    @abc.abstractmethod
    def xml_builder_put(self,):
        raise NotImplementedError
        
    @abc.abstractmethod
    def xml_builder_addordrop(self,):
        raise NotImplementedError
        
    @abc.abstractmethod
    def xml_builder_adddrop(self,):
        raise NotImplementedError
        
    @abc.abstractmethod
    def xml_builder_proposetrade(self,):
        raise NotImplementedError
        
    @abc.abstractmethod
    def xml_builder_roster(self,):
        raise NotImplementedError
        
    #@abc.abstractmethod
    #def xml_builderpost(self,):
        #raise NotImplementedError

    #@abc.abstractmethod
    #def json_builder(self,):
        #raise NotImplementedError
   
    #def to_json(self,):
        #"""Return object as a json string
        #"""
        #return json.dumps(self.json, ensure_ascii=True).encode('ascii')
    
    def to_xml(self,):
        """Return object as a xml string
        """
        return ctree.tostring(self.xml)


class Roster(Base):
    """Roster class
    """

    def __init__(self, players, week=None, date=None):
        """Initialize a roster class
        """
        super(Base, self).__init__()

        self.players = players

        if week:
            self.coverage = week
            self.coverage_type = 'week'
        else:
            self.coverage = date
            self.coverage_type = 'date'

        #self.json_builder()
        self.xml_builder_roster()

    def xml_builder_roster(self,):
        """Convert object to xml
        """
        content = ctree.Element('fantasy_content')
        roster = ctree.SubElement(content, 'roster')

        coverage_type = ctree.SubElement(roster, 'coverage_type')
        coverage_type.text = self.coverage_type

        coverage = ctree.SubElement(roster, self.coverage_type)
        coverage.text = self.coverage

        players = ctree.SubElement(roster, 'players')
        for player in self.players :
            players.append(player.xml)

        self.xml = content
        

    #def json_builder(self,):
        #"""Convert object to json
        #"""
        #self.json = {
            #'fantasy_content':{
                #'roster':{
                    #'coverage_type': self.coverage_type,
                    #self.coverage_type : self.coverage,
                    #'players': [ player.json for player in self.players ]
                #}
            #}
        #}
        #return self.json
        
    def xml_builder_addordrop(self,):
        return None
        
    def xml_builder_adddrop(self,):
        return None
        
    def xml_builder_proposetrade(self,):
        return None
        
    def xml_builder_put(self,):
        return None
        
    def xml_builder_roster(self,):
        return None
    
    def xml_builder_player(self,):
        return None
        
    def xml_builder_player_proposetrade(self,):
        return None
    

class Player(Base):
    """player class
    - player_key
    - position
    """

    def __init__(self, player_key, type=None, position=None,
                 destination_team_key=None, source_team_key=None
        ):
        """Initialize a player object
        """
        super(Base, self).__init__()

        self.player_key = player_key
        self.position = position
        self.type = type
        self.destination_team_key = destination_team_key
        self.source_team_key = source_team_key
        
        if self.type == 'pending_trade':
            self.xml_builder_player_proposetrade()
        else:
            self.xml_builder_player()

    def xml_builder_player(self,):
        """Convert object into a xml object
        """
        player = ctree.Element('player')
        
        player_key = ctree.SubElement(player, 'player_key')
        player_key.text = self.player_key
        
        if self.position:
            position = ctree.SubElement(player, 'position')
            position.text = self.position
        
        if self.type:
            transaction_data = ctree.SubElement(player, 'transaction_data')
            type = ctree.SubElement(transaction_data, 'type')
            type.text = self.type
        
        if self.destination_team_key:
            destination_team_key = ctree.SubElement(transaction_data, 'destination_team_key')
            destination_team_key.text = self.destination_team_key
        
        if self.source_team_key:
            source_team_key = ctree.SubElement(transaction_data, 'source_team_key')
            source_team_key.text = self.source_team_key
        
        self.xml = player
        return self.xml
        
    def xml_builder_player_proposetrade(self,):
        """Convert player object into xml object
        """
        player = ctree.Element('player')
        
        player_key = ctree.SubElement(player, 'player_key')
        player_key.text = self.player_key
        
        transaction_data = ctree.SubElement(player, 'transaction_data')
        
        type = ctree.SubElement(transaction_data, 'type')
        type.text = self.type
        
        source_team_key = ctree.SubElement(transaction_data, 'source_team_key')
        source_team_key.text = self.source_team_key
        
        destination_team_key = ctree.SubElement(transaction_data, 'destination_team_key')
        destination_team_key.text = self.destination_team_key
        
        self.xml = player
        return self.xml

    #def json_builder(self, ):
        #"""Kind of convert object to json
        #"""
        #self.json = {
        #    'player_key': self.player_key,
        #    'position': self.position
        #}

        #return self.json
        
    def xml_builder_addordrop(self,):
        return None
        
    def xml_builder_adddrop(self,):
        return None
        
    def xml_builder_proposetrade(self,):
        return None
        
    def xml_builder_put(self,):
        return None
        
    def xml_builder_player(self,):
        return None
        
    def xml_builder_player_proposetrade(self,):
        return None
        
    def xml_builder_roster(self,):
        return None
        
        
class Transaction(Base):
    """transaction class
    -- edit waiver
    -- allow/disallow trades
    -- allow/disallow against trades (commissioner only)
    -- vote against trades
    -- add, drop, or add/drop a player
    -- propose trades
    """
    def __init__(self, type, transaction_key=None, priority=None, faab_bid=None,
                 action=None, trade_note=None, voter_team_key=None, players=None,
                 trader_team_key=None, tradee_team_key=None, propose_trade=False
        ):
        """Initialize a transaction object for PUT functions"""
        super(Base, self).__init__()
        
        self.type = type
        self.transaction_key = transaction_key
        self.priority = priority
        self.faab_bid = faab_bid
        self.action = action
        self.trade_note = trade_note
        self.voter_team_key = voter_team_key
        self.players=players
        self.trader_team_key = trader_team_key
        self.tradee_team_key = tradee_team_key
        self.propose_trade = propose_trade
        
        types = {'waiver': self.xml_builder_put, 'pending_trade': self.xml_builder_put,
                'add': self.xml_builder_addordrop, 'drop': self.xml_builder_addordrop, 'add/drop': self.xml_builder_adddrop
        }
        
        if self.propose_trade:
            self.xml_builder_proposetrade()
        elif self.type in types:
            types[self.type]()
        else:
            raise Exception("Method %s not implemented" % self.type)
    
    
    def xml_builder_put(self,):
        """Convert into xml object
        """
        content = ctree.Element('fantasy_content')
        transaction = ctree.SubElement(content, 'transaction')
         
        transaction_key = ctree.SubElement(transaction, 'transaction_key')
        transaction_key.text = self.transaction_key
         
        type = ctree.SubElement(transaction, 'type')
        type.text = self.type
         
        if self.priority:
            priority = ctree.SubElement(transaction, 'waiver_priority')
            priority.text = self.priority
         
        if self.faab_bid:
            faab_bid = ctree.SubElement(transaction, 'faab_bid')
            faab_bid.text = self.faab_bid
         
        if self.action:
            action = ctree.SubElement(transaction, 'action')
            action.text = self.action
         
        if self.trade_note:
            trade_note = ctree.SubElement(transaction, 'trade_note')
            trade_note.text = self.trade_note
         
        if self.voter_team_key:
            voter_team_key = ctree.SubElement(transaction, 'voter_team_key')
            voter_team_key.text = self.voter_team_key 
             
        self.xml = content 
        
        
    def xml_builder_addordrop(self,):
        """Convert into xml object
        """
        content = ctree.Element('fantasy_content')
        transaction = ctree.SubElement(content, 'transaction')
         
        type = ctree.SubElement(transaction, 'type')
        type.text = self.type
         
        for player in self.players :
            transaction.append(player.xml)
        
        self.xml = content
        
        
    def xml_builder_adddrop(self,):
        """Convert into xml object
        """
        content = ctree.Element('fantasy_content')
        transaction = ctree.SubElement(content, 'transaction')
         
        type = ctree.SubElement(transaction, 'type')
        type.text = self.type
        
        if self.faab_bid:
            faab_bid = ctree.SubElement(transaction, 'faab_bid')
            faab_bid.text = self.faab_bid
        
        players = ctree.SubElement(transaction, 'players')
        
        for player in self.players:
            players.append(player.xml)
            
        self.xml = content
            
    def xml_builder_proposetrade(self,):
        """Convert into xml object
        """
        content = ctree.Element('fantasy_content')
        transaction = ctree.SubElement(content, 'transaction')
         
        type = ctree.SubElement(transaction, 'type')
        type.text = self.type
        
        trader_team_key = ctree.SubElement(transaction, 'trader_team_key')
        trader_team_key.text = self.trader_team_key
        
        tradee_team_key = ctree.SubElement(transaction, 'tradee_team_key')
        tradee_team_key.text = self.tradee_team_key
        
        if self.trade_note:
            trade_note = ctree.SubElement(transaction, 'trade_note')
            trade_note.text = self.trade_note
        
        players = ctree.SubElement(transaction, 'players')
        
        for player in self.players:
            players.append(player.xml)
            
        self.xml = content
            
    def xml_builder_player(self,):
        return None
        
    def xml_builder_player_proposetrade(self,):
        return None
        
    def xml_builder_roster(self,):
        return None
        