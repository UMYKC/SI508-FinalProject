from selenium import webdriver
from bs4 import BeautifulSoup

browser = webdriver.Chrome() #replace with .Firefox(), or with the browser of your choice
url = "https://stats.nba.com/game/0021800350/"
browser.get(url) #navigate to the page
html_source = browser.page_source
browser.quit()

soup = BeautifulSoup(html_source,'html.parser')
home_and_away_players = soup.find_all(class_="nba-stat-table")
# print(len(home_and_away_players))
away_players = home_and_away_players[0].find_all('tr')
home_players = home_and_away_players[1].find_all('tr')
for player in away_players[:-1]:
    try:
        print(player.a.text)
    except:
        pass

for player in home_players[:-1]:
    try:
        print(player.a.text)
    except:
        pass
