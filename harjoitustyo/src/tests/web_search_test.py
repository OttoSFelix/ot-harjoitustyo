import unittest
import os
import requests
from database_connection import get_database_connection
from web_search import get_player_matches, get_rating, top_date
from db_search import get_player_base_stats
from playerinfo import Player

class TestWebSearch(unittest.TestCase):
    def setUp(self):
        self.connection = get_database_connection()
        self.cursor = self.connection.cursor()
        self.session = requests.Session()
    
    def test_top_date(self):
        date = top_date()
        self.assertEqual(date, '14.12.2025')

    def test_get_newest_rating(self):
        get_rating(connection=self.connection)
        rows = []
        with open('ratinglist', 'r') as f:
                    for i in range(5):
                        rows.append(f.readline().strip())
        print(rows)
        self.assertEqual(rows[1], 'Rating-julkaisu 14.12.2025')
        if os.path.exists("ratinglist"):
            os.remove("ratinglist")


    def test_get_player_matches(self):
        self.cursor.execute("DELETE FROM All_matches WHERE player_name == 'Pihkala Arttu'")
        player = Player(1, 'Pihkala Arttu', 'PihkaArtt', 'PT Espoo', '2419')
        get_player_matches(player, self.connection, self.session)
        stats = get_player_base_stats('Pihkala Arttu', self.cursor)
        self.assertEqual(stats, """11 Pihkala Arttu PT Espoo 2419
    all time wins: 411
    all time losses: 197
    All time win rate: 67.6% """)