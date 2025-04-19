import pygame
from ui.menu_screen import MenuScreen
from ui.game_screen import GameScreen
from ui.pause_screen import PauseScreen

class GameManager:
    """
    Quản lý trạng thái game và chuyển đổi giữa các màn hình.
    """
    
    def __init__(self, screen):
        """
        Khởi tạo Game Manager.
        
        Args:
            screen: Bề mặt pygame để vẽ
        """
        self.screen = screen
        
        # Khởi tạo các trạng thái game
        self.states = {
            "menu": MenuScreen(self),
            "game": GameScreen(self),
            "pause": PauseScreen(self)
        }
        
        # Trạng thái hiện tại
        self.current_state = None
        
        # Cài đặt game
        self.game_mode = "single"  # single, two_players, vs_ai
        self.ai_difficulty = "easy"  # easy, medium, hard
        self.level = 1
        self.maze_generator_type = "prim"  # dfs, kruskal, prim
        
        # Chuyển đến màn hình menu
        self.change_state("menu")
    
    def change_state(self, state_name):
        """
        Chuyển đổi trạng thái game.
        
        Args:
            state_name (str): Tên trạng thái mới
        """
        # Thoát khỏi trạng thái hiện tại nếu có
        if self.current_state is not None:
            self.current_state.exit()
        
        # Chuyển sang trạng thái mới
        if state_name in self.states:
            self.current_state = self.states[state_name]
            self.current_state.enter()
    
    def update(self, events):
        """
        Cập nhật trạng thái hiện tại.
        
        Args:
            events: Danh sách các sự kiện pygame
        """
        if self.current_state:
            self.current_state.update(events)
    
    def draw(self):
        """
        Vẽ trạng thái hiện tại lên màn hình.
        """
        if self.current_state:
            self.current_state.draw()