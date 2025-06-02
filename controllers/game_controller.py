from interfaces.game_interfaces import IGameController, IGameModel, IGameView, IGameObserver, GameState, CellState
from typing import Optional

class MinesweeperController(IGameController, IGameObserver):
    """Game controller implementing separation of concerns"""
    
    def __init__(self, model: IGameModel, view: IGameView):
        self.model = model
        self.view = view
        self.model.add_observer(self)
    
    def initialize_game(self, rows: int = 15, cols: int = 15, mine_count: int = 30) -> None:
        """Initialize new game with default or custom parameters"""
        self.model.initialize_game(rows, cols, mine_count)
        self.view.reset_view()
    
    def on_cell_left_click(self, row: int, col: int) -> None:
        """Handle left click on cell - reveal cell"""
        self.model.reveal_cell(row, col)
    
    def on_cell_right_click(self, row: int, col: int) -> None:
        """Handle right click on cell - toggle flag"""
        self.model.toggle_flag(row, col)
    
    def on_reset_game(self) -> None:
        """Handle game reset"""
        # Get current game parameters to restart with same settings
        rows = self.model.rows if hasattr(self.model, 'rows') else 15
        cols = self.model.cols if hasattr(self.model, 'cols') else 15
        mine_count = self.model.get_mine_count()
        
        self.initialize_game(rows, cols, mine_count)
    
    # Observer methods - respond to model changes
    def on_game_state_changed(self, new_state: GameState) -> None:
        """Called when game state changes"""
        if new_state == GameState.WON:
            self.view.show_game_over(True)
            self._reveal_all_mines_for_display()
        elif new_state == GameState.LOST:
            self.view.show_game_over(False)
            self._reveal_all_mines_for_display()
    
    def on_cell_updated(self, row: int, col: int, state: CellState, value: int) -> None:
        """Called when cell is updated"""
        self.view.update_cell(row, col, state, value)
    
    def on_status_updated(self, flagged_count: int, mine_count: int) -> None:
        """Called when status should be updated"""
        self.view.update_status(flagged_count, mine_count)
    
    def _reveal_all_mines_for_display(self) -> None:
        """Reveal all mines when game ends"""
        if hasattr(self.model, 'get_all_mines'):
            mines = self.model.get_all_mines()
            for row, col in mines:
                state = self.model.get_cell_state(row, col)
                value = self.model.get_cell_value(row, col)
                self.view.update_cell(row, col, state, value)