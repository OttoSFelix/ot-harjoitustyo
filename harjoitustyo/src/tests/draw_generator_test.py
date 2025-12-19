import unittest
from draw_generator import get_match_schedule, format_cell
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
from unittest.mock import MagicMock

class TestDrawGenerator(unittest.TestCase):
    def test_get_match_schedule_for_3(self):
        schedule = get_match_schedule(3)
        self.assertEqual(schedule, [(1, 3, 2), (1, 2, 3), (2, 3, 1)])

    def test_get_match_schedule_for_4(self):
        schedule = get_match_schedule(4)
        self.assertEqual(schedule, [
            (1, 3, 4), (2, 4, 3), (1, 2, 4), 
            (3, 4, 2), (1, 4, 3), (2, 3, 1)
        ])
    
    def test_get_match_schedule_for_5(self):
        schedule = get_match_schedule(5)
        self.assertEqual(schedule, [
            (1, 5, 4), (2, 3, 3), (3, 5, 2), (1, 4, 3), (2, 5, 1), 
            (1, 3, 2), (3, 4, 5), (1, 2, 4), (4, 5, 1), (2, 3, 5)
        ])

    def test_format_cell(self):
        mock_ws = MagicMock()
        mock_cell = MagicMock()
        mock_ws.cell.return_value = mock_cell
        fake_font = "FontObj"
        fake_align = "AlignObj"
        fake_border = "BorderObj"

        result = format_cell(
            ws=mock_ws,
            row=5,
            col=3,
            value="Test",
            font=fake_font,
            alignment=fake_align,
            border=fake_border
        )

        mock_ws.cell.assert_called_once_with(row=5, column=3, value="Test")
        self.assertEqual(mock_cell.font, fake_font)
        self.assertEqual(mock_cell.alignment, fake_align)
        self.assertEqual(mock_cell.border, fake_border)
        self.assertEqual(result, mock_cell)

