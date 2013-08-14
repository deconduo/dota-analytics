# Sets up the sqlite3 database

import sqlite3 as lite
import sys

try:
    con = lite.connect('dota-analytics.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE matchDetails(matchID INT, winner TEXT, firstBlood INT, duration INT)")

finally:
    if con:
        con.close()
