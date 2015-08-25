from fantasy_sport import FantasySport
from yahoo_oauth import OAuth1
from fantasy_sport.utils import pretty_json, pretty_xml
import json
import datetime

# Inputs
gameID = 346
leagueID = 1328
teamID = 12
playerID = 8781
input_date = '2015-08-20'
###

new_optimal_lineup = {}
ineligible = set()

#Make ranking of positions used for sorting
position_dict = {'C': 0, '1B': 1, '2B': 2, '3B': 3, 'SS': 4,
                    'MI': 5, 'CI': 6, 'OF': 7, 'Util': 8}

today = False
current_date = str(datetime.date.today())

if current_date == input_date:
    today = True
    
    
def make_league_code(gameid, leagueid):
    return [str(gameid) + '.l.' + str(leagueid)]

def make_team_code(gameid, leagueid, teamid):
    return [str(gameid) + '.l.' + str(leagueid) + '.t.' + str(teamid)]
    
def make_player_code(gameid, playerid):
    return [str(gameid) + '.p.' + str(playerid)]
    
    
def get_roster_data():
    """Pull league info and parse into useable roster
    """
    team_code = make_team_code(gameID, leagueID, teamID) #make team code
    response = yfs.get_roster_players(team_code, date=input_date) #call API function
    data = response.json() #get response
    return parse_set_roster(data) #organize response 
    
def parse_set_roster(data):
    """cleans API set_roster response
    """
    roster_info = (data['fantasy_content']['team'][1]['roster']['0']['players'])
    
    batters = []
    pitchers = []
    
    for p in roster_info:
        player_info = roster_info[p]
        
        #ignore players on DL for setting lineup
        try:
            if 'on_disabled_list' in player_info['player'][0][4]: continue
        except TypeError:
            continue
        
        try: #don't get caught on irregular output
            name_info = player_info['player'][0][2]
        except TypeError:
            continue
            
        name = name_info['name']['ascii_first'] + ' ' + name_info['name']['ascii_last']
        
        try:
            position_info = player_info['player'][0][12]
        except TypeError:
            continue
            
        eligible_positions = position_info['eligible_positions']
        
        positions = set()
        #create set of eligible positions for each player
        [positions.add(x['position']) for x in eligible_positions]

        #include current position of player
        current_position = player_info['player'][1]['selected_position'][1]['position']
        
        #include if starting and editable.
        #Default is true, only make false if known false
        starting = True
        editable = True
        
        if today:
            try:
                if 'starting_status' in player_info['player'][2]:
                    if 0 == player_info['player'][2]['starting_status'][1]['is_starting']:
                        starting = False
                if 0 == player_info['player'][3]['is_editable']:
                    editable = False
                    
            except TypeError:
                continue
        
        #Create tuple of all relevant
        player = (name, ((current_position, positions), (starting, editable)))
        
        #append to list based on batter or pitcher
        try:
            if 'B' in player_info['player'][0][11]['position_type']:
                batters.append(player)
            else:
                pitchers.append(player)
        except TypeError:
            continue
       
    return (batters, pitchers)
    
   
def get_player_projections(batter_names, pitcher_names):
    #Connect to Rudy's db and get projections
    #For now, use dummy values
    
    batters_proj = []
    pitchers_proj = []
    
    batters_projection_list = [30,20,10,25,15,5,6,7,13,19,40,34,14,26,33]
    pitchers_projection_list = [0,2,0,0,10,0,0,4,0,3]
    
    for (i, _) in enumerate(batter_names):
        batters_proj.append(batters_projection_list[i])
        
    for (i, _) in enumerate(pitcher_names):
        pitchers_proj.append(pitchers_projection_list[i])
    
    return (batters_proj, pitchers_proj)
    
