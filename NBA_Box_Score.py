import psycopg2, psycopg2.extras
import sys # for exit program mgmt
import json

### Set up database
try:
    conn = psycopg2.connect("dbname='NBA_BOXSCORE' user='kerrychou'")
    print("Success connecting to database")
except:
    print("Unable to connect to the database. Check server and credentials.")
    sys.exit(1)

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur.execute('CREATE TABLE IF NOT EXISTS "DAL_POR" ("TEAM" VARCHAR(500) PRIMARY KEY, "Q1" INT, "Q2" INT, "Q3" INT, "Q4" INT, "TOTAL" INT)')

team_box_score_diction = []
Home = {}
Home["TEAM"] = "DAL"
Home["Q1"] = 34
Home["Q2"] = 26
Home["Q3"] = 27
Home["Q4"] = 24
Home["TOTAL"] = 111
team_box_score_diction.append(Home)

Away = {}
Away["TEAM"] = "POR"
Away["Q1"] = 20
Away["Q2"] = 25
Away["Q3"] = 28
Away["Q4"] = 29
Away["TOTAL"] = 102
team_box_score_diction.append(Away)




sql = 'INSERT INTO "DAL_POR" VALUES (%(TEAM)s, %(Q1)s, %(Q2)s, %(Q3)s, %(Q4)s, %(TOTAL)s) ON CONFLICT DO NOTHING'
cur.executemany(sql,team_box_score_diction)
conn.commit()

### AND DONE
conn.close()
