import unittest
import os
from playerinfo import Player
import requests
from database_connection import get_database_connection
from search import get_h2h_record, get_player_base_stats, get_players, total_score, reverse_score, top_10_base_stats, top_date, get_newest_rating, get_player_matches

class TestSearch(unittest.TestCase):

    def setUp(self):
        self.connection = get_database_connection()
        self.session = requests.Session()
    
    def test_total_score_correct(self):
        score = '8,-9,7,10'
        total = total_score(score)
        self.assertEqual(total, ('3-1', 'win'))

    def test_total_score_fail(self):
        score = '8,-9,?,10'
        total = total_score(score)
        self.assertEqual(total, ('fail', 'fail'))

    def test_reverse_score_correct(self):
        score = '8,-9,7,10'
        reverse = reverse_score(score)
        self.assertEqual(reverse, '-8,9,-7,-10')

    def test_reverse_score_fail(self):
        score = '8,-9,?,10'
        reverse = reverse_score(score)
        self.assertEqual(reverse, 'fail')

    def test_get_players_length(self):
        players = get_players()
        self.assertEqual(len(players), 3561)

    def test_get_player_base_stats(self):
        stats = get_player_base_stats('Olah Benedek')
        self.assertEqual(stats, """1 Olah Benedek SeSi 2625
    all time wins: 25
    all time losses: 0
    All time win rate: 100.0% """)
        
    def test_top_10_base_stats(self):
        stats = top_10_base_stats()
        self.assertEqual(stats[0], """1 Olah Benedek SeSi 2625
    all time wins: 25
    all time losses: 0
    All time win rate: 100.0% """)
        
    def test_h2h_record_correct(self):
        h2h = get_h2h_record('Räsänen Aleksi', 'Tennilä Otto')
        self.assertEqual(h2h, 'Räsänen Aleksi and Tennilä Otto have played 8 times and Räsänen Aleksi has won 1 of them and Tennilä Otto 7')

    def test_h2h_record_empty(self):
        h2h = get_h2h_record('Prusa David', 'Olah Benedek')
        self.assertEqual(h2h, 'Prusa David and Olah Benedek have played 0 times')

    def test_top_date(self):
        date = top_date()
        self.assertEqual(date, '23.11.2025')

    def test_get_newest_rating(self):
        get_newest_rating()
        rows = []
        with open('ratinglist', 'r') as f:
                    for i in range(5):
                        rows.append(f.readline().strip())
        print(rows)
        self.assertEqual(rows[1], 'Rating-julkaisu 23.11.2025')
        if os.path.exists("ratinglist"):
            os.remove("ratinglist")


    def test_get_player_matches(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM All_matches WHERE player_name == 'Pihkala Arttu'")
        player = Player(1, 'Pihkala Arttu', 'PihkaArtt', 'PT Espoo', '2423')
        get_player_matches(player, self.connection, self.session)
        stats = get_player_base_stats('Pihkala Arttu')
        self.assertEqual(stats, """10 Pihkala Arttu PT Espoo 2423
    all time wins: 411
    all time losses: 197
    All time win rate: 67.6% """)