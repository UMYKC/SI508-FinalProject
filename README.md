# SI508-FinalProject
YU-KAI CHOU #51054859

# Full instructions are here:

https://paper.dropbox.com/doc/SI-508-Final-Project-Proposal--ASGPsji2Z6NUcZx0M3yV5sNxAg-cflJKwQwD6IWpMUmwhfqQ

# Project Objective
The output of this project is three tables in a relational database called NBA_DB. The tables are named "BOX_SCORE", "PLAYER_INFO" and "PLAYER_STATS" individually, which show users daily NBA game results, players' basic information and statistics in each team. In addition, by using SQL SELECT statements and WHERE clause, served as a filter, users can find some desired result between tables.

The reason that I want to do is that I have been watching NBA for 7 years. I always check out the game results on a Taiwan website, called **PTT Bulletin Board System**, instead of NBA.com at the end of every day since the way it performs those games are like

[12/9/2018 Jazz vs Spurs] https://www.ptt.cc/bbs/NBA/M.1544408033.A.95D.html


<p align="center">
  <img src="https://github.com/UMYKC/SI508-FinalProject/blob/master/Image/NBA_Bucks_Raptors_PTT.png" height="382" width="748">
</p>

When I saw it for the first time, I thought the style was very cool. Hence, for my final project, I want to use what I have learn in PostgreSQL and make a similar but simplified ones like the following

<p align="center">
  <img src="https://github.com/UMYKC/SI508-FinalProject/blob/master/Image/BOX_SCORE_TABLE.png" height="116" width="538">
</p>

## Libraries Need to Know
| Library | Description |
| ---- | --- |
| **BeautifulSoup** | Beautiful Soup is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree|
| **Requests** | Requests is a library that enable program to connect to services that store data. Then the services will send back a repository, in which data stored in some structured way|
| **Psycopg** | PostgreSQL is a relational database management systems (RDBMS). By using it, users can build their own database and tables. And, Psycopg is a PostgreSQL adapter that one can deal with data Pythonically via making queries to the database server|

## Requirements to Run the Program
**1. Postgres database setup**

**For mac only! (Postgres is not for mac only, but this setup is for mac only.)**

| Step | Paste to Command Line |
| ---- | --- |
| **Get homebrew** | ``` /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"```|
| **Install the postgresql database** | ``` brew install postgres ```|
| **Start the database server** | ``` pg_ctl -D /usr/local/var/postgres start ```|

Other useful commands for starting/stopping psql db server (in general) — you may want to refer to these in future:


|  |Enter in Command Line |
| ---- | --- |
| **Check Status** | ```pg_ctl -D /usr/local/var/postgres status```|
| **Start the server** | ```pg_ctl -D /usr/local/var/postgres start```|
| **Stop the server** | ```pg_ctl -D /usr/local/var/postgres stop```|


If you restart your computer, for example, you’ll need to run that ^ start command to start up the DB server.

After starting the server, one can open a new Terminal window. But all is well! This server will run in the background.


**Type ```psql``` in the new Terminal**

Then one now should see a different prompt, something like this

<p align="center">
  <img src="https://github.com/UMYKC/SI508-FinalProject/blob/master/Image/PSQL.png" height="63" width="156">
</p>

The name before =# will be your computer user name, which is the default

**Finally, type ```CREATE DATABASE "NBA_DB";``` in the Terminal**

This will create a database called NBA_DB in your PSQL. One can check it by typing ```\l``` and should see something like this in the prompt

<p align="center">
  <img src="https://github.com/UMYKC/SI508-FinalProject/blob/master/Image/DB.png" height="100" width="440">
</p>

**2. Install all the libraries that are needed for this program, simply run these simple command in your terminal of choice:**

| Library | Installation |
| ---- | --- |
| **BeautifulSoup** | ``` pip install beautifulsoup4```|
| **Requests** | ``` pip install requests ```|
| **Psycopg** | ``` pip install psycopg2 ```|


## Files in this Repo
Excluding Image file, there are 8 files.

| File Name | Description |
| ---- | --- |
| **DataBase_Archive** |A old version of NBA_DB that I archived. One can load this database, including three tables by entering 1. ```createdb old_nba_db``` 2. cd to SI508-FinalProject file and ```pg_restore -d old_nba_db DataBase_Archive```  in terminal|
| **Class.py** | Define two classes, Game and Player|
| **README.md** | Includes all the information one needs to know, setup, and run for this project|
| **SI508_Final_Project.py** | The main file to run with python|
| **TESTS_SI508_Final_Project.py** | The test suite file to see whether SI508_Final_Project.py passes 11 test methods|
| **alternate_advanced_caching.py** | Define a class called Cache. It will do caching but with expiry time|
| **query_for_NBA_DB.py** | The example code of making queries depending upon what users might want to find out from the tables|
| **secrets.py** | Where users should put their own API key, requested from All Sports API website|


## Running Programs

After the setup, one should clone the repo to your desired directory.
Second, check out the secrets.py and apply for your own All Sports API key.
Finally, as soon as receiving the API key and paste it to secrets.py, one can run the program in the terminal by the following steps.

| Step | Command |
| ---- | --- |
| **1. Change directory to the SI508-FinalProject folder** | ``` cd SI508-FinalProject ```|
| **2. Run SI508_Final_Project.py** | ``` python SI508_Final_Project.py ```|
| **3. Go to PSQL** | ``` psql ```|
| **4. Check databases** | ``` \l ```|
| **5. Connect to NBA_DB** | ``` \c NBA_DB ```|
| **6. Check tables** | ``` \dt ```|
| **7. Get into Table BOX_SCORE, like Fig. 1** | ``` select * from "BOX_SCORE"; ```|
| **8. Get into Table PLAYER_INFO, like Fig. 2** | ``` select * from "PLAYER_INFO"; ```|
| **9. Get into Table PLAYER_STATS, like Fig. 3** | ``` select * from "PLAYER_STATS"; ```|

<p align="center">
  <img src="https://github.com/UMYKC/SI508-FinalProject/blob/master/Image/BOX_SCORE.png" height="100" width="362">
  <img src="https://github.com/UMYKC/SI508-FinalProject/blob/master/Image/PLAYER_INFO.png" height="190" width="308">
  <img src="https://github.com/UMYKC/SI508-FinalProject/blob/master/Image/PLAYER_STATS.png" height="245" width="324">
</p>

**Note: a statement must be terminated with semicolon ;**

| Useful commands in PSQL| Description |
| ---- | --- |
| ```\?```| list all the commands |
| ```\l```| list databases |
| ```\c [DBNAME]```| connect to new database |
| ```\dt```| list tables |
| ```q```|  quit table |
| ```\q```| quit psql |

## Running Test Suites
