import requests
from bs4 import BeautifulSoup

class Player():
    def __init__(self, name, min = 0, point = 0, assist = 0, rebound = 0, steal = 0, block = 0):
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

#launch url
box_score_url = "https://www.basketball-reference.com/boxscores/201812020MIA.html"

box_score_response_text = requests.get(box_score_url).text
box_score_soup = BeautifulSoup(box_score_response_text, 'html.parser')
home_away_players_list = box_score_soup.find_all('tbody')
# print(len(lst))
away = home_away_players_list[0]
home = home_away_players_list[2]

list_of_away_player = []
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
        continue


list_of_home_player = []
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
        continue


for away_player in list_of_away_player:
    print(away_player)
print('#################################')
for home_player in list_of_home_player:
    print(home_player)
