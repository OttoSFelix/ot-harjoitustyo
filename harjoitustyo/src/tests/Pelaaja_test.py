import unittest
from playerinfo import Player

class TestPelaaja(unittest.TestCase):
    def setUp(self):
        self.player = Player(405, 'Testinen Testi', 'TestiTest', 'PT Testi', 2350)

    def test_correct_rank(self):
        self.assertEqual(self.player.rank, 405)

    def test_correct_name(self):
        self.assertEqual(self.player.name, 'Testinen Testi')
    
    def test_correct_id(self):
        self.assertEqual(self.player.id, 'TestiTest')
    
    def test_correct_club(self):
        self.assertEqual(self.player.club, 'PT Testi')

    def test_correct_rating(self):
        self.assertEqual(self.player.rating, 2350)

    def test_correct_str(self):
        info = str(self.player)
        self.assertEqual(info, (f'405 Testinen Testi PT Testi 2350'))
        