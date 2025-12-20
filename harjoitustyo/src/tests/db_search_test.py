import unittest
from database_connection import get_database_connection
from db_search import get_h2h_record, get_player_base_stats, get_players, top_10_base_stats, get_seasonal_stats

class TestSearch(unittest.TestCase):

    def setUp(self):
        self.connection = get_database_connection()
        self.cursor = self.connection.cursor()


    def test_get_players_length(self):
        players = get_players(self.cursor)
        self.assertGreater(len(players), 3500)

    def test_get_player_base_stats(self):
        stats = get_player_base_stats('Olah Benedek', self.cursor)
        self.assertEqual(stats, """1 Olah Benedek SeSi 2625
    all time wins: 25
    all time losses: 0
    All time win rate: 100.0% """)
        
    def test_top_10_base_stats(self):
        stats = top_10_base_stats(self.cursor)
        self.assertEqual(stats[0], """1 Olah Benedek SeSi 2625
    all time wins: 25
    all time losses: 0
    All time win rate: 100.0% """)
        
    def test_h2h_record_correct(self):
        h2h = get_h2h_record('Räsänen Aleksi', 'Tennilä Otto', self.cursor)
        self.assertEqual(h2h, 'Räsänen Aleksi and Tennilä Otto have played 8 times and Räsänen Aleksi has won 1 of them and Tennilä Otto 7')

    def test_h2h_record_empty(self):
        h2h = get_h2h_record('Prusa David', 'Olah Benedek', self.cursor)
        self.assertEqual(h2h, 'Prusa David and Olah Benedek have played 0 times')

        
    def test_get_seasonal_stats(self):
        season_stats = get_seasonal_stats('Nguyen Long', self.cursor)['2324']
        self.assertEqual(season_stats, [57, 49, 8, '85.96%'])
