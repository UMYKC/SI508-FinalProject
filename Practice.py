from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
# import pandas as pd
import os

#launch url
url = "http://www.nba.com/games/20181202/PHXLAL#/boxscore"

# create a new Firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(30)
web = driver.get(url)
print(web)

# python_button = driver.find_element_by_id('MainContent_uxLevel1_Agencies_uxAgencyBtn_33') #FHSU
# python_button.click() #click fhsu link
