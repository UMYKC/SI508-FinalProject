###############################

from bs4 import BeautifulSoup
from alternate_advanced_caching import Cache
import requests
import json
from datetime import datetime, timedelta
from secrets import all_sports_api

DATETIME_FORMAT = "%Y-%m-%d"
time_today = datetime.today()
time_today_id = time_today.strftime(DATETIME_FORMAT)
time_delta = timedelta(days = 1)
time_yesterday = time_today - time_delta
time_yesterday_id = time_yesterday.strftime(DATETIME_FORMAT)

#################################

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
    def __init__(self, name, min = 0, point = 0, rebound = 0, assist = 0, steal = 0, block = 0, ):
        self.name = name
        self.min = min
        self.pts = point
        self.reb = rebound
        self.ast = assist
        self.stl = steal
        self.blk = block

    def __str__(self):
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
            player = Player(name, min, pts, asts, rebs, stls, blks)
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
            player = Player(name, min, pts, asts, rebs, stls, blks)
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
Part 4: Run code
#####################################################
'''
list_of_games = get_games_info()
for game in list_of_games:
    print("________________________________________________________________")
    print(game)
    print("----------------------------------------------------------------")
    print('\n')

A = "phi"
A = A.upper()
B = "mem"
B = B.upper()

input_match = (A, B)
## First check if the match exist within this two days
if checked(input_match) == False:
    print("This match does not exist")
else:
    list_of_players = get_player_info(A, B)
    list_of_home_players = list_of_players[0]
    list_of_away_players = list_of_players[1]
    print("HOME: {}".format(A))
    print("############STARTERS#############")
    for home_player in list_of_home_players:
        if home_player != 0:
            print(home_player)
        else:
            print("****BENCHES****")
    print('#################################')

    print("AWAY: {}".format(B))
    print("############STARTERS#############")
    for away_player in list_of_away_players:
        if away_player != 0:
            print(away_player)
        else:
            print("****BENCHES****")
