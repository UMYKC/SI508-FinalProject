import psycopg2, psycopg2.extras
import sys # for exit program mgmt
import json
from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d"
## the dates within these three days
time_today = datetime.today()
time_today_id = time_today.strftime(DATETIME_FORMAT)

try:
    conn = psycopg2.connect("dbname='NBA_DB' user='kerrychou'") # TODO make correct for you; create database as necessary
    print("Success connecting to database")
except:
    print("Unable to connect to the database. Check server and credentials.")
    sys.exit(1)

## OK for your database dump to be an output (https://www.postgresql.org/docs/9.6/app-pgdump.html -- scroll to bottom for examples) -- but you should DEFINITELY make queries to
## (a) give examples of useful queries you can make with such a database in a README
## (b) make sure your database REALLY does work and have info it and relationships built as expected!!!

## So...
## Make some type of queries depending upon what you really want your results to be/to test stuff out/to build new CSV files/to create charts --  like...
cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

query1 = '''
select *
from "PLAYER_INFO"
where "TEAM" = 'LAL'
'''

query2 = '''
select *
from "BOX_SCORE"
where "DATE" = '{}'
and "FINAL" >= 100
'''.format(time_today_id)

query3 = '''
select *
from "PLAYER_STATS"
where "PTS" >= 20
and "REB" >= 5
and "AST" >= 5
'''
## Triple Double means that a player get over 10 points, 10 assists, 10 rebounds

cur.execute(query1)
res1 = cur.fetchall()
cur.execute(query2)
res2 = cur.fetchall()
cur.execute(query3)
res3 = cur.fetchall()

if __name__ == "__main__":
    print(res1) ## this should print out the Los Angles Lakers's players info
    print('''*****************************''')
    print(res2) ## this should print out the team which scored over 100 points
    print('''*****************************''')
    print(res3) ## this should print out the player who scored over 20 points, had over 5 rebounds and 5 assists.
