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
NBA_Teams["Charlotte Hornets"] = "CHA"
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



# print(NBA_Matches.items())

def checked(game, NBA_Matches_dict):
    for match in NBA_Matches_dict.items():
        if game == match:
            return True

    return False

get_games_info()
game = ('PHI', 'MEM')
print(checked(game, NBA_Matches))
