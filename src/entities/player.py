import pygame
from config import CELL_SIZE, PLAYER_SPEED

class Player:
    """
    Lớp đại diện cho người chơi trong game.
    """
    
    def __init__(self, x, y, color=(255, 0, 0)):
        """
        Khởi tạo người chơi tại vị trí (x, y).
        
        Args:
            x (int): Tọa độ x ban đầu (đơn vị: ô)
            y (int): Tọa độ y ban đầu (đơn vị: ô)
            color (tuple): Màu sắc của người chơi (R, G, B)
        """
        self.grid_x = x  # Tọa độ theo ô
        self.grid_y = y
        self.x = x * CELL_SIZE + CELL_SIZE // 2  # Tọa độ pixel (giữa ô)
        self.y = y * CELL_SIZE + CELL_SIZE // 2
        self.color = color
        self.radius = CELL_SIZE // 3  # Bán kính người chơi
        self.speed = PLAYER_SPEED
        
        # Hướng di chuyển hiện tại
        self.dx = 0
        self.dy = 0
    
    def handle_input(self, keys, player_num=1):
        """
        Xử lý đầu vào từ bàn phím cho người chơi.
        
        Args:
            keys: Phím đang được nhấn (từ pygame.key.get_pressed())
            player_num (int): Số thứ tự người chơi (1 hoặc 2)
        """
        self.dx = 0
        self.dy = 0
        
        if player_num == 1:
            # Điều khiển cho người chơi 1 (phím mũi tên)
            if keys[pygame.K_LEFT]:
                self.dx = -1
            elif keys[pygame.K_RIGHT]:
                self.dx = 1
            
            if keys[pygame.K_UP]:
                self.dy = -1
            elif keys[pygame.K_DOWN]:
                self.dy = 1
        else:
            # Điều khiển cho người chơi 2 (WASD)
            if keys[pygame.K_a]:
                self.dx = -1
            elif keys[pygame.K_d]:
                self.dx = 1
            
            if keys[pygame.K_w]:
                self.dy = -1
            elif keys[pygame.K_s]:
                self.dy = 1
    
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
        Vẽ người chơi lên màn hình.
        
        Args:
            screen: Bề mặt pygame để vẽ
            offset_x (int): Độ dịch theo chiều ngang
            offset_y (int): Độ dịch theo chiều dọc
        """
        pygame.draw.circle(
            screen, 
            self.color, 
            (offset_x + self.x, offset_y + self.y), 
            self.radius
        )
    
    def is_at_end(self, maze):
        """
        Kiểm tra xem người chơi đã đến đích chưa.
        
        Args:
            maze (Maze): Mê cung hiện tại
        
        Returns:
            bool: True nếu người chơi đã đến đích
        """
        return (self.grid_x, self.grid_y) == maze.end_pos