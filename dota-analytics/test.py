from sqlalchemy import create_engine, MetaData

engine = create_engine('sqlite:///flask-dota.db', convert_unicode=True)
metadata = MetaData(bind=engine)

print engine.execute('SELECT * FROM MatchData').first()

print engine.execute('SELECT * FROM HeroData').first()

print engine.execute('SELECT * FROM AbilityData').first()
