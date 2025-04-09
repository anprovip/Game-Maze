import pygame
import sys
from ui.screen import Screen
from ui.button import Button
from game.level import Level
from entities.player import Player
from entities.ai_player import AIPlayer
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, RED, GREEN, BLUE, CELL_SIZE

class GameScreen(Screen):
    """
    Màn hình chơi game.
    """
    
    def __init__(self, manager):
        """
        Khởi tạo màn hình game.
        
        Args:
            manager: Game Manager quản lý các trạng thái
        """
        super().__init__(manager)
        
        # Nút tạm dừng
        self.pause_button = Button(
            20, 20, 100, 40, "Pause", (150, 150, 150), (200, 200, 200)
        )
        
        # Biến game
        self.maze = None
        self.players = []
        self.current_level = None
        self.game_over = False
        self.winner = None
        
        # Font
        self.font = pygame.font.SysFont(None, 36)
    
    def enter(self):
        """
        Được gọi khi màn hình bắt đầu hiển thị.
        """
        # Khởi tạo cấp độ
        self.current_level = Level(self.manager.level)
        
        # Tạo mê cung
        self.maze = self.current_level.generate_maze(self.manager.maze_generator_type)
        
        # Khởi tạo người chơi
        self.players = []
        self.game_over = False
        self.winner = None
        
        # Khởi tạo người chơi dựa trên chế độ chơi
        if self.manager.game_mode == "single":
            # Chế độ 1 người chơi
            self.players.append(Player(0, 0, RED))
            
        elif self.manager.game_mode == "two_players":
            # Chế độ 2 người chơi
            self.players.append(Player(0, 0, RED))
            self.players.append(Player(0, 1, GREEN))
            
        elif self.manager.game_mode == "vs_ai":
            # Chế độ chơi với máy
            self.players.append(Player(0, 0, RED))
            self.players.append(AIPlayer(0, 1, self.manager.ai_difficulty))
    
    def exit(self):
        """
        Được gọi khi thoát khỏi màn hình.
        """
        pass
    
    def update(self, events):
        """
        Cập nhật màn hình game dựa trên sự kiện đầu vào.
        
        Args:
            events: Danh sách các sự kiện pygame
        """
        if self.game_over:
            # Kiểm tra sự kiện để quay lại menu
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        self.manager.change_state("menu")
            return
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        # Kiểm tra sự kiện chuột
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
        
        # Kiểm tra nút pause
        self.pause_button.check_hover(mouse_pos)
        if self.pause_button.is_clicked(mouse_pos, mouse_clicked):
            self.manager.change_state("pause")
        
        # Xử lý đầu vào cho người chơi
        keys = pygame.key.get_pressed()
        
        # Người chơi 1
        if len(self.players) > 0:
            self.players[0].handle_input(keys, 1)
            self.players[0].update(self.maze)
            
            # Kiểm tra chiến thắng
            if self.players[0].is_at_end(self.maze):
                self.game_over = True
                self.winner = 0
        
        # Người chơi 2 hoặc AI
        if len(self.players) > 1:
            if isinstance(self.players[1], AIPlayer):
                # AI tự cập nhật
                self.players[1].update(self.maze)
            else:
                # Người chơi 2
                self.players[1].handle_input(keys, 2)
                self.players[1].update(self.maze)
            
            # Kiểm tra chiến thắng
            if self.players[1].is_at_end(self.maze):
                self.game_over = True
                self.winner = 1
    
    def draw(self):
        """
        Vẽ màn hình game.
        """
        # Xóa màn hình
        self.screen.fill((50, 80, 50))
        
        # Tính toán vị trí để mê cung nằm ở giữa màn hình
        maze_pixel_width = self.maze.width * CELL_SIZE
        maze_pixel_height = self.maze.height * CELL_SIZE
        
        offset_x = (SCREEN_WIDTH - maze_pixel_width) // 2
        offset_y = (SCREEN_HEIGHT - maze_pixel_height) // 2
        
        # Vẽ mê cung
        self.maze.draw(self.screen, offset_x, offset_y)
        
        # Vẽ người chơi
        for player in self.players:
            player.draw(self.screen, offset_x, offset_y)
        
        # Vẽ nút pause
        self.pause_button.draw(self.screen)
        
        # Vẽ thông báo chiến thắng nếu game kết thúc
        if self.game_over and self.winner is not None:
            # Xác định thông báo chiến thắng
            if self.manager.game_mode == "single":
                win_text = f"You Win! Level {self.manager.level} Completed!"
            elif self.manager.game_mode == "two_players":
                win_text = f"Player {self.winner + 1} Wins!"
            else:  # vs_ai
                if self.winner == 0:
                    win_text = "You Win!"
                else:
                    win_text = "AI Wins!"
            
            # Vẽ hộp thông báo
            message_box = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3,
                                    SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            pygame.draw.rect(self.screen, (200, 200, 200), message_box)
            pygame.draw.rect(self.screen, (0, 0, 0), message_box, 3)
            
            # Vẽ thông báo
            win_surface = self.font.render(win_text, True, (0, 0, 0))
            win_rect = win_surface.get_rect(center=message_box.center)
            self.screen.blit(win_surface, win_rect)
            
            # Vẽ hướng dẫn
            guide_font = pygame.font.SysFont(None, 24)
            guide_text = "Press Enter or Esc to return to menu"
            guide_surface = guide_font.render(guide_text, True, (0, 0, 0))
            guide_rect = guide_surface.get_rect(centerx=message_box.centerx,
                                              top=win_rect.bottom + 20)
            self.screen.blit(guide_surface, guide_rect)