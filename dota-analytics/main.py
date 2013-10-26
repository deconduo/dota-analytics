'''Imports'''

import urllib
import json
import csv
from time import sleep

'''Variables'''

APIkey = "" # Enter your Steam API key here
numberOfMatches = 100 # Enter number of matches to download
dateStart = 1381363200 # Enter the date to start at, in UNIX time
gameMode = 1 # Enter the number corresponding to the appropriate gamemode
matchBracket = 1 # Enter the number corresponding the match bracket

# Steam API URLs
matchHistoryURL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key="
matchDetailsURL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?key="

'''Classes'''

# Retrieves a list of matches to process, given the starting variables.

def getMatchList():
        matchList = []
        i = 0
        dateMax = dateStart
        while i < numberOfMatches:
                matchListRequest = matchHistoryURL + APIkey + "&date_max=" + str(dateMax) + "&game_mode=" + str(gameMode) + "&skill=" + str(matchBracket) + "&lobby_type=0&matches_requested=25"
                print matchListRequest
                matchListFile = urllib.urlopen(matchListRequest)
                matchListText = matchListFile.read()
                print matchListText
                jsonListText = json.loads(matchListText)
                j = 0
                dateMax = jsonListText['result']['matches'][24]['start_time']
                while j < 25:
                        jsonMatch = jsonListText['result']['matches'][j]['match_id']
                        matchList.append(jsonMatch)
                        j+=1
                i += 25
        print matchList
        getMatchData(matchList)

# Gets match and hero information

def getMatchData(matchList):
	k = 0
	matchInfo = []
	heroInfo = []
        for item in matchList:
            currentMatch = str(item)
            matchDetailsRequest = matchDetailsURL + APIkey + "&match_id=" + currentMatch
            matchDetailsFile = urllib.urlopen(matchDetailsRequest)
            matchDetailsText = matchDetailsFile.read()
            try: 
	        jsonDetailsText = json.loads(matchDetailsText)
                matchDetails = []
		matchDetails.append(jsonDetailsText['result']['match_id'])
                matchDetails.append(jsonDetailsText['result']['radiant_win'])
                matchDetails.append(jsonDetailsText['result']['duration'])
                matchDetails.append(jsonDetailsText['result']['first_blood_time'])
		matchDetails.append(jsonDetailsText['result']['tower_status_radiant'])
		matchDetails.append(jsonDetailsText['result']['tower_status_dire'])
		matchDetails.append(jsonDetailsText['result']['barracks_status_radiant'])
		matchDetails.append(jsonDetailsText['result']['barracks_status_dire'])
		matchDetails.append(jsonDetailsText['result']['lobby_type'])
		matchDetails.append(jsonDetailsText['result']['game_mode'])
		matchDetails.append(jsonDetailsText['result']['human_players'])
		matchDetails.append(matchBracket)
                matchInfo.append(matchDetails)
                j = 0
                while j < 10:
                    heroDetails = []
                    heroDetails.append(jsonDetailsText['result']['match_id'])
		    heroDetails.append(jsonDetailsText['result']['players'][j]['player_slot'])
		    heroDetails.append(jsonDetailsText['result']['players'][j]['hero_id'])
                    heroDetails.append(jsonDetailsText['result']['players'][j]['kills'])
                    heroDetails.append(jsonDetailsText['result']['players'][j]['deaths'])
                    heroDetails.append(jsonDetailsText['result']['players'][j]['assists'])
                    heroDetails.append(jsonDetailsText['result']['players'][j]['gold_per_min'])
                    heroDetails.append(jsonDetailsText['result']['players'][j]['xp_per_min'])
                    heroDetails.append(jsonDetailsText['result']['players'][j]['last_hits'])
                    heroDetails.append(jsonDetailsText['result']['players'][j]['denies'])
		    heroDetails.append(jsonDetailsText['result']['players'][j]['gold_spent'])
		    heroDetails.append(jsonDetailsText['result']['players'][j]['hero_damage'])
		    heroDetails.append(jsonDetailsText['result']['players'][j]['tower_damage'])
		    heroDetails.append(jsonDetailsText['result']['players'][j]['hero_healing'])
		    heroDetails.append(matchBracket)
                    heroInfo.append(heroDetails)
                    j += 1
	        k += 1
		if (k % 25 == 0):
		    print k
            except ValueError:
                print "Type error" 
                sleep(5)
	    if k > 1000:
                writeCSV(matchInfo, "match")
                writeCSV(heroInfo, "hero")
		matchInfo = []
		heroInfo = []
	        k = 0
	writeCSV(matchInfo, "match")
	writeCSV(heroInfo, "hero")


def writeCSV(details, filename):    
    Output = open(filename+'.csv', "a")
    Writer = csv.writer(Output, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)
    for row in details:
	Writer.writerow(row)
    Output.close()

# Main program

def main():
    getMatchList()

if __name__ == "__main__":
    main()
