import sys
import json
from urllib import urlopen
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy import Integer, String


# Loads data from an array of json files into the database
def load_data(matchDetailsList):
    engine = create_engine('sqlite:///flask-dota.db', convert_unicode=False)
    metadata = MetaData(bind=engine)

    # Creates the MatchData table
    match_table = Table('MatchData', metadata,
                        Column('match_id', Integer, primary_key=True),
                        Column('radiant_win', String(5)),
                        Column('duration', Integer),
                        Column('start_time', Integer),
                        Column('first_blood_time', Integer),
                        Column('tower_status_radiant', Integer),
                        Column('tower_status_dire', Integer),
                        Column('barracks_status_radiant', Integer),
                        Column('barracks_status_dire', Integer),
                        Column('lobby_type', Integer),
                        Column('human_players', Integer),
                        Column('leagueid', Integer),
                        Column('game_mode', Integer),
                        Column('match_bracket', Integer),
                        )

    # Creates the HeroData table
    hero_table = Table('HeroData', metadata,
                       Column('player_slot', Integer, primary_key=True),
                       Column('match_id', None, ForeignKey('MatchData.match_id'), primary_key=True),
                       Column('account_id', Integer),
                       Column('hero_id', Integer),
                       Column('kills', Integer),
                       Column('deaths', Integer),
                       Column('assists', Integer),
                       Column('last_hits', Integer),
                       Column('denies', Integer),
                       Column('gold_per_min', Integer),
                       Column('xp_per_min', Integer),
                       Column('gold_spent', Integer),
                       Column('gold', Integer),
                       Column('hero_damage', Integer),
                       Column('tower_damage', Integer),
                       Column('hero_healing', Integer),
                       Column('level', Integer),
                       Column('leaver_status', Integer),
                       Column('item_0', Integer),
                       Column('item_1', Integer),
                       Column('item_2', Integer),
                       Column('item_3', Integer),
                       Column('item_4', Integer),
                       Column('item_5', Integer),
                       )

    # Creates the AbilityData table
    ability_table = Table('AbilityData', metadata,
                       Column('level', Integer, primary_key=True),
                       Column('match_id', None, ForeignKey('MatchData.match_id'), primary_key=True),
                       Column('player_slot', None, ForeignKey('HeroData.player_slot'), primary_key=True),
                       Column('ability', Integer),
                       Column('time', Integer),
                       )

    metadata.create_all()
    conn = engine.connect()

    # Loops through the supplied json files and adds them to the database
    try:
        for item in matchDetailsList:
            detailsFile = json.loads(item[0])
            matchBracket = item[1]

            # Sets the match bracket
            detailsFile['result']['match_bracket'] = matchBracket

            # Loads the match data
            conn.execute(match_table.insert(), detailsFile['result'])
            for hero in detailsFile['result']['players']:
                hero['match_id'] = detailsFile['result']['match_id']

                # Loads the hero data
                conn.execute(hero_table.insert(), hero)
                for ability in hero['ability_upgrades']:
                    ability['match_id'] = detailsFile['result']['match_id']
                    ability['player_slot'] = hero['player_slot']

                    # Loads the ability data
                    conn.execute(ability_table.insert(), ability)
    except:
        pass

# Fetches a list of matches, including the match bracket
def get_match_list(APIKey, dateMax, numberOfMatches):
    matchList = []
    matchListSet = []
    matchStartID = 0
    matchBracket = 1
    matchListRequest = ""
    matchHistoryURL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key="
    gameMode = 0
    # Runs for the number of matches selected
    i = 0
    while i < numberOfMatches:

        try:
            print i
            if matchStartID == 0:
                matchListRequest = (matchHistoryURL + APIKey +
                                    "&date_max=" + str(dateMax) +
                                    "&date_min=" + str(dateMax - 500) +
                                    "&game_mode=" + str(gameMode) +
                                    "&skill=" + str(matchBracket) +
                                    "&lobby_type=0&matches_requested=100"
                )

            else:
                matchListRequest = (matchHistoryURL + APIKey +
                                    "&date_max=" + str(dateMax) +
                                    "&date_min=" + str(dateMax - 500) +
                                    "&start_at_match_id=" + str(matchStartID) +
                                    "&skill=" + str(matchBracket) +
                                    "&lobby_type=0&matches_requested=100"
                )
            matchListFile = urlopen(matchListRequest)
            matchListText = matchListFile.read()
            jsonListText = json.loads(matchListText)
            totalRes = jsonListText['result']['num_results']
            matchStartID = jsonListText['result']['matches'][totalRes - 1]['match_id']
            for j in range(totalRes):
                matchList.append((jsonListText['result']['matches'][j]['match_id'], matchBracket))
            if totalRes <= 1:
                if matchBracket == 3:
                    print i
                    dateMax =  dateMax - 500
                    matchBracket = 1
                else:
                    matchBracket += 1
                matchStartID = 0
            matchListSet = set(matchList)
            i = len(matchListSet)

        except:
            e = sys.exc_info()[0]
            print "Error: %s" % e
            print matchListRequest
            sleep(15)

    return list(matchListSet)

# Gets the last matches played by a certain player
def get_player_matches(steamID, APIKey):
    matchHistoryURL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key="
    matchList = []
    matchListRequest = matchHistoryURL + APIKey + "&account_id=" + str(steamID)
    matchListFile = urlopen(matchListRequest)
    matchListText = matchListFile.read()
    jsonListText = json.loads(matchListText)

    #for i in range(jsonListText['result']['num_results'] - 1):
    for i in range(5):

        matchList.append((jsonListText['result']['matches'][i]['match_id'], 0))

    return matchList

# Gets the match_id of the last game played by a player
def get_last_match(steamID, APIKey):
    matchHistoryURL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key="
    matchList = []
    matchListRequest = matchHistoryURL + APIKey + "&account_id=" + str(steamID)
    matchListFile = urlopen(matchListRequest)
    matchListText = matchListFile.read()
    jsonListText = json.loads(matchListText)

    return jsonListText['result']['matches'][0]['match_id']

    
# Gets the jsons file for a list of matches
def get_match_data(matchList, APIKey):
    matchDetailsList = []
    matchDetailsURL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?key="

    for item in matchList:
        currentMatch = str(item[0])
        matchBracket = item[1]
        matchDetailsRequest = matchDetailsURL + APIKey + "&match_id=" + currentMatch
        matchDetailsFile = urlopen(matchDetailsRequest)
        matchDetailsText = matchDetailsFile.read()
        matchDetailsList.append((matchDetailsText, matchBracket))

    return matchDetailsList
