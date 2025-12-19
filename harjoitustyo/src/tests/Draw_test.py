import unittest
from draw import Draw
from unittest.mock import MagicMock, patch, mock_open, call

class TestDraw(unittest.TestCase):
    def setUp(self):
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value = self.mock_cursor


    def test_next_pool_size(self):
        with patch('draw.Draw.create_classes'):
            draw = Draw('test.txt', self.mock_conn)
            
            self.assertEqual(draw.next_pool_size(0), 0)
            self.assertEqual(draw.next_pool_size(4), 4)  
            self.assertEqual(draw.next_pool_size(6), 3)  
            self.assertEqual(draw.next_pool_size(10), 5) 
            self.assertEqual(draw.next_pool_size(11), 4) 
            self.assertEqual(draw.next_pool_size(3), 3)


    def test_pool_sizes(self):
        with patch('draw.Draw.create_classes'):
            draw = Draw('test.txt', self.mock_conn)

            self.assertEqual(draw.pool_sizes(11), [4, 4, 3])
            self.assertEqual(draw.pool_sizes(8), [4, 4])


    @patch('draw.script_dir', '/tmp')
    @patch('draw.get_player_classes_from_file')
    @patch('builtins.open', new_callable=mock_open, read_data="ClassA\nClassB")
    def test_create_classes_inserts_correctly(self, mock_file, mock_parser):
        mock_parser.return_value = {
            'Player One': ['ClassA'], 
            'Player Two': ['ClassB, ClassA']
        }
        self.mock_cursor.fetchall.return_value = [1, 2, 3, 4] 
        draw = Draw('entries.txt', self.mock_conn)

        mock_file.assert_called_with('/tmp/possible_classes.txt')
        self.mock_cursor.execute.assert_any_call('CREATE TABLE Entries(class, player)')

        calls = [
            call('INSERT INTO Entries(class, player) values(?, ?)', ('ClassA', 'Player One')),
            call('INSERT INTO Entries(class, player) values(?, ?)', ('ClassB', 'Player Two')),
            call('INSERT INTO Entries(class, player) values(?, ?)', ('ClassA', 'Player Two'))
        ]
        self.mock_cursor.execute.assert_has_calls(calls, any_order=True)


    @patch('draw.Player')
    def test_get_player_found(self, MockPlayer):
        """Test retrieving an existing player from DB"""
        with patch('draw.Draw.create_classes'):
            draw = Draw('f.txt', self.mock_conn)
            self.mock_cursor.fetchone.return_value = [123, 'Pro Player', 'ClubX', 1500, 'ID1']
            result = draw.get_player('Pro Player')
            
            self.mock_cursor.execute.assert_called()
            MockPlayer.assert_called_with(123, 'Pro Player', 'ClubX', 1500, 'ID1')


    @patch('draw.random')
    @patch('draw.Player')
    def test_draw_for_class(self, MockPlayer, mock_random):
        mock_random.choice.side_effect = lambda seq: seq[0]
        with patch('draw.Draw.create_classes'):
            draw = Draw('f.txt', self.mock_conn)
            player_names = [f'Player{i}' for i in range(1, 9)]
            self.mock_cursor.fetchall.return_value = [(0, name) for name in player_names]

            draw.player_rating = MagicMock(side_effect=lambda x: int(x.replace('Player', '')) * 100)

            def fake_get_player(name):
                p = MagicMock()
                p.name = name
                p.rating = int(name.replace('Player', '')) * 100
                p.club = 'Club'
                return p
            draw.get_player = MagicMock(side_effect=fake_get_player)

            result = draw.draw_for_class('ClassA')

            self.assertIn('Pooli A', result)
            self.assertIn('Pooli B', result)

            pool_a_seed = result['Pooli A'][0]['name']
            pool_b_seed = result['Pooli B'][0]['name']
            
            self.assertEqual(pool_a_seed, 'Player8')
            self.assertEqual(pool_b_seed, 'Player7')

            all_in_draw = []
            for pool in result.values():
                for p in pool:
                    all_in_draw.append(p['name'])
            
            self.assertCountEqual(all_in_draw, player_names)