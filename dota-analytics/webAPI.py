import urllib
from variables import APIkey, steamID

'''Variables'''

# APIkey = ""
# steamID = ""



APIkey = "?key=%s" % APIkey
steamID = "&account_id=%s" % steamID
baseURL = "https://api.steampowered.com/IDOTA2Match_570/"
matchHistory = "GetMatchHistory/v001/"
matchDetails = "GetMatchDetails/v001/"
heroes = "GetHeroes/v0001/"
playerSummaries = "GetPlayerSummaries/v0002/"
economySchema = "GetSchema/v0001/"

matchHistoryFile = urllib.urlopen(baseURL + matchHistory + APIkey + steamID)
matchHistoryText = matchHistoryFile.read()

print matchHistoryText