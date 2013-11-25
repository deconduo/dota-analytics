from __future__ import absolute_import
from celery import Celery
import urllib
import json

celery = Celery("tasks",
                broker='redis://localhost:6379/0',
                backend='redis')

def getGameData(steamID):
    gameData = []
    APIkey = ""
    matchHistoryURL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key="
    matchDetailsURL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?key="

    matchList = []
    matchListRequest = matchHistoryURL + APIkey + "&account_id=" + str(steamID)
    matchListFile = urllib.urlopen(matchListRequest)
    matchListText = matchListFile.read()
    jsonListText = json.loads(matchListText)

    i = 0
    while i < 3:
        matchList.append(jsonListText['result']['matches'][i]['match_id'])
        i += 1

    for matchID in matchList:
        matchDetailsRequest = matchDetailsURL + APIkey + "&match_id=" + str(matchID)
        matchDetailsFile = urllib.urlopen(matchDetailsRequest)
        matchDetailsText = matchDetailsFile.read()
        jsonDetailsText = json.loads(matchDetailsText)
        matchDetails = []
        for j in range(0, 9):
            if str(jsonDetailsText['result']['players'][j]['account_id']) == str(steamID):
                matchDetails.append(jsonDetailsText['result']['match_id'])
                matchDetails.append(jsonDetailsText['result']['players'][j]['gold_per_min'])
                matchDetails.append(jsonDetailsText['result']['players'][j]['xp_per_min'])
                matchDetails.append(jsonDetailsText['result']['players'][j]['last_hits'])
                matchDetails.append(jsonDetailsText['result']['players'][j]['denies'])
                matchDetails.append(jsonDetailsText['result']['players'][j]['kills'])
                matchDetails.append(jsonDetailsText['result']['players'][j]['deaths'])
                matchDetails.append(jsonDetailsText['result']['players'][j]['assists'])
                matchDetails.append(jsonDetailsText['result']['duration'])
                gameData.append(matchDetails)
    return gameData

def getCleanData(gameData):
    cleanData = []
    namesRow = []
    xpRow = []
    goldRow = []
    lasthitsRow = []
    deniesRow = []
    killsRow = []
    deathsRow = []
    assistsRow = []
    skillRow = []

    for row in gameData:
        namesRow.append(row[0])
        goldRow.append(row[1])
        xpRow.append(row[2])
        lasthitsRow.append(row[3])
        deniesRow.append(row[4])
        killsRow.append(row[5])
        deathsRow.append(row[6])
        assistsRow.append(row[7])
        skillRow.append(getSkill(row))

    cleanData.append(namesRow)
    cleanData.append(goldRow)
    cleanData.append(xpRow)
    cleanData.append(lasthitsRow)
    cleanData.append(deniesRow)
    cleanData.append(killsRow)
    cleanData.append(deathsRow)
    cleanData.append(assistsRow)
    cleanData.append(skillRow)

    return cleanData

def getSkill(gameRow):
    skill = 1
    return skill


@celery.task(name="tasks.celeryData")
def celeryData(steamID, x):
    y = x
    gameData = getGameData(steamID)
    cleanData = getCleanData(gameData)
    return cleanData

if __name__ == "__main__":
    celery.start()
