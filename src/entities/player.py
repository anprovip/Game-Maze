import os
import pygame
from config import CELL_SIZE, PLAYER_SPEED

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

class Player:
    """
    Lớp đại diện cho người chơi trong game.
    """
    
    def __init__(self, x, y, color=(255, 0, 0), image_path = os.path.join(project_root, 'assets', 'img', 'player.png')):
        """
        Khởi tạo người chơi tại vị trí (x, y).
        
        Args:
            x (int): Tọa độ x ban đầu (đơn vị: ô)
            y (int): Tọa độ y ban đầu (đơn vị: ô)
            color (tuple): Màu sắc của người chơi (R, G, B)
            image_path (str): Đường dẫn đến hình ảnh của người chơi
        """
        self.grid_x = x  # Tọa độ theo ô
        self.grid_y = y
        self.x = x * CELL_SIZE + CELL_SIZE // 2  # Tọa độ pixel (giữa ô)
        self.y = y * CELL_SIZE + CELL_SIZE // 2
        self.color = color
        self.speed = PLAYER_SPEED
        
        # Hướng di chuyển hiện tại
        self.dx = 0
        self.dy = 0
        
        self.facing_left = False
        # Load hình ảnh người chơi từ đường dẫn tùy chọn
        self.player_img = pygame.image.load(image_path)
        self.player_img = pygame.transform.scale(self.player_img, (CELL_SIZE - 6, CELL_SIZE - 6))
        #Tai am thanh
        footstep_path = os.path.join(project_root, 'assets', 'sounds', 'cartoon-jump.mp3')
        self.footstep_sound = pygame.mixer.Sound(footstep_path)
    
    def handle_input(self, keys, player_num=1):
        """
        Xử lý đầu vào từ bàn phím cho người chơi.
        
        Args:
            keys: Phím đang được nhấn (từ pygame.key.get_pressed())
            player_num (int): Số thứ tự người chơi (1 hoặc 2)
        """
        self.dx = 0
        self.dy = 0
        sound_played = False 

        if player_num == 1:
            # Điều khiển cho người chơi 1 (phím mũi tên)
            if keys[pygame.K_LEFT]:
                self.dx = -1
                sound_played = True
                if self.facing_left:  # Chỉ lật ảnh nếu đang hướng trái
                    self.player_img = pygame.transform.flip(self.player_img, True, False)
                    self.facing_left = False
            elif keys[pygame.K_RIGHT]:
                self.dx = 1
                sound_played = True
                if not self.facing_left:  # Chỉ lật ảnh nếu đang hướng phải
                    self.player_img = pygame.transform.flip(self.player_img, True, False)
                    self.facing_left = True
            if keys[pygame.K_UP]:
                self.dy = -1
                sound_played = True
            elif keys[pygame.K_DOWN]:
                self.dy = 1
                sound_played = True
        else:
            # Điều khiển cho người chơi 2 (WASD)
            if keys[pygame.K_a]:
                self.dx = -1
                sound_played = True
                if not self.facing_left:  
                    self.player_img = pygame.transform.flip(self.player_img, True, False)
                    self.facing_left = True
            elif keys[pygame.K_d]:
                self.dx = 1
                sound_played = True
                if self.facing_left:
                    self.player_img = pygame.transform.flip(self.player_img, True, False)
                    self.facing_left = False
            if keys[pygame.K_w]:
                self.dy = -1
                sound_played = True
            elif keys[pygame.K_s]:
                self.dy = 1
                sound_played = True
        if sound_played:
            self.footstep_sound.play()
    
    def update(self, maze):
        """
        Cập nhật vị trí người chơi dựa trên hướng di chuyển và kiểm tra va chạm với tường.
        
        Args:
            maze (Maze): Mê cung hiện tại
        """
        # Tính vị trí mới theo pixel
        new_x = self.x + self.dx * self.speed
        new_y = self.y + self.dy * self.speed
        
        # Tính vị trí ô mới
        new_grid_x = new_x // CELL_SIZE
        new_grid_y = new_y // CELL_SIZE
        
        # Kiểm tra va chạm với tường
        if not maze.is_wall(new_grid_x, new_grid_y):
            self.x = new_x
            self.y = new_y
            self.grid_x = new_grid_x
            self.grid_y = new_grid_y
    
    def draw(self, screen, offset_x=0, offset_y=0):
        """
        Vẽ người chơi lên màn hình sử dụng hình ảnh.
        
        Args:
            screen: Bề mặt pygame để vẽ
            offset_x (int): Độ dịch theo chiều ngang
            offset_y (int): Độ dịch theo chiều dọc
        """
        # Tính toán vị trí để vẽ ảnh (căn giữa ô)
        pos_x = offset_x + self.grid_x * CELL_SIZE + (CELL_SIZE - self.player_img.get_width()) // 2
        pos_y = offset_y + self.grid_y * CELL_SIZE + (CELL_SIZE - self.player_img.get_height()) // 2
        
        # Vẽ hình ảnh người chơi
        screen.blit(self.player_img, (pos_x, pos_y))
    
    def is_at_end(self, maze):
        """
        Kiểm tra xem người chơi đã đến đích chưa.
        
        Args:
            maze (Maze): Mê cung hiện tại
        
        Returns:
            bool: True nếu người chơi đã đến đích
        """
        return (self.grid_x, self.grid_y) == maze.end_pos