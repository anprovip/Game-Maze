import pygame
import sys
from ui.screen import Screen
from ui.button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, GRAY

class MenuScreen(Screen):
    """
    Màn hình menu chính của game.
    """
    
    def __init__(self, manager):
        """
        Khởi tạo màn hình menu.
        
        Args:
            manager: Game Manager quản lý các trạng thái
        """
        super().__init__(manager)
        
        # Khởi tạo các nút
        button_width = 200
        button_height = 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        
        # Nút chơi 1 người
        self.single_player_button = Button(
            button_x, 200, button_width, button_height, 
            "1 Player Mode", (100, 200, 100), (150, 255, 150)
        )
        
        # Nút chơi 2 người
        self.two_players_button = Button(
            button_x, 270, button_width, button_height, 
            "2 Players Mode", (100, 100, 200), (150, 150, 255)
        )
        
        # Nút chơi với máy
        self.vs_ai_button = Button(
            button_x, 340, button_width, button_height, 
            "Play vs AI", (200, 100, 100), (255, 150, 150)
        )
        
        # Nút thoát
        self.exit_button = Button(
            button_x, 410, button_width, button_height, 
            "Exit", (150, 150, 150), (200, 200, 200)
        )
        
        # Font cho tiêu đề
        self.title_font = pygame.font.SysFont(None, 64)
    
    def enter(self):
        """
        Được gọi khi màn hình bắt đầu hiển thị.
        """
        pass
    
    def exit(self):
        """
        Được gọi khi thoát khỏi màn hình.
        """
        pass
    
    def update(self, events):
        """
        Cập nhật màn hình menu dựa trên sự kiện đầu vào.
        
        Args:
            events: Danh sách các sự kiện pygame
        """
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        # Kiểm tra sự kiện chuột
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
        
        # Kiểm tra hover
        self.single_player_button.check_hover(mouse_pos)
        self.two_players_button.check_hover(mouse_pos)
        self.vs_ai_button.check_hover(mouse_pos)
        self.exit_button.check_hover(mouse_pos)
        
        # Kiểm tra click
        if self.single_player_button.is_clicked(mouse_pos, mouse_clicked):
            self.manager.game_mode = "single"
            self.manager.change_state("game")
        
        if self.two_players_button.is_clicked(mouse_pos, mouse_clicked):
            self.manager.game_mode = "two_players"
            self.manager.change_state("game")
        
        if self.vs_ai_button.is_clicked(mouse_pos, mouse_clicked):
            self.manager.game_mode = "vs_ai"
            self.manager.change_state("game")
        
        if self.exit_button.is_clicked(mouse_pos, mouse_clicked):
            pygame.quit()
            sys.exit()
    
    def draw(self):
        """
        Vẽ màn hình menu.
        """
        # Xóa màn hình
        self.screen.fill((50, 50, 80))
        
        # Vẽ tiêu đề
        title_surface = self.title_font.render("MAZE GAME", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_surface, title_rect)
        
        # Vẽ các nút
        self.single_player_button.draw(self.screen)
        self.two_players_button.draw(self.screen)
        self.vs_ai_button.draw(self.screen)
        self.exit_button.draw(self.screen)
        
        # Vẽ thông tin phụ
        info_font = pygame.font.SysFont(None, 24)
        info_surface = info_font.render("Use arrow keys to navigate the maze", True, WHITE)
        info_rect = info_surface.get_rect(center=(SCREEN_WIDTH // 2, 500))
        self.screen.blit(info_surface, info_rect)