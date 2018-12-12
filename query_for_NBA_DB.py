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

## Check out the players in Los Angles Lakers
query1 = '''
select *
from "PLAYER_INFO"
where "TEAM" = 'LAL'
'''
## Check out teams which scored over 100 points
query2 = '''
select *
from "BOX_SCORE"
where "DATE" = '{}'
and "FINAL" >= 100
'''.format(time_today_id)

## Check out the player who got triple double, which means that a player get over 10 points, 10 assists, 10 rebounds
query3 = '''
select *
from "PLAYER_STATS"
where "PTS" >= 10
and "REB" >= 10
and "AST" >= 10
'''

## Check out the player who score over 20 points and his field goal percentage is equal or higher than 50%
query4 = '''
select *
from "PLAYER_STATS"
where "PTS" >= 20
and "FG%(FG/FGA)" >= 0.5
'''

cur.execute(query1)
res1 = cur.fetchall()
cur.execute(query2)
res2 = cur.fetchall()
cur.execute(query3)
res3 = cur.fetchall()
cur.execute(query4)
res4 = cur.fetchall()

if __name__ == "__main__":
    print(res1) ## this should print out the Los Angles Lakers's players info(list of list) [['LAL', 40, 'Ivica Zubac', 'C', '7-1', 240],
    ## ['LAL', 14, 'Brandon Ingram', 'SG', '6-9', 190], ['LAL', 2, 'Lonzo Ball', 'PG', '6-6', 190], ['LAL', 0, 'Kyle Kuzma', 'SF', '6-9', 220],
    ## ['LAL', 3, 'Josh Hart', 'SG', '6-5', 215], ['LAL', 15, 'Moritz Wagner', 'C', '6-11', 245], ['LAL', 17, 'Isaac Bonga', 'PG', '6-8', 180],
    ## ['LAL', 1, 'Kentavious Caldwell-Pope', 'SG', '6-5', 205], ['LAL', 9, 'Rajon Rondo', 'PG', '6-1', 186], ['LAL', 23, 'LeBron James', 'PF', '6-8', 250],
    ## ['LAL', 6, 'Lance Stephenson', 'SG', '6-6', 230], ['LAL', 10, 'Svi Mykhailiuk', 'SF', '6-8', 205], ['LAL', 7, 'JaVale McGee', 'C', '7-0', 270],
    ## ['LAL', -1, 'Alex Caruso', 'G', '6-5', 186], ['LAL', 11, 'Michael Beasley', 'PF', '6-9', 235], ['LAL', 19, 'Johnathan Williams', 'C', '6-9', 228],
    ## ['LAL', 5, 'Tyson Chandler', 'C', '7-1', 240]]
    print('''*****************************''')
    print(res2)
    print('''*****************************''')
    print(res3)
    print('''*****************************''')
    print(res4)
