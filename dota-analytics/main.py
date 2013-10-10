import os
import sqlite3
import sys
import urllib
import json

# Variables

APIkey = #Enter your API key here
numberOfMatches = 25
startDate = "1378036800"
gameMode = "1"
currentMatch = "0"
matchHistoryURL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key="
matchDetailsURL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?key="

# Database setup

def initDB():
	try:
	    con = sqlite3.connect('dota-analytics.db')
	    cur = con.cursor()
	    cur.execute("CREATE TABLE matchDetails(matchID INT, winner TEXT, firstBlood INT, duration INT, radiant1 INT, radiant2 INT, radiant3 INT, radiant4 INT, radiant5 INT, dire1 INT, dire2 INT, dire3 INT, dire4 INT, dire5 INT)")

	finally:
	    if con:
	        con.close()


def getMatchList(matchBracket):
	print "Testing"
	matchList = []

	matchDateRequest = matchHistoryURL + APIkey + "&matches_requested=1"
	print matchDateRequest
	matchDateFile = urllib.urlopen(matchDateRequest)
	matchDateText = matchDateFile.read()
	jsonDateText = json.loads(matchDateText)
	currentMatch = str(jsonDateText['result']['matches'][0]['match_id'])
        print currentMatch

	i = 0
	while i < numberOfMatches:
		matchListRequest = matchHistoryURL + APIkey + "&start_at_match_id=" + currentMatch + "&game_mode=" + gameMode + "&skill=" + matchBracket + "&lobby_type=0&matches_requested=25"
		print matchListRequest
		matchListFile = urllib.urlopen(matchListRequest)
		matchListText = matchListFile.read()
		jsonListText = json.loads(matchListText)
		j = 0
                while j < 25:
			jsonMatch = jsonListText['result']['matches'][j]['match_id']
			matchList.append(jsonMatch)
                        j+=1
		i += 25

	return matchList


def getMatchData(matchList):
	heroDetails = []
	matchDetails = []

	for item in matchList:
		currentMatch = str(item)
		matchDetailsRequest = matchDetailsURL + APIkey + "&match_id=" + currentMatch
		print matchDetailsRequest
		matchDetailsFile = urllib.urlopen(matchDetailsRequest)
		matchDetailsText = matchDetailsFile.read()

		print matchDetailsText

		jsonDetailsText = json.loads(matchDetailsText)
		matchDetails.append(jsonDetailsText['result']['match_id'])
		matchDetails.append(jsonDetailsText['result']['radiant_win'])
		matchDetails.append(jsonDetailsText['result']['duration'])
		matchDetails.append(jsonDetailsText['result']['first_blood_time'])

		print matchDetails	

#initDB()
matchList = getMatchList("0")
print matchList

getMatchData(matchList)
