import pygame
import sys
from collections import deque
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
        self.show_hint = False
        self.hint_path = []
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
        Được gọi khi chuyển sang màn hình game.
        """
        # Tạo mê cung mới cho cấp độ hiện tại
        self.current_level = Level(self.manager.level)
        self.maze = self.current_level.generate_maze(self.manager.maze_generator_type)
        
        # Lấy vị trí bắt đầu từ mê cung
        start_x, start_y = self.maze.start_pos
        
        # Khởi tạo người chơi tại vị trí bắt đầu
        self.players = []
        
        if self.manager.game_mode == "single":
            # Chế độ một người chơi
            self.players.append(Player(start_x, start_y))
        
        elif self.manager.game_mode == "two_players":
            # Chế độ hai người chơi
            self.players.append(Player(start_x, start_y))
            self.players.append(Player(start_x, start_y, color=GREEN))
        
        elif self.manager.game_mode == "vs_ai":
            # Chế độ đấu với AI
            self.players.append(Player(start_x, start_y))
            # Khởi tạo AI tại CÙNG vị trí bắt đầu với người chơi
            self.players.append(AIPlayer(start_x, start_y, difficulty=self.manager.ai_difficulty))
        
        # Biến trạng thái
        self.game_over = False
        self.winner = None
        self.show_hint = False
        self.hint_path = []
        
        # Debug: In ra cấu trúc mê cung
        print("Cấu trúc mê cung:")
        for y in range(self.maze.height):
            row = ""
            for x in range(self.maze.width):
                if (x, y) == self.maze.start_pos:
                    row += "S"
                elif (x, y) == self.maze.end_pos:
                    row += "E"
                elif self.maze.is_wall(x, y):
                    row += "#"
                else:
                    row += "."
            print(row)
    
    def exit(self):
        """
        Được gọi khi thoát khỏi màn hình.
        """
        pass
    
    def calculate_hint_path(self):
        """
        Tính toán đường đi gợi ý từ vị trí người chơi đến đích bằng thuật toán BFS.
        """
        if not self.players or self.manager.game_mode != "single":
            return
        
        player = self.players[0]
        start = (player.grid_x, player.grid_y)
        end = self.maze.end_pos
        
        # Nếu đã ở đích, không cần tìm đường
        if start == end:
            self.hint_path = []
            return
        
        queue = deque([start])
        visited = {start: None}
        
        # Thực hiện BFS
        while queue:
            x, y = queue.popleft()
            if (x, y) == end:
                break
            
            # Lấy các ô lân cận
            neighbors = self.maze.get_neighbors(x, y)
            
            for nx, ny in neighbors:
                if (nx, ny) not in visited:
                    queue.append((nx, ny))
                    visited[(nx, ny)] = (x, y)
        
        # Tạo đường đi
        if end in visited:
            path = []
            current = end
            while current != start:
                path.append(current)
                current = visited[current]
            path.reverse()
            self.hint_path = path
        else:
            self.hint_path = []
    
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
        
        # Kiểm tra sự kiện
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
            if event.type == pygame.KEYDOWN:
                # Khi nhấn phím Q, hiển thị/ẩn gợi ý
                if event.key == pygame.K_q and self.manager.game_mode == "single":
                    if not self.show_hint:
                        # Tính toán đường đi mỗi khi bật gợi ý
                        self.calculate_hint_path()
                    self.show_hint = not self.show_hint
        
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
        
        # Cập nhật đường đi gợi ý nếu đang hiển thị
        if self.show_hint and self.manager.game_mode == "single" :
            self.calculate_hint_path()
        
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
        
        # Vẽ đường đi gợi ý nếu được bật
        if self.show_hint and self.hint_path:
            for i, (x, y) in enumerate(self.hint_path):
                # Vẽ điểm trên đường đi
                center_x = offset_x + x * CELL_SIZE + CELL_SIZE // 2
                center_y = offset_y + y * CELL_SIZE + CELL_SIZE // 2
                radius = CELL_SIZE // 6
                
                # Màu đậm dần theo tiến trình đường đi
                color_value = 255 - min(200, 10 * i)
                pygame.draw.circle(self.screen, (0, color_value, 0), (center_x, center_y), radius)
        
        # Vẽ người chơi
        for player in self.players:
            player.draw(self.screen, offset_x, offset_y)
        
        # Hiển thị thông tin phím tắt nếu ở chế độ một người chơi
        if self.manager.game_mode == "single":
            hint_text = "Press Q for hint" if not self.show_hint else "Press Q to hide hint"
            hint_surface = self.font.render(hint_text, True, WHITE)
            self.screen.blit(hint_surface, (SCREEN_WIDTH - 220, 20))
        
        # Vẽ nút pause
        self.pause_button.draw(self.screen)
        
        # Vẽ thông báo chiến thắng nếu game kết thúc
        if self.game_over:
            # Tạo nền mờ
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # RGBA, alpha=128 để mờ
            self.screen.blit(overlay, (0, 0))
            
            # Hiển thị thông báo
            if self.winner is not None:
                if self.manager.game_mode == "vs_ai":
                    win_text = "You win!" if self.winner == 0 else "AI wins!"
                else:
                    win_text = f"Player {self.winner + 1} wins!"
                
                text_surface = self.font.render(win_text, True, WHITE)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
                self.screen.blit(text_surface, text_rect)
            
            # Hiển thị hướng dẫn
            hint_surface = self.font.render("Press Enter to return to menu", True, WHITE)
            hint_rect = hint_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(hint_surface, hint_rect)