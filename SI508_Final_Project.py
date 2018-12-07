###############################

from bs4 import BeautifulSoup
from alternate_advanced_caching import Cache
import requests
from datetime import datetime, timedelta
from secrets import all_sports_api
import psycopg2, psycopg2.extras
import sys # for exit program mgmt
import json

DATETIME_FORMAT = "%Y-%m-%d"
time_today = datetime.today()
time_today_id = time_today.strftime(DATETIME_FORMAT)
time_delta = timedelta(days = 1)
time_yesterday = time_today - time_delta
time_yesterday_id = time_yesterday.strftime(DATETIME_FORMAT)

#################################

'''
##########################################################
Part 0: Setup PSQL and NBA Team Abbreviation Dictionary
##########################################################
'''

# cur.execute('CREATE TABLE IF NOT EXISTS "DAL_POR" ("TEAM" VARCHAR(500) PRIMARY KEY, "Q1" INT, "Q2" INT, "Q3" INT, "Q4" INT, "TOTAL" INT)')


# DATE_FORMAT_FOR_SCRAPING = "%Y%m%d"
# time_for_url = datetime.today().strftime(DATE_FORMAT_FOR_SCRAPING)

NBA_Teams = {}
NBA_Teams["Atlanta Hawks"] = "ATL"
NBA_Teams["Brooklyn Nets"] = "BKN"
NBA_Teams["Boston Celtics"] = "BOS"
NBA_Teams["Charlotte Hornets"] = "CHO"
NBA_Teams["Chicago Bulls"] = "CHI"
NBA_Teams["Cleveland Cavaliers"] = "CLE"
NBA_Teams["Dallas Mavericks"] = "DAL"
NBA_Teams["Denver Nuggets"] = "DEN"
NBA_Teams["Detroit Pistons"] = "DET"
NBA_Teams["Golden State Warriors"] = "GSW"
NBA_Teams["Houston Rockets"] = "HOU"
NBA_Teams["Indiana Pacers"] = "IND"
NBA_Teams["Los Angeles Clippers"] = "LAC"
NBA_Teams["Los Angeles Lakers"] = "LAL"
NBA_Teams["Memphis Grizzlies"] = "MEM"
NBA_Teams["Miami Heat"] = "MIA"
NBA_Teams["Milwaukee Bucks"] = "MIL"
NBA_Teams["Minnesota Timberwolves"] = "MIN"
NBA_Teams["New Orleans Pelicans"] = "NOP"
NBA_Teams["New York Knicks"] = "NYK"
NBA_Teams["Oklahoma City Thunder"] = "OKC"
NBA_Teams["Orlando Magic"] = "ORL"
NBA_Teams["Philadelphia 76ers"] = "PHI"
NBA_Teams["Phoenix Suns"] = "PHX"
NBA_Teams["Portland Trail Blazers"] = "POR"
NBA_Teams["Sacramento Kings"] = "SAC"
NBA_Teams["San Antonio Spurs"] = "SAS"
NBA_Teams["Toronto Raptors"] = "TOR"
NBA_Teams["Utah Jazz"] = "UTA"
NBA_Teams["Washington Wizards"] = "WAS"

NBA_Matches = {}

'''
https://paper.dropbox.com/doc/SI-508-Final-Project-Proposal--ASGPsji2Z6NUcZx0M3yV5sNxAg-cflJKwQwD6IWpMUmwhfqQ
'''
'''
#####################################################
Part 1: Use RESTful API and Scraping Building Classes
#####################################################
'''

'''
#####################################################
Game
#####################################################
'''
# home_score is a int list, like [136, 39, 31, 40, 26]

