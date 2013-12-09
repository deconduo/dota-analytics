from __future__ import absolute_import
from celery import Celery
from api import *
from sqlalchemy import create_engine, MetaData
from settings import APIKey

celery = Celery("tasks",
                broker='redis://localhost:6379/0',
                backend='redis')

@celery.task(name="tasks.celeryData")
def celeryData(steamID, x):
    engine = create_engine('sqlite:///flask-dota.db', convert_unicode=True)
    metadata = MetaData(bind=engine)
    upToDate = False
    lastMatch = get_last_match(steamID, APIKey)
    result = engine.execute('SELECT match_id FROM HeroData WHERE account_id = :1', [steamID])
    for row in result:
        if str(row['match_id']) == str(lastMatch):
            upToDate = True
    result.close()
    if upToDate == False:
        matches = get_player_matches(steamID, APIKey)
        data = get_match_data(matches, APIKey)
        load_data(data)

    queryData = engine.execute('SELECT match_id, gold_per_min, xp_per_min, last_hits, denies, kills, deaths, assists, hero_id FROM HeroData WHERE account_id = :1', [steamID])
    gameData = zip(*queryData)

    return gameData

if __name__ == "__main__":
    celery.start()
