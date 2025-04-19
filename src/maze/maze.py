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
        
        # Load hình ảnh
        self.wall_img = pygame.image.load('assets/img/wall.png')
        self.bg_img = pygame.transform.scale(pygame.image.load('assets/img/bg.jpg'), (CELL_SIZE, CELL_SIZE))
        self.start_img = pygame.transform.scale(pygame.image.load('assets/img/player.png'), (CELL_SIZE, CELL_SIZE))
        self.goal_img = pygame.transform.scale(pygame.image.load('assets/img/goal.png'), (CELL_SIZE, CELL_SIZE))
        
        # Thay đổi kích thước ảnh tường để phù hợp với CELL_SIZE
        self.wall_img = pygame.transform.scale(self.wall_img, (CELL_SIZE, CELL_SIZE))
    
    def set_cell(self, x, y, is_wall):
        """
        Thiết lập giá trị của một ô trong mê cung.
        
        Args:
            x (int): Tọa độ x của ô
            y (int): Tọa độ y của ô
            is_wall (bool): True nếu là tường, False nếu là đường đi
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = is_wall
    
    def get_cell(self, x, y):
        """
        Lấy giá trị của một ô trong mê cung.
        
        Args:
            x (int): Tọa độ x của ô
            y (int): Tọa độ y của ô
            
        Returns:
            bool: True nếu là tường, False nếu là đường đi
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return True  # Trả về tường nếu ô nằm ngoài mê cung
    
    def is_wall(self, x, y):
        """
        Kiểm tra xem một ô có phải là tường hay không.
        
        Args:
            x (int): Tọa độ x của ô
            y (int): Tọa độ y của ô
            
        Returns:
            bool: True nếu là tường, False nếu là đường đi
        """
        return self.get_cell(x, y)
    
    def set_start(self, x, y):
        """
        Thiết lập vị trí bắt đầu.
        
        Args:
            x (int): Tọa độ x
            y (int): Tọa độ y
        """
        self.start_pos = (x, y)
        
    def set_end(self, x, y):
        """
        Thiết lập vị trí kết thúc.
        
        Args:
            x (int): Tọa độ x
            y (int): Tọa độ y
        """
        self.end_pos = (x, y)
    
    def get_neighbors(self, x, y):
        """
        Lấy danh sách các ô lân cận có thể đi được từ một ô.
        
        Args:
            x (int): Tọa độ x của ô
            y (int): Tọa độ y của ô
            
        Returns:
            list: Danh sách các tọa độ (x, y) của các ô lân cận có thể đi được
        """
        neighbors = []
        # Kiểm tra 4 hướng: trên, phải, dưới, trái
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Kiểm tra xem ô có nằm trong mê cung và không phải là tường
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not self.is_wall(nx, ny):  # Chỉ thêm vào nếu không phải tường
                    neighbors.append((nx, ny))
        
        return neighbors

    def draw(self, screen, offset_x=0, offset_y=0):
        """
        Vẽ mê cung lên màn hình sử dụng hình ảnh.
        
        Args:
            screen: Bề mặt pygame để vẽ
            offset_x (int): Độ dịch theo chiều ngang
            offset_y (int): Độ dịch theo chiều dọc
        """
        for y in range(self.height):
            for x in range(self.width):
                # Tính toán vị trí để vẽ ảnh
                pos = (offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE)
                
                # Vẽ nền (đường đi hoặc tường) trước
                if self.grid[y][x]:  # Nếu là tường
                    # Không vẽ tường ở vị trí đích (để tránh chồng lên nhau)
                    if (x, y) != self.end_pos:
                        screen.blit(self.wall_img, pos)
                    else:
                        # Nếu là vị trí đích, vẽ nền đường đi
                        screen.blit(self.bg_img, pos)
                else:  # Nếu là đường đi
                    screen.blit(self.bg_img, pos)
                
                # Vẽ vị trí bắt đầu và kết thúc sau cùng (để chúng luôn hiển thị trên cùng)
                
                
                if (x, y) == self.end_pos:
                    screen.blit(self.goal_img, pos)