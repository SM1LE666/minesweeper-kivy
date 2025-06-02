# -*- coding: utf-8 -*-
"""
Refactored Minesweeper following SOLID principles
"""
import sys
import os

# Add current directory to Python path for module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.core.window import Window

# Import our SOLID-compliant components
from models.minesweeper_model import MinesweeperModel
from views.game_view import MinesweeperView
from controllers.game_controller import MinesweeperController
from utils.cell_renderers import DefaultCellRenderer, MinimalistCellRenderer

class MinesweeperApp(App):
    """Main application class following dependency injection principles"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kv_file = None  # Disable KV file loading
        
        # Game configuration
        self.rows = 15
        self.cols = 15
        self.mine_count = 30
        
        # Components (will be injected)
        self.model = None
        self.view = None
        self.controller = None
    
    def build(self):
        """Build the application using dependency injection"""
        Window.size = (600, 700)
        
        # Create model (business logic)
        self.model = MinesweeperModel()
        
        # Create view with renderer strategy
        cell_renderer = DefaultCellRenderer()  # Could be MinimalistCellRenderer()
        
        # Create temporary controller for view initialization
        temp_controller = type('TempController', (), {
            'on_cell_left_click': lambda self, r, c: None,
            'on_cell_right_click': lambda self, r, c: None,
            'on_reset_game': lambda self: None
        })()
        
        self.view = MinesweeperView(
            controller=temp_controller,
            rows=self.rows,
            cols=self.cols,
            cell_renderer=cell_renderer
        )
        
        # Create real controller and inject dependencies
        self.controller = MinesweeperController(self.model, self.view.get_view_interface())
        
        # Update view with real controller using the new method
        self.view.view_impl.set_controller(self.controller)
        
        # Initialize game
        self.controller.initialize_game(self.rows, self.cols, self.mine_count)
        
        return self.view
    
    def on_start(self):
        """Called when application starts"""
        self.title = "SOLID Minesweeper"

# Factory function for easy testing and configuration
def create_minesweeper_app(rows: int = 15, cols: int = 15, mine_count: int = 30, 
                          use_minimalist_renderer: bool = False) -> MinesweeperApp:
    """
    Factory function to create configured minesweeper app
    Demonstrates Open/Closed Principle - easy to extend without modifying existing code
    """
    app = MinesweeperApp()
    app.rows = rows
    app.cols = cols
    app.mine_count = mine_count
    
    if use_minimalist_renderer:
        # This could be extended to support more renderer types
        pass
    
    return app

if __name__ == '__main__':
    # Use factory function for better configurability
    app = create_minesweeper_app(
        rows=15, 
        cols=15, 
        mine_count=30,
        use_minimalist_renderer=False  # Change to True for alternative style
    )
    app.run()