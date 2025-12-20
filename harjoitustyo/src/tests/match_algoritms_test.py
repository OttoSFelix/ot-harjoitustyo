import unittest
from match_algoritms import total_score, reverse_score

class TestAlgoritms(unittest.TestCase):
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