class Game():
    def __init__(self, event_date, home_team, away_team, home_score, away_score):
        self.date = event_date
        self.home_team = home_team
        self.home_total_score = home_score[0]
        self.home1Q = home_score[1]
        self.home2Q = home_score[2]
        self.home3Q = home_score[3]
        self.home4Q = home_score[4]

        self.away_team = away_team
        self.away_total_score = away_score[0]
        self.away1Q = away_score[1]
        self.away2Q = away_score[2]
        self.away3Q = away_score[3]
        self.away4Q = away_score[4]


    def __str__(self):
        date = self.date
        home = "Home: {}| Total:{}| 1Q: {}| 2Q: {}| 3Q: {}| 4Q: {}".format(self.home_team, self.home_total_score, self.home1Q, self.home2Q, self.home3Q, self.home4Q)
        away = "Away: {}| Total:{}| 1Q: {}| 2Q: {}| 3Q: {}| 4Q: {}".format(self.away_team, self.away_total_score, self.away1Q, self.away2Q, self.away3Q, self.away4Q)
        return date + '\n' + home + '\n' + away

def get_games_info():
    base_url = "https://allsportsapi.com/api/basketball/?"
    api_key = all_sports_api
    para_dict = {}
    para_dict["met"] = "Fixtures"
    para_dict["APIkey"] = all_sports_api
    para_dict["from"]= time_yesterday_id
    para_dict["to"] = time_today_id
    para_dict["leagueId"] = "787" #League ID - if set events from specific league will be returned (Optional)

    cache_file = "NBA_Cache.json"
    cache = Cache(cache_file)
    daily_game_text = cache.get(time_today_id)

    if daily_game_text == None:
        # response is a string
        daily_game_text = requests.get(base_url, para_dict).text
        cache.set(time_today_id, daily_game_text, 1)
        print("send requests")
    else:
        print("already in cache")

        # url = requests.get(base_url, para_dict).url

    # with open("NBA_games.json", 'w') as f:
    #     f.write(daily_game_text)
    #     f.close()

    games_dict = json.loads(daily_game_text)
    list_of_games = games_dict["result"]
    list_of_game_objects = []
    for game in list_of_games:
        event_date = game["event_date"]
        home_team = "{} ({})".format(game["event_home_team"], NBA_Teams[game["event_home_team"]])
        # print(home_team)
        away_team = "{} ({})".format(game["event_away_team"], NBA_Teams[game["event_away_team"]])
        # print(away_team)
        NBA_Matches[NBA_Teams[game["event_home_team"]]] = NBA_Teams[game["event_away_team"]]
        home_score = []
        away_score = []
        final_score = game["event_final_result"].split('-')
        try:
            home_team_final_score = final_score[0]
            away_team_final_score = final_score[1]
            home_score.append(home_team_final_score)
            away_score.append(away_team_final_score)
        except:
            home_score.append(0)
            away_score.append(0)
        # print([home_team_final_score, away_team_final_score])
        for quarter, score in game["scores"].items():
            # print(score[0]["score_home"])
            try:
                home_score.append(score[0]["score_home"])
                away_score.append(score[0]["score_away"])
            except:
                home_score.append(0)
                away_score.append(0)


        one_game = Game(event_date, home_team, away_team, home_score, away_score)
        list_of_game_objects.append(one_game)

    return list_of_game_objects

'''
#####################################################
Player
#####################################################
'''
class Player():
    def __init__(self, team, name, min = 0, point = 0, rebound = 0, assist = 0, steal = 0, block = 0, no = -1, position = "PG", height = "7-0", weight = 230):
        self.team = team
        self.name = name
        self.min = min
        self.pts = point
        self.reb = rebound
        self.ast = assist
        self.stl = steal
        self.blk = block
        self.no = no
        self.position = position
        self.height = height
        self.weight = weight

    def __str__(self, arg = "Team"):
        if arg == "Team":
            s = "Team: {}, No.{}, {}, Pos: {}, Ht: {}, Wt: {}".format(self.team, self.no, self.name, self.position, self.height, self.weight)
        else:
            s = "In this game, {} got {} points, {} rebounds, {} assists in {} minutes".format(self.name, self.pts, self.reb, self.ast, self.min.split(':')[0])
        return s

def checked(game):
    for match in NBA_Matches.items():
        if game == match:
            return True

    return False

