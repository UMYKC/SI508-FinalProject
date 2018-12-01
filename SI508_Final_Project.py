###############################

from bs4 import BeautifulSoup
from alternate_advanced_caching import Cache
import requests
import json
from datetime import datetime, timedelta
from secrets import all_sports_api

DATETIME_FORMAT = "%Y-%m-%d"
time_today = datetime.today()
time_delta = timedelta(days = 1)
time_yesterday = time_today - time_delta

time_id = time_today.strftime(DATETIME_FORMAT)
#################################


'''
https://paper.dropbox.com/doc/SI-508-Final-Project-Proposal--ASGPsji2Z6NUcZx0M3yV5sNxAg-cflJKwQwD6IWpMUmwhfqQ
'''

def get_games_info():
    base_url = "https://allsportsapi.com/api/basketball/?"
    api_key = all_sports_api
    para_dict = {}
    para_dict["met"] = "Fixtures"
    para_dict["APIkey"] = all_sports_api
    para_dict["from"]= time_yesterday.strftime(DATETIME_FORMAT)
    para_dict["to"] = time_id
    para_dict["leagueId"] = "787" #League ID - if set events from specific league will be returned (Optional)

    cache_file = "NBA_Cache.json"
    cache = Cache(cache_file)
    daily_game_text = cache.get(time_id)

    if daily_game_text == None:
        # response is a string
        daily_game_text = requests.get(base_url, para_dict).text
        cache.set(time_id, daily_game_text, 1)
        print("send requests")
    else:
        print("already in cache")

        # url = requests.get(base_url, para_dict).url

    games_dict = json.loads(daily_game_text)
    list_of_games = games_dict["result"]
    list_of_game_objects = []
    for game in list_of_games[1:]:
        home_team = game["event_home_team"]
        # print(home_team)
        away_team = game["event_away_team"]
        # print(away_team)
        home_score = []
        away_score = []
        final_score = game["event_final_result"].split('-')
        home_team_final_score = final_score[0]
        away_team_final_score = final_score[1]
        home_score.append(home_team_final_score)
        away_score.append(away_team_final_score)
        # print([home_team_final_score, away_team_final_score])
        for quarter, score in game["scores"].items():
            # print(score[0]["score_home"])
            home_score.append(score[0]["score_home"])
            away_score.append(score[0]["score_away"])

        one_game = Game(home_team, away_team, home_score, away_score)
        list_of_game_objects.append(one_game)

    return list_of_game_objects

# home_score is a int list, like [136, 39, 31, 40, 26]

class Game():
    def __init__(self, home_team, away_team, home_score, away_score):
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
        home = "Home: {}| Total:{}| 1Q: {}| 2Q: {}| 3Q: {}| 4Q: {}".format(self.home_team, self.home_total_score, self.home1Q, self.home2Q, self.home3Q, self.home4Q)
        away = "Away: {}| Total:{}| 1Q: {}| 2Q: {}| 3Q: {}| 4Q: {}".format(self.away_team, self.away_total_score, self.away1Q, self.away2Q, self.away3Q, self.away4Q)
        return home + '\n' + away



list_of_games = get_games_info()
for game in list_of_games:
    print("________________________________________________________________")
    print(game)
    print("----------------------------------------------------------------")
    print('\n')
