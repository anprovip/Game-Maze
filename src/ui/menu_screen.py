import os
import pygame
import sys
from ui.screen import Screen
from ui.button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, GRAY

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

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
        # Nút hướng dẫn
        self.tutorial_button = Button(
            button_x, 410, button_width, button_height,
            "Tutorials & Rules", (120,120,200), (170,170,255)
        )
        
        # Nút thoát
        self.exit_button = Button(
            button_x, 480, button_width, button_height, 
            "Exit", (150, 150, 150), (200, 200, 200)
        )
        
        # Font cho tiêu đề
        self.title_font = pygame.font.SysFont(None, 64)

        # Tải hình nền
        background_path = os.path.join(project_root, 'assets', 'img', 'bg-menu.jpg')
        self.background_image = pygame.image.load(background_path)
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Load volume toggle icons
        self.volume_img = pygame.transform.scale(
            pygame.image.load(os.path.join(project_root, 'assets', 'img', 'volume.png')),
            (40, 40)
        )
        self.mute_img = pygame.transform.scale(
            pygame.image.load(os.path.join(project_root, 'assets', 'img', 'volume-mute.png')),
            (40, 40)
        )
        self.music_btn_rect = self.volume_img.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        self.music_on = True
    
    def enter(self):
        """
        Được gọi khi màn hình bắt đầu hiển thị.
        """
        # Đường dẫn đến tệp nhạc nền
        bg_music_path = os.path.join(project_root, 'assets', 'sounds', 'bg-1.mp3')
        
        # Phát nhạc nền
        pygame.mixer.music.load(bg_music_path)
        pygame.mixer.music.set_volume(0.5)  # Đặt âm lượng (50%)
        pygame.mixer.music.play(-1)  # Phát lặp vô hạn
    
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
                if self.music_btn_rect.collidepoint(event.pos):
                    self.music_on = not self.music_on
                    pygame.mixer.music.set_volume(0.5 if self.music_on else 0)
                    mouse_clicked = False
        
        # Kiểm tra hover
        self.single_player_button.check_hover(mouse_pos)
        self.two_players_button.check_hover(mouse_pos)
        self.vs_ai_button.check_hover(mouse_pos)
        self.tutorial_button.check_hover(mouse_pos)
        self.exit_button.check_hover(mouse_pos)
        
        # Kiểm tra click
        if self.single_player_button.is_clicked(mouse_pos, mouse_clicked):
            self.manager.game_mode = "single"
            self.manager.change_state("difficulty")
            #self.manager.change_state("game")
        
        if self.two_players_button.is_clicked(mouse_pos, mouse_clicked):
            self.manager.game_mode = "two_players"
            self.manager.change_state("difficulty")
            #self.manager.change_state("game")
        
        if self.vs_ai_button.is_clicked(mouse_pos, mouse_clicked):
            self.manager.game_mode = "vs_ai"
            self.manager.change_state("difficulty")
            #self.manager.change_state("game")
        if self.tutorial_button.is_clicked(mouse_pos, mouse_clicked):
            self.manager.change_state("tutorials")
            
        if self.exit_button.is_clicked(mouse_pos, mouse_clicked):
            pygame.quit()
            sys.exit()
    
    def draw(self):
        """
        Vẽ màn hình menu.
        """
        # Vẽ hình nền
        self.screen.blit(self.background_image, (0, 0))
        
        # Vẽ tiêu đề
        title_surface = self.title_font.render("MAZE GAME", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_surface, title_rect)
        
        # Vẽ các nút
        self.single_player_button.draw(self.screen)
        self.two_players_button.draw(self.screen)
        self.vs_ai_button.draw(self.screen)
        self.tutorial_button.draw(self.screen)
        self.exit_button.draw(self.screen)
        
        # Vẽ thông tin phụ
        info_font = pygame.font.SysFont(None, 24)
        info_surface = info_font.render("", True, WHITE)
        info_rect = info_surface.get_rect(center=(SCREEN_WIDTH // 2, 500))
        self.screen.blit(info_surface, info_rect)
        
        # Draw volume toggle icon
        icon = self.volume_img if self.music_on else self.mute_img
        self.screen.blit(icon, self.music_btn_rect)
    
    def exit(self):
        """
        Được gọi khi thoát khỏi màn hình.
        """
        # Dừng nhạc nền
        pygame.mixer.music.stop()