def get_player_info(home_team_abbr, away_team_abbr):
    # https://www.basketball-reference.com/boxscores/201812020LAL.html
    # time_today_id = time_today.strftime(DATETIME_FORMAT)
    # 2018-12-03
    # time_yesterday_id = time_yesterday.strftime(DATETIME_FORMAT)
    # 2018-12-02
    box_score_date1 = time_today_id.replace('-', '')
    box_score_date2 = time_yesterday_id.replace('-', '')
    # away_team_abbr = away_team_abbr.upper()
    # home_team_abbr = home_team_abbr.upper()
    box_score_url1 = "https://www.basketball-reference.com/boxscores/{}0{}.html".format(box_score_date1, home_team_abbr)
    box_score_url2 = "https://www.basketball-reference.com/boxscores/{}0{}.html".format(box_score_date2, home_team_abbr)
    box_score_id = "{} vs {}".format(away_team_abbr, home_team_abbr)

    cache_file = "box_score_id.json"
    cache = Cache(cache_file)
    box_score_response_text = cache.get(box_score_id)

    if box_score_response_text == None:
        # response is a string
        box_score_response_status1 = requests.get(box_score_url1).status_code
        # print("box_score_response_text1: {}".format(box_score_response_text1))
        # print("##############################################################")
        box_score_response_status2 = requests.get(box_score_url2).status_code
        # print("box_score_response_text2: {}".format(box_score_response_text2))
        if box_score_response_status1 == 200:
            box_score_url = box_score_url1
            box_score_response_text = requests.get(box_score_url1).text
        else:
            box_score_url = box_score_url2
            box_score_response_text = requests.get(box_score_url2).text

        cache.set(box_score_id, box_score_response_text, 1)
        print("send resquest to {}".format(box_score_id))

    else:
        print("{} is already in cache".format(box_score_id))

    # print(box_score_url)

    box_score_soup = BeautifulSoup(box_score_response_text, 'html.parser')
    # print(box_score_soup.prettify())
    lst = box_score_soup.find_all('tbody')
    # print(len(lst))
    away = lst[0]
    home = lst[2]
    list_of_away_player = []
    list_of_home_player = []

    away_count = 0
    for player in away.find_all('tr'):
        try:
            name = player.a.text
            player_info = player.find_all("td")
            # print(player_info[0].text)
            # print(player_info[17].text)
            min = player_info[0].text
            pts = player_info[18].text
            rebs = player_info[12].text
            asts = player_info[13].text
            stls = player_info[14].text
            blks = player_info[15].text
            player = Player(away_team_abbr, name, min, pts, asts, rebs, stls, blks)
            list_of_away_player.append(player)
        except:
            if away_count == 0:
                away_count += 1
                list_of_away_player.append(0)
            else:
                pass

    home_count = 0
    for player in home.find_all('tr'):
        try:
            name = player.a.text
            player_info = player.find_all("td")
            min = player_info[0].text
            pts = player_info[18].text
            rebs = player_info[12].text
            asts = player_info[13].text
            stls = player_info[14].text
            blks = player_info[15].text
            player = Player(home_team_abbr, name, min, pts, asts, rebs, stls, blks)
            list_of_home_player.append(player)
        except:
            if home_count == 0:
                home_count += 1
                list_of_home_player.append(0)
            else:
                pass

    return [list_of_home_player, list_of_away_player]


'''
scraping example https://www.nba.com/games/20181201/BKNWAS#/boxscore
'''

'''
#####################################################
Part 2: Functions
<1> get_players_for_the_team()
<2> get_wins_and_loses_to_date()
#####################################################
'''
# class Roster():
#     def __init__(self, name, no, position, height, weight):
#         self.name = name
#         self.no = no
#         self.position = position
#         self.height = height
#         self.weight = weight
#
#     def __str__(self):
#         s = "No.{}, {}, Pos: {}, Ht: {}, Wt: {}".format(self.no, self.name, self.position, self.height, self.weight)
#         return s

