'''Imports'''

import urllib
import json
import csv
import sys
from time import sleep
from operator import itemgetter

'''Variables'''

APIkey = ""
numberOfMatches = 200000 # Enter number of matches to download
dateStart = 1384098000  # Enter the date to start at, in UNIX time
gameMode = 1 # Enter the number corresponding to the appropriate gamemode

# Steam API URLs
matchHistoryURL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key="
matchDetailsURL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?key="

'''Classes'''

# Retrieves a list of matches to process, given the starting variables.

def getMatchList():
        matchList = []
        i = 0
        dateMax = dateStart
        dateMin = dateStart - 500
        matchStartID = 0
        matchBracket = 1
        while i < numberOfMatches:
            try:
                if matchStartID == 0:
                    matchListRequest = matchHistoryURL + APIkey + "&date_max=" + str(dateMax) + "&date_min=" + str(dateMin) + "&game_mode="$
                else:
                    matchListRequest = matchHistoryURL + APIkey + "&date_max=" + str(dateMax) + "&date_min=" + str(dateMin) + "&start_at_ma$
                matchListFile = urllib.urlopen(matchListRequest)
                matchListText = matchListFile.read()
                jsonListText = json.loads(matchListText)
                j = 0
                l = jsonListText['result']['num_results']
                matchStartID = jsonListText['result']['matches'][l-1]['match_id']
                while j < l:
                    matchTuple = (jsonListText['result']['matches'][j]['match_id'], matchBracket)
                    matchList.append(matchTuple)
                    j+=1
                if l <= 1:
                    if matchBracket == 3:
                        print i
                        dateMin = dateMin - 500
                        dateMax =  dateMax - 500
                        matchBracket = 1
                    else:
                        matchBracket += 1
                    matchStartID = 0
                i += l
            except:
                e = sys.exc_info()[0]
                print "Error: %s" % e
                print matchListRequest
                sleep(15)
        matchList = set(matchList)
        listFile = open("list.txt", 'w')
        for item in matchList:
            print>>listFile, item
        listFile.close()

# Gets match and hero information
def getMatchData(matchList):
        k = 0
        matchInfo = []
        heroInfo = []
        for item in matchList:
            currentMatch = str(item[0])
            matchBracket = item[1]
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
                    writeCSV(matchInfo, "match")
                    writeCSV(heroInfo, "hero")
                           matchInfo = []
                    heroInfo = []
            except:
                print "Error"
                print matchDetailsRequest
                sleep(15)
        writeCSV(matchInfo, "match")
        writeCSV(heroInfo, "hero")


def cleanCSV(filename):
    f = open(filename, 'rb')
    reader = csv.reader(f, delimiter='\t', quotechar="'")
    current = []
    for row in reader:
        current.append(row)
    f.close()

    for x in current:
        i = 0
        while i < 15:
            x[i] = int(x[i])
            i += 1
        if x[1] > 120:
            x[1] = "Dire"
        else:
            x[1] = "Radiant"

    current = sorted(current, key=itemgetter(0,1,6))
    cleaned = []
    y = []
    j = 0
    k = 0
    for x in current:
        while j < 14:
            y.append(x[j])
            j+= 1
        k += 1
        if k == 10:
            j = 0
            k = 0
            y.append(x[14])
            cleaned.append(y)
            y = []
        else:
            j = 2
    writeCSV(cleaned, filename)


def writeCSV(details, filename):
    Output = open(filename+'.csv', "a")
    Writer = csv.writer(Output, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)
    for row in details:
        Writer.writerow(row)
    Output.close()

# Main program

def main():
    matchList = []
    with open('matchList', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
           matchList.append(row)

    getMatchData(matchList)

if __name__ == "__main__":
    main()

