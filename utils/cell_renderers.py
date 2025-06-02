from abc import ABC, abstractmethod
from typing import Tuple
from interfaces.game_interfaces import CellState

class ICellRenderer(ABC):
    """Interface for cell rendering strategies"""
    
    @abstractmethod
    def get_cell_text(self, state: CellState, value: int) -> str:
        """Get text to display in cell"""
        pass
    
    @abstractmethod
    def get_background_color(self, state: CellState, value: int) -> Tuple[float, float, float, float]:
        """Get background color for cell"""
        pass
    
    @abstractmethod
    def get_text_color(self, state: CellState, value: int) -> Tuple[float, float, float, float]:
        """Get text color for cell"""
        pass

class DefaultCellRenderer(ICellRenderer):
    """Default cell renderer with emoji support"""
    
    def __init__(self):
        # Color coding for mine count numbers
        self.number_colors = [
            (0, 0, 1, 1),      # 1 - blue
            (0, 0.5, 0, 1),    # 2 - green
            (1, 0, 0, 1),      # 3 - red
            (0, 0, 0.5, 1),    # 4 - dark blue
            (0.5, 0, 0, 1),    # 5 - dark red
            (0, 0.5, 0.5, 1),  # 6 - teal
            (0, 0, 0, 1),      # 7 - black
            (0.5, 0.5, 0.5, 1) # 8 - gray
        ]
    
    def get_cell_text(self, state: CellState, value: int) -> str:
        """Get text to display in cell"""
        if state == CellState.FLAGGED:
            return '🚩'
        elif state == CellState.MINE_EXPLODED:
            return '💣'
        elif state == CellState.REVEALED:
            if value == -1:  # Mine
                return '💣'
            elif value == 0:  # Empty cell
                return ''
            else:  # Number
                return str(value)
        else:  # HIDDEN
            return ''
    
    def get_background_color(self, state: CellState, value: int) -> Tuple[float, float, float, float]:
        """Get background color for cell"""
        if state == CellState.FLAGGED:
            return (0.9, 0.7, 0.7, 1)  # Light red for flagged
        elif state == CellState.MINE_EXPLODED:
            return (1, 0, 0, 1)  # Red for exploded mine
        elif state == CellState.REVEALED:
            return (0.9, 0.9, 0.9, 1)  # Light gray for revealed
        else:  # HIDDEN
            return (0.7, 0.7, 0.7, 1)  # Gray for hidden
    
    def get_text_color(self, state: CellState, value: int) -> Tuple[float, float, float, float]:
        """Get text color for cell"""
        if state == CellState.FLAGGED:
            return (1, 0, 0, 1)  # Red for flag
        elif state == CellState.MINE_EXPLODED:
            return (1, 1, 1, 1)  # White for contrast
        elif state == CellState.REVEALED and value > 0 and value <= len(self.number_colors):
            return self.number_colors[value - 1]
        else:
            return (1, 1, 1, 1)  # White default

class MinimalistCellRenderer(ICellRenderer):
    """Alternative minimalist renderer without emoji"""
    
    def get_cell_text(self, state: CellState, value: int) -> str:
        """Get text to display in cell"""
        if state == CellState.FLAGGED:
            return 'F'
        elif state == CellState.MINE_EXPLODED:
            return 'X'
        elif state == CellState.REVEALED:
            if value == -1:  # Mine
                return 'M'
            elif value == 0:  # Empty cell
                return ''
            else:  # Number
                return str(value)
        else:  # HIDDEN
            return ''
    
    def get_background_color(self, state: CellState, value: int) -> Tuple[float, float, float, float]:
        """Get background color for cell"""
        if state == CellState.FLAGGED:
            return (1, 1, 0, 1)  # Yellow for flagged
        elif state == CellState.MINE_EXPLODED:
            return (1, 0, 0, 1)  # Red for exploded mine
        elif state == CellState.REVEALED:
            return (1, 1, 1, 1)  # White for revealed
        else:  # HIDDEN
            return (0.8, 0.8, 0.8, 1)  # Light gray for hidden
    
    def get_text_color(self, state: CellState, value: int) -> Tuple[float, float, float, float]:
        """Get text color for cell"""
        return (0, 0, 0, 1)  # Black text for all states