def get_players_for_the_team(team_name_abbre):
    team_url = "https://www.basketball-reference.com/teams/{}/2019.html".format(team_name_abbre)
    team_id = "{}".format(team_name_abbre)

    cache_file = "Team_Roster.json"
    cache = Cache(cache_file)
    team_response_text = cache.get(team_id)

    if team_response_text == None:
        # response is a string
        team_response_text = requests.get(team_url).text
        cache.set(team_id, team_response_text, 1)
        print("send resquest to {}".format(team_id))

    else:
        print("{} is already in cache".format(team_id))

    # print(box_score_url)

    team_roster_soup = BeautifulSoup(team_response_text, 'html.parser')
    team_roster_table = team_roster_soup.find(class_ = "overthrow table_container").tbody
    team_roster_list = team_roster_table.find_all('tr')
    roster_list = []
    for player in team_roster_list:
        player_name = player.a.text
        player_no = player.th.text
        player_info = player.find_all('td')
        player_position = player_info[1].text
        player_height = player_info[2].text
        player_weight = player_info[3].text
        player = Player(team_name_abbre, player_name, no = player_no, position = player_position, height = player_height, weight = player_weight)
        roster_list.append(player)

    return roster_list




'''
#####################################################
Part 3: A clear visualization of data, Table in PSQL
<1> Make dictionary for create table
#####################################################
'''
# make_diction_for_psql
# game.home_team, game.home_total_score, game.home1Q, game.home2Q, game.home3Q, game.home4Q
def covert_to_game_diction(game):
    team_box_score_diction = []
    home_abbre = game.home_team.split(' ')[-1].strip('(').strip(')')
    away_abbre = game.away_team.split(' ')[-1].strip('(').strip(')')
    match1 = "{}|{}".format(home_abbre, away_abbre)
    match2 = "{}|{}".format(away_abbre, home_abbre)

    Home = {}
    Home["DATE"] = game.date
    Home["MATCH"] = match1
    Home["TEAM"] = "{}".format(game.home_team)
    Home["Q1"] = game.home1Q
    Home["Q2"] = game.home2Q
    Home["Q3"] = game.home3Q
    Home["Q4"] = game.home4Q
    Home["TOTAL"] = game.home_total_score
    team_box_score_diction.append(Home)

    Away = {}
    Away["DATE"] = game.date
    Away["MATCH"] = match2
    Away["TEAM"] = "{}".format(game.away_team)
    Away["Q1"] = game.away1Q
    Away["Q2"] = game.away2Q
    Away["Q3"] = game.away3Q
    Away["Q4"] = game.away4Q
    Away["TOTAL"] = game.away_total_score
    team_box_score_diction.append(Away)

    return team_box_score_diction

def covert_to_roster_diction(roster_list):
    list_of_player_diction = []
    for player in roster_list:
        player_diction = {}
        player_diction["Team"] = player.team
        if player.no != '':
            player_diction["No"] = player.no
        else:
            player_diction["No"] = -1
        player_diction["Name"] = player.name
        player_diction["Position"] = player.position
        player_diction["Height"] = player.height
        player_diction["Weight"] = player.weight
        list_of_player_diction.append(player_diction)

    return list_of_player_diction







'''
#####################################################
Part 4: Run code
#####################################################
'''
## Set up database
try:
    conn = psycopg2.connect("dbname='NBA_DB' user='kerrychou'")
    print("Success connecting to database")
except:
    print("Unable to connect to the database. Check server and credentials.")
    sys.exit(1)

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
list_of_games = get_games_info()
for game in list_of_games:
    team_box_score_diction = covert_to_game_diction(game)
    table_name = "BOX_SCORE"
    query_for_table = 'CREATE TABLE IF NOT EXISTS "{}" ("DATE" VARCHAR(500), "MATCH" VARCHAR(500) PRIMARY KEY, "TEAM" VARCHAR(500), "Q1" INT, "Q2" INT, "Q3" INT, "Q4" INT, "FINAL" INT)'.format(table_name)
    cur.execute(query_for_table)
    sql = 'INSERT INTO "{}" VALUES (%(DATE)s, %(MATCH)s, %(TEAM)s, %(Q1)s, %(Q2)s, %(Q3)s, %(Q4)s, %(TOTAL)s) ON CONFLICT DO NOTHING'.format(table_name)
    cur.executemany(sql,team_box_score_diction)
    conn.commit()

    print("________________________________________________________________")
    print(game)
    print("----------------------------------------------------------------")
    print('\n')

