###############################

from bs4 import BeautifulSoup
from alternate_advanced_caching import Cache
from secrets import all_sports_api
from Class import Game, Player
import requests
from datetime import datetime, timedelta
import psycopg2, psycopg2.extras
import json
import sys # for exit program mgmt

DATETIME_FORMAT = "%Y-%m-%d"
## the dates within these three days
list_of_time_id = []
time_today = datetime.today()
time_today_id = time_today.strftime(DATETIME_FORMAT)
time_delta = timedelta(days = 1)
for i in range(3):
    time_id = (time_today - i*time_delta).strftime(DATETIME_FORMAT)
    list_of_time_id.append(time_id)

# print(list_of_time_id)

#################################

'''
##########################################################
Part 0: Setup PSQL and NBA Team Abbreviation Dictionary
##########################################################
'''

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

## Put match(home_team, away_team) in it
NBA_Matches = []
## Put box_score_url in it to check if there is duplicate
Repeated = []

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
def get_games_info():
    base_url = "https://allsportsapi.com/api/basketball/?"
    api_key = all_sports_api
    para_dict = {}
    para_dict["met"] = "Fixtures"
    para_dict["APIkey"] = all_sports_api
    para_dict["from"]= list_of_time_id[1]
    para_dict["to"] = list_of_time_id[0]
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
        pass
        # print("already in cache")

        # url = requests.get(base_url, para_dict).url

    # with open("NBA_games.json", 'w') as f:
    #     f.write(daily_game_text)
    #     f.close()

    games_dict = json.loads(daily_game_text)
    list_of_games = games_dict["result"]
    list_of_game_objects = []
    for game in list_of_games:
        event_date = game["event_date"]
        home_team = NBA_Teams[game["event_home_team"]]
        away_team = NBA_Teams[game["event_away_team"]]
        # home_team = "{} ({})".format(game["event_home_team"], NBA_Teams[game["event_home_team"]])
        # away_team = "{} ({})".format(game["event_away_team"], NBA_Teams[game["event_away_team"]])
        Match = (NBA_Teams[game["event_home_team"]], NBA_Teams[game["event_away_team"]])
        NBA_Matches.append(Match)
        home_score = []
        away_score = []
        final_score = game["event_final_result"].split('-')
        if final_score[0] != '' and final_score[1] != '':
            home_team_final_score = final_score[0]
            away_team_final_score = final_score[1]
            home_score.append(home_team_final_score)
            away_score.append(away_team_final_score)
        else:
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
def checked(game):
    for match in NBA_Matches:
        if game == match:
            return True

    return False

