import pygame
from config import BLACK, GRAY, GREEN, RED, WHITE, CELL_SIZE

class Maze:
    """
    Lớp đại diện cho mê cung, lưu trữ cấu trúc mê cung và cung cấp các phương thức
    để tương tác với mê cung.
    """
    def __init__(self, width, height):
        """
        Khởi tạo mê cung trống với kích thước cho trước.
        
        Args:
            width (int): Số ô theo chiều ngang
            height (int): Số ô theo chiều dọc
        """
        self.width = width
        self.height = height
        
        # Khởi tạo mảng 2D để lưu trữ mê cung
        # True: Tường, False: Đường đi
        self.grid = [[True for _ in range(width)] for _ in range(height)]
        
        # Vị trí bắt đầu và kết thúc
        self.start_pos = (0, 0)
        self.end_pos = (width - 1, height - 1)
    
    def set_cell(self, x, y, is_wall):
        """
        Thiết lập ô tại vị trí (x, y) là tường hoặc đường đi.
        
        Args:
            x (int): Tọa độ x
            y (int): Tọa độ y
            is_wall (bool): True nếu là tường, False nếu là đường đi
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = is_wall
    
    def is_wall(self, x, y):
        """
        Kiểm tra ô tại vị trí (x, y) có phải là tường không.
        
        Args:
            x (int): Tọa độ x
            y (int): Tọa độ y
        
        Returns:
            bool: True nếu là tường, False nếu là đường đi
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return True  # Ngoài biên luôn là tường
    
    def set_start(self, x, y):
        """Thiết lập vị trí bắt đầu"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.start_pos = (x, y)
            self.set_cell(x, y, False)  # Đảm bảo vị trí bắt đầu là đường đi
    
    def set_end(self, x, y):
        """Thiết lập vị trí kết thúc"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.end_pos = (x, y)
            self.set_cell(x, y, False)  # Đảm bảo vị trí kết thúc là đường đi
    
    def get_neighbors(self, x, y):
        """
        Lấy danh sách các ô lân cận (4 hướng) của ô tại vị trí (x, y).
        
        Args:
            x (int): Tọa độ x
            y (int): Tọa độ y
        
        Returns:
            list: Danh sách các tọa độ (x, y) lân cận
        """
        neighbors = []
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Lên, phải, xuống, trái
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append((nx, ny))
        
        return neighbors
    
    def draw(self, screen, offset_x=0, offset_y=0):
        """
        Vẽ mê cung lên màn hình.
        
        Args:
            screen: Bề mặt pygame để vẽ
            offset_x (int): Độ dịch theo chiều ngang
            offset_y (int): Độ dịch theo chiều dọc
        """
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    offset_x + x * CELL_SIZE,
                    offset_y + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
                
                if self.grid[y][x]:  # Nếu là tường
                    pygame.draw.rect(screen, BLACK, rect)
                else:  # Nếu là đường đi
                    pygame.draw.rect(screen, WHITE, rect)
                    pygame.draw.rect(screen, GRAY, rect, 1)  # Viền
                
                # Vẽ vị trí bắt đầu
                if (x, y) == self.start_pos:
                    pygame.draw.rect(screen, GREEN, rect)
                
                # Vẽ vị trí kết thúc
                if (x, y) == self.end_pos:
                    pygame.draw.rect(screen, RED, rect)