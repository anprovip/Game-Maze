import random
import pygame
from collections import deque
from entities.player import Player
from config import BLUE, CELL_SIZE

class AIPlayer(Player):
    """
    Lớp đại diện cho người chơi AI.
    Kế thừa từ lớp Player và bổ sung khả năng tự di chuyển.
    """
    
    def __init__(self, x, y, difficulty="easy"):
        """
        Khởi tạo người chơi AI tại vị trí (x, y).
        
        Args:
            x (int): Tọa độ x ban đầu (đơn vị: ô)
            y (int): Tọa độ y ban đầu (đơn vị: ô)
            difficulty (str): Độ khó của AI ("easy", "medium", "hard")
        """
        super().__init__(x, y, color=BLUE)
        self.difficulty = difficulty
        self.path = []  # Đường đi đã tính toán
        self.path_index = 0  # Vị trí hiện tại trong đường đi
        self.move_timer = 0  # Bộ đếm thời gian giữa các bước di chuyển
        self.update_rate = self._get_update_rate()  # Tốc độ cập nhật theo độ khó
    
    def _get_update_rate(self):
        """
        Xác định tốc độ cập nhật dựa trên độ khó.
        
        Returns:
            int: Số khung hình giữa các lần cập nhật
        """
        if self.difficulty == "easy":
            return 30  # Khoảng 0.5 giây ở 60 FPS
        elif self.difficulty == "medium":
            return 15  # Khoảng 0.25 giây ở 60 FPS
        else:  # hard
            return 7   # Khoảng 0.117 giây ở 60 FPS
    
    def calculate_path(self, maze):
        """
        Tính toán đường đi từ vị trí hiện tại đến đích.
        
        Args:
            maze (Maze): Mê cung hiện tại
        """
        if self.difficulty == "easy":
            self._calculate_random_path(maze)
        elif self.difficulty == "medium":
            self._calculate_bfs_path(maze)
        else:  # hard
            self._calculate_astar_path(maze)
    
    def _calculate_random_path(self, maze):
        """
        Tính toán đường đi ngẫu nhiên (cho độ khó easy).
        
        Args:
            maze (Maze): Mê cung hiện tại
        """
        self.path = []
        self.path_index = 0
        
        # AI dễ chỉ nhìn trước vài bước
        max_steps = 5
        current_x, current_y = self.grid_x, self.grid_y
        
        for _ in range(max_steps):
            # Lấy các ô lân cận có thể đi được
            valid_neighbors = []
            for nx, ny in maze.get_neighbors(current_x, current_y):
                if not maze.is_wall(nx, ny):
                    valid_neighbors.append((nx, ny))
            
            if not valid_neighbors:
                break
            
            # Chọn ngẫu nhiên một ô để đi
            next_x, next_y = random.choice(valid_neighbors)
            self.path.append((next_x, next_y))
            current_x, current_y = next_x, next_y
    
    def _calculate_bfs_path(self, maze):
        """
        Tính toán đường đi bằng thuật toán BFS (cho độ khó medium).
        
        Args:
            maze (Maze): Mê cung hiện tại
        """
        start = (self.grid_x, self.grid_y)
        end = maze.end_pos
        
        # Khởi tạo queue và các biến
        queue = deque([start])
        visited = {start: None}  # Ô gốc không có ô cha
        
        while queue:
            x, y = queue.popleft()
            
            # Nếu tìm thấy đích
            if (x, y) == end:
                break
            
            # Kiểm tra các ô lân cận
            for nx, ny in maze.get_neighbors(x, y):
                if not maze.is_wall(nx, ny) and (nx, ny) not in visited:
                    queue.append((nx, ny))
                    visited[(nx, ny)] = (x, y)
        
        # Xây dựng đường đi từ đích về ô hiện tại
        if end in visited:
            path = []
            current = end
            while current != start:
                path.append(current)
                current = visited[current]
            
            self.path = path[::-1]  # Đảo ngược để có đường đi từ ô hiện tại đến đích
            self.path_index = 0
        else:
            # Không tìm thấy đường đi
            self.path = []
            self.path_index = 0
    
    def _calculate_astar_path(self, maze):
        """
        Tính toán đường đi bằng thuật toán A* (cho độ khó hard).
        Đây là thuật toán tìm đường tốt nhất.
        
        Args:
            maze (Maze): Mê cung hiện tại
        """
        start = (self.grid_x, self.grid_y)
        end = maze.end_pos
        
        # Đây là phần cài đặt A* đơn giản
        # Trong dự án thực tế, bạn có thể cài đặt chi tiết hơn
        
        # Sẽ dùng BFS cho ví dụ này (trong dự án thực bạn nên cài đặt A* đầy đủ)
        self._calculate_bfs_path(maze)
    
    def update(self, maze):
        """
        Cập nhật vị trí AI dựa trên đường đi đã tính toán.
        
        Args:
            maze (Maze): Mê cung hiện tại
        """
        # Tăng bộ đếm thời gian
        self.move_timer += 1
        
        # Kiểm tra xem đã đến lúc cập nhật chưa
        if self.move_timer < self.update_rate:
            return
        
        # Reset bộ đếm
        self.move_timer = 0
        
        # Nếu chưa có đường đi hoặc đã đi hết đường, tính toán lại
        if not self.path or self.path_index >= len(self.path):
            self.calculate_path(maze)
        
        # Nếu có đường đi hợp lệ, di chuyển theo đường đi
        if self.path and self.path_index < len(self.path):
            next_x, next_y = self.path[self.path_index]
            
            # Xác định hướng di chuyển
            self.dx = 1 if next_x > self.grid_x else (-1 if next_x < self.grid_x else 0)
            self.dy = 1 if next_y > self.grid_y else (-1 if next_y < self.grid_y else 0)
            
            # Cập nhật vị trí
            if not maze.is_wall(next_x, next_y):
                self.grid_x = next_x
                self.grid_y = next_y
                self.x = next_x * CELL_SIZE + CELL_SIZE // 2
                self.y = next_y * CELL_SIZE + CELL_SIZE // 2
                self.path_index += 1