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
matchBracket = 0 # Enter the number corresponding the match bracket

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

	return matchList

# Gets match information and writes it to a csv file.

def getMatchData(matchList):
	for item in matchList:
		matchDetails = []
		currentMatch = str(item)
		matchDetailsRequest = matchDetailsURL + APIkey + "&match_id=" + currentMatch
		matchDetailsFile = urllib.urlopen(matchDetailsRequest)
		matchDetailsText = matchDetailsFile.read()

		jsonDetailsText = json.loads(matchDetailsText)
		matchDetails.append(jsonDetailsText['result']['match_id'])
		matchDetails.append(jsonDetailsText['result']['radiant_win'])
		matchDetails.append(jsonDetailsText['result']['duration'])
		matchDetails.append(jsonDetailsText['result']['first_blood_time'])

		j = 0
		while j < 10:
			sleep(1)
			heroDetails = []
			heroDetails.append(jsonDetailsText['result']['match_id'])
			heroDetails.append(jsonDetailsText['result']['players'][j]['hero_id'])
			heroDetails.append(jsonDetailsText['result']['players'][j]['kills'])
			heroDetails.append(jsonDetailsText['result']['players'][j]['deaths'])
			heroDetails.append(jsonDetailsText['result']['players'][j]['assists'])
			heroDetails.append(jsonDetailsText['result']['players'][j]['gold_per_min'])
			heroDetails.append(jsonDetailsText['result']['players'][j]['xp_per_min'])
			heroDetails.append(jsonDetailsText['result']['players'][j]['last_hits'])
			heroDetails.append(jsonDetailsText['result']['players'][j]['denies'])
			j += 1

			heroOutput = open('heroData.csv', "wb")
    			heroWriter = csv.writer(heroOutput, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)
    			heroWriter.writerow(heroDetails)
    			heroOutput.close()

		matchOutput = open('matchData.csv', "wb")
	    	matchWriter = csv.writer(matchOutput, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)
		matchWriter.writerow(matchDetails)
    		matchOutput.close()

# Main program

def main():
	matchList = getMatchList()
	print matchList

	getMatchData(matchList)


if __name__ == "__main__":
    main()
