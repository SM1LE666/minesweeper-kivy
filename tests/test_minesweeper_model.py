import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.minesweeper_model import MinesweeperModel
from interfaces.game_interfaces import GameState, CellState


class TestMinesweeperModel(unittest.TestCase):
    """Unit tests for MinesweeperModel"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.model = MinesweeperModel()

    def test_initialize_game(self):
        """Test game initialization"""
        self.model.initialize_game(10, 10, 10)
        
        self.assertEqual(self.model.rows, 10)
        self.assertEqual(self.model.cols, 10)
        self.assertEqual(self.model.mine_count, 10)
        self.assertEqual(self.model.get_game_state(), GameState.NOT_STARTED)
        self.assertEqual(self.model.get_flagged_count(), 0)
        self.assertTrue(self.model.first_click)

    def test_cell_state_initial(self):
        """Test initial cell states"""
        self.model.initialize_game(5, 5, 5)
        
        # All cells should be hidden initially
        for row in range(5):
            for col in range(5):
                self.assertEqual(self.model.get_cell_state(row, col), CellState.HIDDEN)

    def test_toggle_flag(self):
        """Test flag toggling functionality"""
        self.model.initialize_game(5, 5, 5)
        
        # Flag a cell
        result = self.model.toggle_flag(2, 2)
        self.assertTrue(result)
        self.assertEqual(self.model.get_cell_state(2, 2), CellState.FLAGGED)
        self.assertEqual(self.model.get_flagged_count(), 1)
        
        # Unflag the cell
        result = self.model.toggle_flag(2, 2)
        self.assertTrue(result)
        self.assertEqual(self.model.get_cell_state(2, 2), CellState.HIDDEN)
        self.assertEqual(self.model.get_flagged_count(), 0)

    def test_invalid_position(self):
        """Test handling of invalid positions"""
        self.model.initialize_game(5, 5, 5)
        
        # Test out of bounds positions
        self.assertEqual(self.model.get_cell_state(-1, 0), CellState.HIDDEN)
        self.assertEqual(self.model.get_cell_state(0, -1), CellState.HIDDEN)
        self.assertEqual(self.model.get_cell_state(5, 0), CellState.HIDDEN)
        self.assertEqual(self.model.get_cell_state(0, 5), CellState.HIDDEN)
        
        # Operations on invalid positions should return False
        self.assertFalse(self.model.toggle_flag(-1, 0))
        self.assertFalse(self.model.reveal_cell(-1, 0))

    def test_reveal_cell_first_click(self):
        """Test that first click starts the game and places mines"""
        self.model.initialize_game(5, 5, 3)
        
        # First click should start the game
        result = self.model.reveal_cell(2, 2)
        self.assertTrue(result)
        self.assertEqual(self.model.get_game_state(), GameState.IN_PROGRESS)
        self.assertFalse(self.model.first_click)
        
        # Should have placed exactly 3 mines
        self.assertEqual(len(self.model.mines), 3)
        
        # First clicked cell should not be a mine
        self.assertNotIn((2, 2), self.model.mines)

    def test_cannot_flag_revealed_cell(self):
        """Test that revealed cells cannot be flagged"""
        self.model.initialize_game(5, 5, 1)
        
        # Reveal a cell first
        self.model.reveal_cell(0, 0)
        
        # Try to flag the revealed cell - should fail
        result = self.model.toggle_flag(0, 0)
        self.assertFalse(result)

    def test_cannot_reveal_flagged_cell(self):
        """Test that flagged cells cannot be revealed"""
        self.model.initialize_game(5, 5, 1)
        
        # Flag a cell first
        self.model.toggle_flag(1, 1)
        
        # Try to reveal the flagged cell - should fail
        result = self.model.reveal_cell(1, 1)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()