'''
#####################################################
Building Classes: Game, Player
#####################################################
'''

'''
#####################################################
Game
#####################################################
'''

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


    def table_rep(self):
        team_box_score_diction = []
        home_abbre = self.home_team.split(' ')[-1].strip('(').strip(')')
        away_abbre = self.away_team.split(' ')[-1].strip('(').strip(')')
        match1 = "{}|{}".format(home_abbre, away_abbre)
        match2 = "{}|{}".format(away_abbre, home_abbre)

        Home = {}
        Home["DATE"] = self.date
        Home["MATCH"] = match1
        Home["TEAM"] = "{}".format(self.home_team)
        Home["Q1"] = self.home1Q
        Home["Q2"] = self.home2Q
        Home["Q3"] = self.home3Q
        Home["Q4"] = self.home4Q
        Home["TOTAL"] = self.home_total_score
        team_box_score_diction.append(Home)

        Away = {}
        Away["DATE"] = self.date
        Away["MATCH"] = match2
        Away["TEAM"] = "{}".format(self.away_team)
        Away["Q1"] = self.away1Q
        Away["Q2"] = self.away2Q
        Away["Q3"] = self.away3Q
        Away["Q4"] = self.away4Q
        Away["TOTAL"] = self.away_total_score
        team_box_score_diction.append(Away)

        return team_box_score_diction

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

    def table_rep(self, arg = "Team"):
        player_diction = {}
        player_diction["Team"] = self.team
        player_diction["Name"] = self.name
        if arg == "Team":
            if self.no != '':
                player_diction["No"] = self.no
            else:
                player_diction["No"] = -1
            player_diction["Position"] = self.position
            player_diction["Height"] = self.height
            player_diction["Weight"] = self.weight
        else:
            player_diction["MIN"] = self.min
            player_diction["PTS"] = self.pts
            player_diction["REB"] = self.reb
            player_diction["AST"] = self.ast
            player_diction["STL"] = self.stl
            player_diction["BLK"] = self.blk

        return player_diction
