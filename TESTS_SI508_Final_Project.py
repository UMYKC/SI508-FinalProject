import unittest
import sys
from SI508_Final_Project import *
from query_for_NBA_DB import *

list_of_games = get_games_info()

class Test1_Setup(unittest.TestCase):
    def test_number_of_NBA_Teams(self):
        self.assertEqual(len(NBA_Teams.items()), 30, "Testing the number of NBA_Teams")
    def test_team_abbre(self):
        self.assertEqual(NBA_Teams["Atlanta Hawks"], "ATL", "Testing the abbreviation of Atlanta Hawks")
        self.assertEqual(NBA_Teams["Brooklyn Nets"], "BKN", "Testing the abbreviation of Brooklyn Nets")
        self.assertEqual(NBA_Teams["New Orleans Pelicans"], "NOP", "Testing the abbreviation of New Orleans Pelican")
        self.assertEqual(NBA_Teams["Phoenix Suns"], "PHX", "Testing the abbreviation of Phoenix Suns")
        self.assertEqual(NBA_Teams["Toronto Raptors"], "TOR", "Testing the abbreviation of Toronto Raptors")
    def test_time_today_id(self):
        self.assertEqual(len(time_today_id), 10, "Testing the length of time_today_id")
        self.assertEqual(len(time_today_id.split('-')), 3, "Testing the number of '-' in time_today_id")
    def test_list_time_id(self):
        self.assertEqual(len(list_of_time_id), 3, "Testing the length of list_of_time_id")

class Test2_Game(unittest.TestCase):
    def test_game_type(self):
        for game in list_of_games:
            self.assertIsInstance(game, Game)
    def test_game_home_away_team(self):
        for game in list_of_games:
            self.assertFalse(game.home_team == game.away_team)
    def test_num_of_NBA_games(self):
        self.assertEqual(len(list_of_games), len(NBA_Matches), "Testing the number of NBA_Matches within these two days")

class Test3_Player(unittest.TestCase):
    def test_player_type(self):
        self.assertIsInstance(get_players_for_the_team("LAL")[3], Player)
    def test_player_team(self):
        player = Player("DAL", "Luka Doncic")
        self.assertEqual(player.team, "DAL")
    def test_player_name(self):
        player = Player("DAL", "Luka Doncic")
        self.assertEqual(player.name, "Luka Doncic")
    def test_player_table_rep(self):
        player = Player("DAL", "Luka Doncic")
        self.assertEqual(len(player.table_rep().keys()), 6)

class Test4_NBA_DB(unittest.TestCase):
    def test_player_existence(self):
        for player_info in res2:
            self.assertIn('LeBron James', player_info[2])



# # class Problem3(unittest.TestCase):
# #     def test_func_var(self):
# #         self.assertEqual(func_var, greeting)
# #     def test_new_digit(self):
# #         self.assertIsInstance(new_digit, int)
# #         self.assertTrue(new_digit<10 and new_digit > -1)
# #     def test_digit_func(self):
# #         self.assertEqual(digit_func, random_digit)
# #


if __name__ == "__main__":
    unittest.main(verbosity=2)
