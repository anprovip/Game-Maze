import pygame
import sys
from ui.screen import Screen
from ui.button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE

class PauseScreen(Screen):
    """
    Màn hình tạm dừng game.
    """
    
    def __init__(self, manager):
        """
        Khởi tạo màn hình tạm dừng.
        
        Args:
            manager: Game Manager quản lý các trạng thái
        """
        super().__init__(manager)
        
        # Khởi tạo các nút
        button_width = 200
        button_height = 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        
        # Nút tiếp tục
        self.resume_button = Button(
            button_x, 200, button_width, button_height, 
            "Resume", (100, 200, 100), (150, 255, 150)
        )
        
        # Nút trở về menu
        self.menu_button = Button(
            button_x, 270, button_width, button_height, 
            "Main Menu", (200, 100, 100), (255, 150, 150)
        )
        
        # Nút thoát game
        self.exit_button = Button(
            button_x, 340, button_width, button_height, 
            "Exit Game", (150, 150, 150), (200, 200, 200)
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
        Cập nhật màn hình tạm dừng dựa trên sự kiện đầu vào.
        
        Args:
            events: Danh sách các sự kiện pygame
        """
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        # Kiểm tra sự kiện chuột
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Nhấn Esc để tiếp tục game
                    self.manager.change_state("game")
        
        # Kiểm tra hover
        self.resume_button.check_hover(mouse_pos)
        self.menu_button.check_hover(mouse_pos)
        self.exit_button.check_hover(mouse_pos)
        
        # Kiểm tra click
        if self.resume_button.is_clicked(mouse_pos, mouse_clicked):
            self.manager.change_state("game")
        
        if self.menu_button.is_clicked(mouse_pos, mouse_clicked):
            self.manager.change_state("menu")
        
        if self.exit_button.is_clicked(mouse_pos, mouse_clicked):
            pygame.quit()
            sys.exit()