from abc import ABC, abstractmethod
from typing import List, Tuple, Set, Callable
from enum import Enum

class CellState(Enum):
    HIDDEN = "hidden"
    REVEALED = "revealed"
    FLAGGED = "flagged"
    MINE_EXPLODED = "mine_exploded"

class GameState(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"

class IGameModel(ABC):
    """Interface for game logic model"""
    
    @abstractmethod
    def initialize_game(self, rows: int, cols: int, mine_count: int) -> None:
        """Initialize new game with given parameters"""
        pass
    
    @abstractmethod
    def reveal_cell(self, row: int, col: int) -> bool:
        """Reveal cell at given position. Returns True if successful"""
        pass
    
    @abstractmethod
    def toggle_flag(self, row: int, col: int) -> bool:
        """Toggle flag on cell. Returns True if successful"""
        pass
    
    @abstractmethod
    def get_cell_state(self, row: int, col: int) -> CellState:
        """Get current state of cell"""
        pass
    
    @abstractmethod
    def get_cell_value(self, row: int, col: int) -> int:
        """Get cell value (mine count or -1 for mine)"""
        pass
    
    @abstractmethod
    def get_game_state(self) -> GameState:
        """Get current game state"""
        pass
    
    @abstractmethod
    def get_flagged_count(self) -> int:
        """Get number of flagged cells"""
        pass
    
    @abstractmethod
    def get_mine_count(self) -> int:
        """Get total number of mines"""
        pass

class IGameView(ABC):
    """Interface for game view"""
    
    @abstractmethod
    def update_cell(self, row: int, col: int, state: CellState, value: int) -> None:
        """Update visual representation of a cell"""
        pass
    
    @abstractmethod
    def update_status(self, flagged_count: int, mine_count: int) -> None:
        """Update status display"""
        pass
    
    @abstractmethod
    def show_game_over(self, won: bool) -> None:
        """Show game over dialog"""
        pass
    
    @abstractmethod
    def reset_view(self) -> None:
        """Reset view to initial state"""
        pass

class IGameController(ABC):
    """Interface for game controller"""
    
    @abstractmethod
    def on_cell_left_click(self, row: int, col: int) -> None:
        """Handle left click on cell"""
        pass
    
    @abstractmethod
    def on_cell_right_click(self, row: int, col: int) -> None:
        """Handle right click on cell"""
        pass
    
    @abstractmethod
    def on_reset_game(self) -> None:
        """Handle game reset"""
        pass

class IGameObserver(ABC):
    """Observer interface for game events"""
    
    @abstractmethod
    def on_game_state_changed(self, new_state: GameState) -> None:
        """Called when game state changes"""
        pass
    
    @abstractmethod
    def on_cell_updated(self, row: int, col: int, state: CellState, value: int) -> None:
        """Called when cell is updated"""
        pass
    
    @abstractmethod
    def on_status_updated(self, flagged_count: int, mine_count: int) -> None:
        """Called when status should be updated"""
        pass