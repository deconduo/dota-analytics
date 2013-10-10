import urllib
import json
import csv

# Variables

APIkey = '' #Enter your API key here
numberOfMatches = 25
startDate = "1378036800"
gameMode = "1"
currentMatch = "0"
matchHistoryURL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key="
matchDetailsURL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?key="

# Database setup

def getMatchList(matchBracket):
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
		matchTuple = []
		currentMatch = str(item)
		matchDetailsRequest = matchDetailsURL + APIkey + "&match_id=" + currentMatch
		matchDetailsFile = urllib.urlopen(matchDetailsRequest)
		matchDetailsText = matchDetailsFile.read()

		jsonDetailsText = json.loads(matchDetailsText)
		matchTuple.append(jsonDetailsText['result']['match_id'])
		matchTuple.append(jsonDetailsText['result']['radiant_win'])
		matchTuple.append(jsonDetailsText['result']['duration'])
		matchTuple.append(jsonDetailsText['result']['first_blood_time'])

		j = 0
		while j < 10:
			heroTuple = []
			heroTuple.append(jsonDetailsText['result']['match_id'])
			heroTuple.append(jsonDetailsText['result']['players'][j]['hero_id'])
			heroTuple.append(jsonDetailsText['result']['players'][j]['kills'])
			heroTuple.append(jsonDetailsText['result']['players'][j]['deaths'])
			heroTuple.append(jsonDetailsText['result']['players'][j]['assists'])
			heroTuple.append(jsonDetailsText['result']['players'][j]['gold_per_min'])
			heroTuple.append(jsonDetailsText['result']['players'][j]['xp_per_min'])
			heroTuple.append(jsonDetailsText['result']['players'][j]['last_hits'])
			heroTuple.append(jsonDetailsText['result']['players'][j]['denies'])
			heroDetails.append(heroTuple)
			j += 1
		
		matchDetails.append(matchTuple)

        return matchDetails, heroDetails


def outputData(matchDetails, heroDetails):
    matchOutput = open('matchData.csv', "wb")
    matchWriter = csv.writer(matchOutput, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)

    heroOutput = open('heroData.csv', "wb")
    heroWriter = csv.writer(heroOutput, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)


    for row in matchDetails:
        matchWriter.writerow(row)

    for row in heroDetails:
	heroWriter.writerow(row)

    matchOutput.close()
    heroOutput.close()

#initDB()
matchList = getMatchList("0")
print matchList

matchDetails, heroDetails = getMatchData(matchList)
print matchDetails
print heroDetails

outputData(matchDetails, heroDetails)
