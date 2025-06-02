from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
from interfaces.game_interfaces import IGameView, IGameController, CellState
from utils.cell_renderers import ICellRenderer, DefaultCellRenderer
from typing import Dict, Tuple, Optional

# Register emoji font
LabelBase.register(name="DejaVuSans", 
                   fn_regular="C:/Windows/Fonts/seguiemj.ttf")

class MinesweeperCell(Button):
    """Custom button for minesweeper cell with clean separation of concerns"""
    
    def __init__(self, row: int, col: int, controller: IGameController, **kwargs):
        super(MinesweeperCell, self).__init__(**kwargs)
        self.row = row
        self.col = col
        self.controller = controller
        self.font_name = "DejaVuSans"
        self.font_size = '20sp'
        self.text = ''
        self.background_normal = ''
        self.background_color = (0.7, 0.7, 0.7, 1)
    
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super(MinesweeperCell, self).on_touch_down(touch)
        
        if touch.button == 'right':
            self.controller.on_cell_right_click(self.row, self.col)
        
        return True
    
    def on_touch_up(self, touch):
        if touch.button == 'left' and self.collide_point(*touch.pos):
            self.controller.on_cell_left_click(self.row, self.col)
        
        return super(MinesweeperCell, self).on_touch_up(touch)

class MinesweeperViewImpl(IGameView):
    """Implementation of IGameView interface using composition pattern"""
    
    def __init__(self, widget: BoxLayout, controller: IGameController, rows: int = 15, cols: int = 15, 
                 cell_renderer: Optional[ICellRenderer] = None):
        self.widget = widget
        self.controller = controller
        self.rows = rows
        self.cols = cols
        self.cell_renderer = cell_renderer or DefaultCellRenderer()
        
        # UI components
        self.cells: Dict[Tuple[int, int], MinesweeperCell] = {}
        self.status_label: Optional[Label] = None
        self.grid: Optional[GridLayout] = None
        self.reset_button: Optional[Button] = None
        self._reset_callback = None  # Store callback reference for unbinding
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the user interface"""
        # Status label
        self.status_label = Label(
            text="Mines: 0/0", 
            size_hint=(1, 0.1),
            font_size='16sp'
        )
        self.widget.add_widget(self.status_label)
        
        # Game grid
        self.grid = GridLayout(
            cols=self.cols, 
            spacing=2, 
            padding=10
        )
        
        # Create cell buttons
        for row in range(self.rows):
            for col in range(self.cols):
                cell = MinesweeperCell(
                    row=row,
                    col=col,
                    controller=self.controller
                )
                self.cells[(row, col)] = cell
                self.grid.add_widget(cell)
        
        self.widget.add_widget(self.grid)
        
        # Reset button
        self.reset_button = Button(
            text="Перезапустить игру", 
            size_hint=(1, 0.1),
            font_size='16sp'
        )
        self._reset_callback = lambda x: self.controller.on_reset_game()
        self.reset_button.bind(on_release=self._reset_callback)
        self.widget.add_widget(self.reset_button)
    
    def set_controller(self, controller: IGameController) -> None:
        """Update controller reference for all UI elements"""
        self.controller = controller
        
        # Update reset button binding
        if self.reset_button and self._reset_callback:
            # Unbind old callback and bind new one
            self.reset_button.unbind(on_release=self._reset_callback)
            self._reset_callback = lambda x: self.controller.on_reset_game()
            self.reset_button.bind(on_release=self._reset_callback)
        
        # Update all cells with new controller
        for cell in self.cells.values():
            cell.controller = controller
    
    def update_cell(self, row: int, col: int, state: CellState, value: int) -> None:
        """Update visual representation of a cell"""
        if (row, col) not in self.cells:
            return
        
        cell = self.cells[(row, col)]
        
        # Use renderer strategy to get visual properties
        cell.text = self.cell_renderer.get_cell_text(state, value)
        cell.background_color = self.cell_renderer.get_background_color(state, value)
        cell.color = self.cell_renderer.get_text_color(state, value)
    
    def update_status(self, flagged_count: int, mine_count: int) -> None:
        """Update status display"""
        if self.status_label:
            self.status_label.text = f"Mines: {flagged_count}/{mine_count}"
    
    def show_game_over(self, won: bool) -> None:
        """Show game over dialog"""
        title = "Победа!" if won else "Игра окончена"
        message = "Поздравляю, ты нашёл все мины!" if won else "Упс, ты напоролся на мину!"
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        message_label = Label(
            text=message,
            text_size=(300, None),
            halign='center',
            valign='middle'
        )
        content.add_widget(message_label)
        
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.3), spacing=10)
        
        new_game_btn = Button(text="Новая игра")
        new_game_btn.bind(on_release=lambda x: (popup.dismiss(), self.controller.on_reset_game()))
        button_layout.add_widget(new_game_btn)
        
        content.add_widget(button_layout)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.6, 0.4),
            auto_dismiss=False
        )
        popup.open()
    
    def reset_view(self) -> None:
        """Reset view to initial state"""
        for cell in self.cells.values():
            cell.text = ''
            cell.background_color = (0.7, 0.7, 0.7, 1)
            cell.color = (1, 1, 1, 1)
        
        if self.status_label:
            self.status_label.text = "Mines: 0/0"
    
    def set_cell_renderer(self, renderer: ICellRenderer) -> None:
        """Change cell rendering strategy (Open/Closed Principle)"""
        self.cell_renderer = renderer

class MinesweeperView(BoxLayout):
    """Kivy widget that wraps the view implementation"""
    
    def __init__(self, controller: IGameController, rows: int = 15, cols: int = 15, 
                 cell_renderer: Optional[ICellRenderer] = None, **kwargs):
        super(MinesweeperView, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Create the view implementation using composition
        self.view_impl = MinesweeperViewImpl(
            widget=self,
            controller=controller,
            rows=rows,
            cols=cols,
            cell_renderer=cell_renderer
        )
    
    def get_view_interface(self) -> IGameView:
        """Get the IGameView interface implementation"""
        return self.view_impl