def optimal_batting(batters):
    #Finds optimal hitting lineup
    
    #batters = ((name, ((current_pos, eligible_positions), (starting, editable))), projection)
    position_list = ['C','1B','2B','3B','SS','MI','CI','OF','OF','OF','OF','Util','Util']
    """
    #Handle any player that cannot be edited
    for ((name, ((current_position, eligible_positions), (starting, editable))), projection) in batters:
        if not editable:
            new_optimal_lineup.insert(position_dict[current_position],(name, (current_position, projection)))
            if current_position == 'OF' or 'Util':
                position_dict[current_position] += 1
            position_list.remove(current_position)
            ineligible.add(name)
    """
    for ((name, ((current_position, eligible_positions), (starting, editable))), projection) in batters:
        if not editable:
            new_optimal_lineup[name] = current_position
            position_list.remove(current_position)
            ineligible.add(name)
    
    #For all positions remaining that do not have an uneditable player in them
    for pos in position_list:
        eligible_players = [(name, projection) for ((name, ((current_position, eligible_positions), (starting, editable))), projection) in batters
                            if pos in eligible_positions if starting if name not in ineligible]
        _ = optimal_batting_position(eligible_players, pos)
        
    return new_optimal_lineup

    
def optimal_batting_position(eligible_players, position):
    #Given list of eligible players and the position,
    #Determines best players for that position
    #Adds players to list of closed players
    
    if len(eligible_players) == 1:
        new_optimal_lineup[eligible_players[0][0]] = position
        ineligible.add(eligible_players[0][0])
    else:
        eligible_players.sort(key = lambda x: x[1], reverse=True)
        new_optimal_lineup[eligible_players[0][0]] = position
        ineligible.add(eligible_players[0][0])

    return None
    
#def optimal_pitching(pitchers):
def optimal_pitching():
    return None
    
def make_hitting_lineup(batting):
    #Make current hitting lineup
    
    #unsorted lineup
    #In defunct list format
    #lineup = [(name, current_position) for (name, ((current_position, e_p), (s, e))) 
            #in batting if current_position != 'BN']
            
    #In better dict format
    old_lineup = {name: current_position for (name, ((current_position, _), _)) in batting}
    
    #sort by values in position_dict
    #lineup.sort(key=lambda x: position_dict[x[1]])
    
    return old_lineup
    
def find_differences(o_h_l, n_h_l):
    #compare old and new hitting lineup
    
    diffy = set(o_h_l.keys()) - set(n_h_l.keys())
    
    for bn_plyr in diffy:
        n_h_l[bn_plyr] = 'BN'
    
    diff = {x:n_h_l[x] for x in n_h_l if n_h_l[x] != o_h_l[x]}
    
    for x in diff:
        p1 = x
        pos1 = diff[x]
        for k, v in o_h_l.items():
            if v == diff[x]:
                p2 = k
                pos2 = n_h_l[p2]
                print 'Move %s to %s, and move %s to %s' % (p1, pos1, p2, pos2)
                
    
    return None
                
        
def optimal_lineup():
    #Take in current roster, projections
    #find optimal hitting and pitching lineup
    
    #Get current team data
    batting, pitching = get_roster_data()
    
    #Construct current lineups (sorted)
    original_hitting_lineup = make_hitting_lineup(batting)
    
    #names not used yet, I'm assuming will be for SQL lookup
    batter_names = [name for (name, _) in batting]
    pitcher_names = [name for (name, _) in pitching]
    
    bat_projection, pitch_projection = get_player_projections(batter_names, pitcher_names)
    
    batters = zip(batting, bat_projection)
    #pitchers = zip(pitching, pitch_projection)
    
    new_hitting_lineup = optimal_batting(batters)
    #y = optimal_pitching(pitchers)
    
    print 'old'
    print original_hitting_lineup
    
    print '\nnew'
    print new_hitting_lineup
    
    zzzxzx = find_differences(original_hitting_lineup, new_hitting_lineup)
    
    return None
     

### 

if __name__ == "__main__":            
    oauth = OAuth1(None, None, from_file='oauth.json',base_url='http://fantasysports.yahooapis.com/fantasy/v2/')
    yfs = FantasySport(oauth)

    zzz = optimal_lineup()
    
    
    
    