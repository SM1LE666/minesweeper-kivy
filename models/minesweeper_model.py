from typing import List, Set, Tuple
from random import randint
from interfaces.game_interfaces import IGameModel, IGameObserver, CellState, GameState

class MinesweeperModel(IGameModel):
    """Game logic model implementing single responsibility principle"""
    
    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.mine_count = 0
        self.mines: Set[Tuple[int, int]] = set()
        self.revealed: Set[Tuple[int, int]] = set()
        self.flagged: Set[Tuple[int, int]] = set()
        self.game_state = GameState.NOT_STARTED
        self.first_click = True
        self.observers: List[IGameObserver] = []
    
    def add_observer(self, observer: IGameObserver) -> None:
        """Add observer for game events"""
        self.observers.append(observer)
    
    def remove_observer(self, observer: IGameObserver) -> None:
        """Remove observer"""
        if observer in self.observers:
            self.observers.remove(observer)
    
    def _notify_game_state_changed(self) -> None:
        """Notify observers about game state change"""
        for observer in self.observers:
            observer.on_game_state_changed(self.game_state)
    
    def _notify_cell_updated(self, row: int, col: int) -> None:
        """Notify observers about cell update"""
        state = self.get_cell_state(row, col)
        value = self.get_cell_value(row, col)
        for observer in self.observers:
            observer.on_cell_updated(row, col, state, value)
    
    def _notify_status_updated(self) -> None:
        """Notify observers about status update"""
        for observer in self.observers:
            observer.on_status_updated(self.get_flagged_count(), self.mine_count)
    
    def initialize_game(self, rows: int, cols: int, mine_count: int) -> None:
        """Initialize new game with given parameters"""
        self.rows = rows
        self.cols = cols
        self.mine_count = mine_count
        self.mines.clear()
        self.revealed.clear()
        self.flagged.clear()
        self.game_state = GameState.NOT_STARTED
        self.first_click = True
        self._notify_game_state_changed()
        self._notify_status_updated()
    
    def _place_mines(self, first_row: int, first_col: int) -> None:
        """Place mines avoiding the first clicked cell and its neighbors"""
        self.mines.clear()
        mines_placed = 0
        
        while mines_placed < self.mine_count:
            row = randint(0, self.rows - 1)
            col = randint(0, self.cols - 1)
            
            # Skip the first clicked cell and its neighbors
            if abs(row - first_row) <= 1 and abs(col - first_col) <= 1:
                continue
                
            if (row, col) not in self.mines:
                self.mines.add((row, col))
                mines_placed += 1
    
    def _count_adjacent_mines(self, row: int, col: int) -> int:
        """Count mines adjacent to the given cell"""
        count = 0
        for r in range(max(0, row-1), min(self.rows, row+2)):
            for c in range(max(0, col-1), min(self.cols, col+2)):
                if (r, c) in self.mines:
                    count += 1
        return count
    
    def _is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within game bounds"""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def _reveal_cell_recursive(self, row: int, col: int) -> None:
        """Recursively reveal cells when empty cell is clicked"""
        if not self._is_valid_position(row, col) or (row, col) in self.revealed or (row, col) in self.mines:
            return
            
        self.revealed.add((row, col))
        self._notify_cell_updated(row, col)
        
        # If no adjacent mines, reveal neighboring cells
        if self._count_adjacent_mines(row, col) == 0:
            for r in range(max(0, row-1), min(self.rows, row+2)):
                for c in range(max(0, col-1), min(self.cols, col+2)):
                    if (r, c) != (row, col):
                        self._reveal_cell_recursive(r, c)
    
    def _check_win_condition(self) -> bool:
        """Check if player has won the game"""
        return len(self.revealed) == (self.rows * self.cols - len(self.mines))
    
    def reveal_cell(self, row: int, col: int) -> bool:
        """Reveal cell at given position"""
        if (not self._is_valid_position(row, col) or 
            self.game_state in [GameState.WON, GameState.LOST] or
            (row, col) in self.revealed or 
            (row, col) in self.flagged):
            return False
        
        # Place mines on first click
        if self.first_click:
            self._place_mines(row, col)
            self.first_click = False
            self.game_state = GameState.IN_PROGRESS
            self._notify_game_state_changed()
        
        # Check if mine
        if (row, col) in self.mines:
            self.game_state = GameState.LOST
            self.revealed.add((row, col))
            self._notify_cell_updated(row, col)
            self._notify_game_state_changed()
            return True
        
        # Reveal cell and potentially neighbors
        self._reveal_cell_recursive(row, col)
        
        # Check for win condition
        if self._check_win_condition():
            self.game_state = GameState.WON
            self._notify_game_state_changed()
        
        return True
    
    def toggle_flag(self, row: int, col: int) -> bool:
        """Toggle flag on cell"""
        if (not self._is_valid_position(row, col) or 
            self.game_state in [GameState.WON, GameState.LOST] or
            (row, col) in self.revealed):
            return False
        
        if (row, col) in self.flagged:
            self.flagged.remove((row, col))
        else:
            self.flagged.add((row, col))
        
        self._notify_cell_updated(row, col)
        self._notify_status_updated()
        return True
    
    def get_cell_state(self, row: int, col: int) -> CellState:
        """Get current state of cell"""
        if not self._is_valid_position(row, col):
            return CellState.HIDDEN
        
        if (row, col) in self.flagged:
            return CellState.FLAGGED
        elif (row, col) in self.revealed:
            if (row, col) in self.mines and self.game_state == GameState.LOST:
                return CellState.MINE_EXPLODED
            return CellState.REVEALED
        else:
            return CellState.HIDDEN
    
    def get_cell_value(self, row: int, col: int) -> int:
        """Get cell value (mine count or -1 for mine)"""
        if not self._is_valid_position(row, col):
            return 0
        
        if (row, col) in self.mines:
            return -1
        else:
            return self._count_adjacent_mines(row, col)
    
    def get_game_state(self) -> GameState:
        """Get current game state"""
        return self.game_state
    
    def get_flagged_count(self) -> int:
        """Get number of flagged cells"""
        return len(self.flagged)
    
    def get_mine_count(self) -> int:
        """Get total number of mines"""
        return self.mine_count
    
    def get_all_mines(self) -> Set[Tuple[int, int]]:
        """Get all mine positions (for game over display)"""
        return self.mines.copy()