### AND DONE
conn.close()


## Set up database
try:
    conn = psycopg2.connect("dbname='NBA_DB' user='kerrychou'")
    print("Success connecting to database")
except:
    print("Unable to connect to the database. Check server and credentials.")
    sys.exit(1)

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

### get team roster
for team_name in NBA_Teams.values():
    try:
        roster_list = get_players_for_the_team(team_name)
        list_of_player_diction = covert_to_roster_diction(roster_list)
        # for player in roster_list:
        #     print(player)
        # table_name = "{}".format(team_name)
        table_name = "Player_Info"
        query_for_table = 'CREATE TABLE IF NOT EXISTS "{}" ("Team" VARCHAR(500), "NO" INT, "Player" VARCHAR(500) PRIMARY KEY, "Position" VARCHAR(500), "Height" VARCHAR(500), "Weight" INT)'.format(table_name)
        cur.execute(query_for_table)
        sql = 'INSERT INTO "{}" VALUES (%(Team)s, %(No)s, %(Name)s, %(Position)s, %(Height)s, %(Weight)s) ON CONFLICT DO NOTHING'.format(table_name)
        cur.executemany(sql, list_of_player_diction)
        conn.commit()
    except:
        if team_name == "BKN":
            roster_list = get_players_for_the_team("BRK")
            list_of_player_diction = covert_to_roster_diction(roster_list)
            # for player in roster_list:
            #     print(player)
            # table_name = "{}".format(team_name)
            table_name = "Player_Info"
            query_for_table = 'CREATE TABLE IF NOT EXISTS "{}" ("Team" VARCHAR(500), "NO" INT, "Player" VARCHAR(500) PRIMARY KEY, "Position" VARCHAR(500), "Height" VARCHAR(500), "Weight" INT)'.format(table_name)
            cur.execute(query_for_table)
            sql = 'INSERT INTO "{}" VALUES (%(Team)s, %(No)s, %(Name)s, %(Position)s, %(Height)s, %(Weight)s) ON CONFLICT DO NOTHING'.format(table_name)
            cur.executemany(sql, list_of_player_diction)
            conn.commit()
        elif team_name == "PHX":
            roster_list = get_players_for_the_team("PHO")
            list_of_player_diction = covert_to_roster_diction(roster_list)
            # for player in roster_list:
            #     print(player)
            # table_name = "{}".format(team_name)
            table_name = "Player_Info"
            query_for_table = 'CREATE TABLE IF NOT EXISTS "{}" ("Team" VARCHAR(500), "NO" INT, "Player" VARCHAR(500) PRIMARY KEY, "Position" VARCHAR(500), "Height" VARCHAR(500), "Weight" INT)'.format(table_name)
            cur.execute(query_for_table)
            sql = 'INSERT INTO "{}" VALUES (%(Team)s, %(No)s, %(Name)s, %(Position)s, %(Height)s, %(Weight)s) ON CONFLICT DO NOTHING'.format(table_name)
            cur.executemany(sql, list_of_player_diction)
            conn.commit()
        else:
            print("Cannot get players' info from {} ".format(team_name))

### AND DONE
conn.close()


# A = "IND"
# A = A.upper()
# B = "CHI"
# B = B.upper()
#
# input_match = (A, B)
# ## First check if the match exist within this two days
# if checked(input_match) == False:
#     print("This match does not exist")
# else:
#     list_of_players = get_player_info(A, B)
#     list_of_home_players = list_of_players[0]
#     list_of_away_players = list_of_players[1]
#     print("HOME: {}".format(A))
#     print("############STARTERS#############")
#     for home_player in list_of_home_players:
#         if home_player != 0:
#             print(home_player.__str__("stats"))
#         else:
#             print("****BENCHES****")
#     print('#################################')
#
#     print("AWAY: {}".format(B))
#     print("############STARTERS#############")
#     for away_player in list_of_away_players:
#         if away_player != 0:
#             print(away_player.__str__("stats"))
#         else:
#             print("****BENCHES****")
