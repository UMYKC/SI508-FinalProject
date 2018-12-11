# SI508-FinalProject
YU-KAI CHOU #51054859

# Full instructions are here:

https://paper.dropbox.com/doc/SI-508-Final-Project-Proposal--ASGPsji2Z6NUcZx0M3yV5sNxAg-cflJKwQwD6IWpMUmwhfqQ

# Project Objective
This project will build three tables in NBA_DB via PostgreSQL. Each tables shows users daily NBA games, players' basic information and statistics in each team with SQL select statements.

The reason that I want to do is that I have been watching NBA for 7 years. I always check out the game results on a Taiwan website, called **PTT Bulletin Board System**, instead of NBA.com at the end of every day since the way it performs those games are like

[12/9/2018 Jazz vs Spurs] https://www.ptt.cc/bbs/NBA/M.1544408033.A.95D.html

[12/9/2018 Bucks vs Raptors] https://www.ptt.cc/bbs/NBA/M.1544405017.A.E79.html

![EXAMPLE](https://github.com/UMYKC/SI508-FinalProject/blob/master/Image/NBA_HORNETS_SPURS_PTT.png)

When I saw it for the first time, I thought the style was very cool. Hence, for my final project, I want to use what I have learn in PostgreSQL and make a similar but simplified ones like the following


![BOX SCORE TABLE](https://github.com/UMYKC/SI508-FinalProject/blob/master/Image/BOX_SCORE_TABLE.png)


## Libraries Need to Know
| Library | Description |
| ---- | --- |
| **BeautifulSoup** | Beautiful Soup is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree|
| **Requests** | Requests is a library that enable program to connect to services that store data. Then the services will send back a repository, in which data stored in some structured way|
| **Psycopg** | PostgreSQL is a relational database management systems (RDBMS). And, Psycopg is a PostgreSQL adapter that one can deal with data Pythonically via making queries to the database server|

## Requirements to Run the Program
1. Postgres Database setup

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

![PSQL](https://github.com/UMYKC/SI508-FinalProject/blob/master/Image/PSQL.png)

The name before =# will be your computer user name, which is the default

**Finally, type ```CREATE DATABASE "NBA_DB";``` in the Terminal**

This will create a database called NBA_DB in your PSQL. One can check it by typing ```\l``` and should see something like this in the prompt

![DB](https://github.com/UMYKC/SI508-FinalProject/blob/master/Image/DB.png)


2. Install all the libraries that are needed for this program, simply run these simple command in your terminal of choice:

| Library | Installation |
| ---- | --- |
| **BeautifulSoup** | ``` pip install beautifulsoup4```|
| **Requests** | ``` pip install requests ```|
| **Psycopg** | ``` pip install psycopg2 ```|


## Files in this Repo
Excluding Image file, there are 8 files. They are
1.
