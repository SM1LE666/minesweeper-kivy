import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.cell_renderers import DefaultCellRenderer, MinimalistCellRenderer
from interfaces.game_interfaces import CellState


class TestCellRenderers(unittest.TestCase):
    """Unit tests for cell renderers"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.default_renderer = DefaultCellRenderer()
        self.minimalist_renderer = MinimalistCellRenderer()

    def test_default_renderer_hidden_cell(self):
        """Test default renderer for hidden cells"""
        text = self.default_renderer.get_cell_text(CellState.HIDDEN, 0)
        self.assertEqual(text, '')
        
        bg_color = self.default_renderer.get_background_color(CellState.HIDDEN, 0)
        self.assertEqual(bg_color, (0.7, 0.7, 0.7, 1))

    def test_default_renderer_flagged_cell(self):
        """Test default renderer for flagged cells"""
        text = self.default_renderer.get_cell_text(CellState.FLAGGED, 0)
        self.assertEqual(text, '🚩')
        
        bg_color = self.default_renderer.get_background_color(CellState.FLAGGED, 0)
        self.assertEqual(bg_color, (0.9, 0.7, 0.7, 1))

    def test_default_renderer_mine_exploded(self):
        """Test default renderer for exploded mine"""
        text = self.default_renderer.get_cell_text(CellState.MINE_EXPLODED, -1)
        self.assertEqual(text, '💣')
        
        bg_color = self.default_renderer.get_background_color(CellState.MINE_EXPLODED, -1)
        self.assertEqual(bg_color, (1, 0, 0, 1))

    def test_default_renderer_revealed_number(self):
        """Test default renderer for revealed number cells"""
        for i in range(1, 9):
            text = self.default_renderer.get_cell_text(CellState.REVEALED, i)
            self.assertEqual(text, str(i))

    def test_default_renderer_revealed_empty(self):
        """Test default renderer for revealed empty cells"""
        text = self.default_renderer.get_cell_text(CellState.REVEALED, 0)
        self.assertEqual(text, '')

    def test_minimalist_renderer_flagged_cell(self):
        """Test minimalist renderer for flagged cells"""
        text = self.minimalist_renderer.get_cell_text(CellState.FLAGGED, 0)
        self.assertEqual(text, 'F')
        
        bg_color = self.minimalist_renderer.get_background_color(CellState.FLAGGED, 0)
        self.assertEqual(bg_color, (1, 1, 0, 1))

    def test_minimalist_renderer_mine_exploded(self):
        """Test minimalist renderer for exploded mine"""
        text = self.minimalist_renderer.get_cell_text(CellState.MINE_EXPLODED, -1)
        self.assertEqual(text, 'X')

    def test_minimalist_renderer_revealed_mine(self):
        """Test minimalist renderer for revealed mine"""
        text = self.minimalist_renderer.get_cell_text(CellState.REVEALED, -1)
        self.assertEqual(text, 'M')

    def test_minimalist_renderer_text_color(self):
        """Test minimalist renderer always uses black text"""
        for state in CellState:
            color = self.minimalist_renderer.get_text_color(state, 1)
            self.assertEqual(color, (0, 0, 0, 1))


if __name__ == '__main__':
    unittest.main()