def get_player_stats(home_team_abbr, away_team_abbr):
    # https://www.basketball-reference.com/boxscores/201812020LAL.html
    box_score_id = "{} vs {}".format(away_team_abbr, home_team_abbr)
    # https://www.basketball-reference.com/boxscores/201812080CLE.html
    # https://www.basketball-reference.com/boxscores/201812070CLE.html

    cache_file = "box_score_id.json"
    cache = Cache(cache_file)
    box_score_response_text = cache.get(box_score_id)

    if box_score_response_text == None:
        # response is a string
        if home_team_abbr == "PHX" or home_team_abbr == "BKN":
            for time_id in list_of_time_id:
                time_id = time_id.replace('-', '')
                if home_team_abbr == "PHX":
                    box_score_url = "https://www.basketball-reference.com/boxscores/{}0{}.html".format(time_id, "PHO")
                else:
                    box_score_url = "https://www.basketball-reference.com/boxscores/{}0{}.html".format(time_id, "BRK")
                box_score_response_status = requests.get(box_score_url).status_code
                if box_score_response_status == 200 and box_score_url not in Repeated:
                    Repeated.append(box_score_url)
                    print("send request to {}".format(box_score_id))
                    print(box_score_url)
                    box_score_response_text = requests.get(box_score_url).text
                    break
                else:
                    pass

        else:
            for time_id in list_of_time_id:
                time_id = time_id.replace('-', '')
                box_score_url = "https://www.basketball-reference.com/boxscores/{}0{}.html".format(time_id, home_team_abbr)
                box_score_response_status = requests.get(box_score_url).status_code
                if box_score_response_status == 200 and box_score_url not in Repeated:
                    Repeated.append(box_score_url)
                    print("send request to {}".format(box_score_id))
                    print(box_score_url)
                    box_score_response_text = requests.get(box_score_url).text
                    break
                else:
                    pass

        cache.set(box_score_id, box_score_response_text, 1)

    else:
        print("{} is already in cache".format(box_score_id))

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
            #fg means field goal
            fg = player_info[1].text
            #fga means field goal attempted
            fga = player_info[2].text
            if player_info[3].text != '':
                #fga means field goal/field goal attempted
                fg_percent = player_info[3].text
            else:
                fg_percent = 0
            rebs = player_info[12].text
            asts = player_info[13].text
            stls = player_info[14].text
            blks = player_info[15].text
            pts = player_info[18].text
            player = Player(away_team_abbr, name, min, fg, fga, fg_percent, rebs, asts, stls, blks, pts)
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
            #fg means field goal
            fg = player_info[1].text
            #fga means field goal attempted
            fga = player_info[2].text
            if player_info[3].text != '':
                #fga means field goal/field goal attempted
                fg_percent = player_info[3].text
            else:
                fg_percent = 0
            rebs = player_info[12].text
            asts = player_info[13].text
            stls = player_info[14].text
            blks = player_info[15].text
            pts = player_info[18].text
            player = Player(home_team_abbr, name, min, fg, fga, fg_percent, rebs, asts, stls, blks, pts)
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
#####################################################
'''

def get_players_for_the_team(team_name_abbre):
    team_id = "{}".format(team_name_abbre)
    if team_name_abbre == "BKN":
        team_url = "https://www.basketball-reference.com/teams/BRK/2019.html"
    elif team_name_abbre == "PHX":
        team_url = "https://www.basketball-reference.com/teams/PHO/2019.html"
    else:
        team_url = "https://www.basketball-reference.com/teams/{}/2019.html".format(team_name_abbre)

    cache_file = "Team_Roster.json"
    cache = Cache(cache_file)
    team_response_text = cache.get(team_id)

    if team_response_text == None:
        # response is a string
        team_response_text = requests.get(team_url).text
        cache.set(team_id, team_response_text, 1)
        print("send resquest to {}".format(team_id))

    else:
        # pass
        print("{} is already in cache".format(team_id))


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
def covert_to_roster_diction(roster_list):
    list_of_player_diction = []
    for player in roster_list:
        player_diction = player.table_rep()
        list_of_player_diction.append(player_diction)

    return list_of_player_diction


def convert_to_players_stats_dict(player_stats_in_match):
    list_of_player_stats_diction = []
    list_of_home_player = player_stats_in_match[0]
    list_of_away_player = player_stats_in_match[1]
    for home_player in list_of_home_player:
        if home_player != 0:
            player_stats_diction = home_player.table_rep("Stats")
            list_of_player_stats_diction.append(player_stats_diction)
        else:
            pass

    for away_player in list_of_away_player:
        if away_player != 0:
            player_stats_diction = away_player.table_rep("Stats")
            list_of_player_stats_diction.append(player_stats_diction)
        else:
            pass

    return list_of_player_stats_diction


'''
#####################################################
Part 4: Run code
#####################################################
'''
# Set up database
if __name__ == "__main__":
    try:
        conn = psycopg2.connect("dbname='NBA_DB' user='kerrychou'")
        print("Success connecting to database")
    except:
        print("Unable to connect to the database. Check server and credentials.")
        sys.exit(1)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    table_name = "BOX_SCORE"
    drop_query = '''DROP TABLE IF EXISTS "{}", {}'''.format(table_name, '''"PLAYER_STATS"''')
    cur.execute(drop_query)
    conn.commit()
    query_for_table = 'CREATE TABLE IF NOT EXISTS "{}" ("DATE" VARCHAR(500), "MATCH" VARCHAR(500), "TEAM" VARCHAR(500), "Q1" INT, "Q2" INT, "Q3" INT, "Q4" INT, "FINAL" INT, PRIMARY KEY("MATCH", "TEAM"))'.format(table_name)
    cur.execute(query_for_table)
    conn.commit()

    list_of_games = get_games_info()
    for game in list_of_games:
        team_box_score_diction = game.table_rep()
        sql = 'INSERT INTO "{}" VALUES (%(DATE)s, %(MATCH)s, %(TEAM)s, %(Q1)s, %(Q2)s, %(Q3)s, %(Q4)s, %(TOTAL)s) ON CONFLICT DO NOTHING'.format(table_name)
        cur.executemany(sql,team_box_score_diction)
        conn.commit()

        # print("________________________________________________________________")
        # print(game)
        # print("----------------------------------------------------------------")
        # print('\n')

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
    table_name = "PLAYER_INFO"
    drop_query = '''DROP TABLE IF EXISTS "{}"'''.format(table_name)
    cur.execute(drop_query)
    conn.commit()

    query_for_table = 'CREATE TABLE IF NOT EXISTS "{}" ("TEAM" VARCHAR(500), "NO" INT, "PLAYER" VARCHAR(500) PRIMARY KEY, "POSITION" VARCHAR(500), "HEIGHT" VARCHAR(500), "WEIGHT" INT)'.format(table_name)
    cur.execute(query_for_table)
    conn.commit()
    ### get team roster
    for team_name in NBA_Teams.values():
        try:
            roster_list = get_players_for_the_team(team_name)
            list_of_player_diction = covert_to_roster_diction(roster_list)
            # for player in roster_list:
            #     print(player)
            # table_name = "{}".format(team_name)
            sql = 'INSERT INTO "{}" VALUES (%(Team)s, %(No)s, %(Name)s, %(Position)s, %(Height)s, %(Weight)s) ON CONFLICT DO NOTHING'.format(table_name)
            cur.executemany(sql, list_of_player_diction)
            conn.commit()
        except:
            print("Cannot get players' info from {} ".format(team_name))

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
    table_name = "PLAYER_STATS"
    drop_query = '''DROP TABLE IF EXISTS "{}"'''.format(table_name)
    cur.execute(drop_query)
    conn.commit()

    # query_for_table = 'CREATE TABLE IF NOT EXISTS "{}" ("MATCH" VARCHAR(500), "TEAM" VARCHAR(500), "PLAYER" VARCHAR(500) REFERENCES {}, "MIN" VARCHAR(500), "FG" INT, "FGA" INT, "FG%(FG/FGA)" FLOAT, "REB" INT, "AST" INT, "STL" INT, "BLK" INT, "PTS" INT,  PRIMARY KEY("MATCH", "PLAYER"))'.format(table_name, '''"PLAYER_INFO"("PLAYER")''')
    query_for_table = 'CREATE TABLE IF NOT EXISTS "{}" ("MATCH" VARCHAR(500), "TEAM" VARCHAR(500), "PLAYER" VARCHAR(500), "MIN" VARCHAR(500), "FG" INT, "FGA" INT, "FG%" FLOAT, "REB" INT, "AST" INT, "STL" INT, "BLK" INT, "PTS" INT,  PRIMARY KEY("MATCH", "PLAYER"), FOREIGN KEY ("MATCH", "TEAM") REFERENCES {})'.format(table_name, '''"BOX_SCORE"("MATCH", "TEAM")''')
    cur.execute(query_for_table)
    conn.commit()

    for match in NBA_Matches:
        try:
            player_stats_in_match = get_player_stats(match[0], match[1])
            list_of_player_stats_diction = convert_to_players_stats_dict(player_stats_in_match)
            # print(list_of_player_stats_diction)
            for player_diction in list_of_player_stats_diction:
                player_diction["MATCH"] = "{}|{}".format(match[0], match[1])
            sql = 'INSERT INTO "{}" VALUES (%(MATCH)s, %(Team)s, %(Name)s, %(MIN)s, %(FG)s, %(FGA)s, %(PERCENT)s, %(REB)s, %(AST)s, %(STL)s, %(BLK)s, %(PTS)s) ON CONFLICT DO NOTHING'.format(table_name)
            cur.executemany(sql, list_of_player_stats_diction)
            conn.commit()
        except Exception as e:
            print(e)
            # print("Cannot get info from {} ".format(match))



    ### AND DONE
    conn.close()


    # print(Repeated)
    # print(NBA_Matches)
# A = "MIL"
# A = A.upper()
# B = "GSW"
# B = B.upper()
#
# input_match = (A, B)
# ## First check if the match exist within this two days
# if checked(input_match) == False:
#     print("This match does not exist")
# else:
#     list_of_players = get_player_stats(A, B)
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
