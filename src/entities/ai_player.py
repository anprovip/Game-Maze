import pygame
from collections import deque
from entities.player import Player
from config import BLUE, CELL_SIZE

class AIPlayer(Player):
    """
    Lớp đại diện cho người chơi AI sử dụng BFS,
    độ khó chỉ ảnh hưởng đến tốc độ di chuyển.
    """

    def __init__(self, x, y, difficulty="easy", image_path='assets/img/player.png'):
        """
        Khởi tạo người chơi AI tại vị trí (x, y).
        
        Args:
            x (int): Tọa độ x ban đầu (ô)
            y (int): Tọa độ y ban đầu (ô)
            difficulty (str): "easy", "medium", hoặc "hard"
            image_path (str): Đường dẫn tới hình ảnh của người chơi
        """
        super().__init__(x, y, color=BLUE, image_path=image_path)
        self.difficulty = difficulty
        self.path = []
        self.path_index = 0
        self.move_timer = 0
        self.update_rate = self._get_update_rate()
        self.recalculate_counter = 0  # Đếm để tính lại đường đi định kỳ
        # For hard difficulty freeze cycle
        self.hard_freezing = False
        self.last_freeze_cycle_tick = pygame.time.get_ticks()
        self.freeze_start_tick = None

    def _get_update_rate(self):
        """
        Xác định tốc độ di chuyển dựa trên độ khó.
        Returns:
            int: số khung hình giữa mỗi lần di chuyển
        """
        # Giảm giá trị để AI di chuyển nhanh hơn
        if self.difficulty == "easy":
            return 35  # rất chậm
        elif self.difficulty == "medium":
            return 25  # chậm hơn một chút
        else:  # hard
            return 15   # di chuyển mỗi frame, cực nhanh

    def _calculate_bfs_path(self, maze):
        """
        Tìm đường đi từ vị trí hiện tại đến đích bằng BFS.
        """
        start = (self.grid_x, self.grid_y)
        end = maze.end_pos
        
        # Debug
        print(f"AI tại: {start}, mục tiêu: {end}")
        
        # Kiểm tra xem AI có nằm trên tường không
        if maze.is_wall(self.grid_x, self.grid_y):
            print("LỖI: AI đang nằm trên tường! Di chuyển AI đến vị trí bắt đầu.")
            self.grid_x, self.grid_y = maze.start_pos
            self.x = self.grid_x * CELL_SIZE + CELL_SIZE // 2
            self.y = self.grid_y * CELL_SIZE + CELL_SIZE // 2
            start = maze.start_pos
        
        # Nếu đã ở đích, không cần tìm đường
        if start == end:
            self.path = []
            self.path_index = 0
            return

        queue = deque([start])
        visited = {start: None}

        # Thực hiện BFS
        while queue:
            x, y = queue.popleft()
            if (x, y) == end:
                break

            # Debug để xem có lỗi trong get_neighbors không
            neighbors = maze.get_neighbors(x, y)
            
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
            path.reverse()  # Đảo ngược để có đường đi từ start đến end
            self.path = path
            self.path_index = 0
            print(f"Tìm thấy đường đi: {len(self.path)} bước")
        else:
            self.path = []
            self.path_index = 0
            print("Không tìm thấy đường đi!")
            # Debug: In cấu trúc mê cung
            print("Cấu trúc mê cung:")
            for y in range(maze.height):
                row = ""
                for x in range(maze.width):
                    if (x, y) == start:
                        row += "S"
                    elif (x, y) == end:
                        row += "E"
                    elif maze.is_wall(x, y):
                        row += "#"
                    else:
                        row += "."
                print(row)
         
            
            # Debug
            print(f"AI tại: {start}, mục tiêu: {end}")
            
            # Kiểm tra xem AI có nằm trên tường không
            if maze.is_wall(self.grid_x, self.grid_y):
                print("LỖI: AI đang nằm trên tường! Di chuyển AI đến vị trí bắt đầu.")
                self.grid_x, self.grid_y = maze.start_pos
                self.x = self.grid_x * CELL_SIZE + CELL_SIZE // 2
                self.y = self.grid_y * CELL_SIZE + CELL_SIZE // 2
                start = maze.start_pos
            
            # Nếu đã ở đích, không cần tìm đường
            if start == end:
                self.path = []
                self.path_index = 0
                return

            queue = deque([start])
            visited = {start: None}

            # Thực hiện BFS
            while queue:
                x, y = queue.popleft()
                if (x, y) == end:
                    break

                # Debug để xem có lỗi trong get_neighbors không
                neighbors = maze.get_neighbors(x, y)
                
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
                path.reverse()  # Đảo ngược để có đường đi từ start đến end
                self.path = path
                self.path_index = 0
                print(f"Tìm thấy đường đi: {len(self.path)} bước")
            else:
                self.path = []
                self.path_index = 0
                print("Không tìm thấy đường đi!")
                # Debug: In cấu trúc mê cung
                print("Cấu trúc mê cung:")
                for y in range(maze.height):
                    row = ""
                    for x in range(maze.width):
                        if (x, y) == start:
                            row += "S"
                        elif (x, y) == end:
                            row += "E"
                        elif maze.is_wall(x, y):
                            row += "#"
                        else:
                            row += "."
                    print(row)
               

    def calculate_path(self, maze):
        """
        Tính toán lại đường đi (luôn dùng BFS).
        """
        self._calculate_bfs_path(maze)

    def update(self, maze):
        """
        Cập nhật vị trí AI dựa trên đường đi đã tính.
        """
        now = pygame.time.get_ticks()
        # Hard-mode: freeze every 15s for 2s
        if self.difficulty == "hard":
            if not self.hard_freezing and now - self.last_freeze_cycle_tick >= 10000:
                self.hard_freezing = True
                self.freeze_start_tick = now
            if self.hard_freezing:
                if now - self.freeze_start_tick < 2000:
                    return
                # end freeze
                self.hard_freezing = False
                self.last_freeze_cycle_tick = now
        
        # Tăng bộ đếm thời gian
        self.move_timer += 1
        self.recalculate_counter += 1
        
        # Tính lại đường đi định kỳ hoặc khi cần
        if self.recalculate_counter >= 60 or not self.path:
            self.calculate_path(maze)
            self.recalculate_counter = 0
        
        # Chỉ di chuyển khi đã đủ thời gian theo tốc độ
        if self.move_timer < self.update_rate:
            return
        
        # Reset bộ đếm thời gian
        self.move_timer = 0
        
        # Kiểm tra xem có đường đi không và chưa đến đích
        if self.path and self.path_index < len(self.path):
            # Lấy tọa độ ô tiếp theo trên đường đi
            next_x, next_y = self.path[self.path_index]
            
            # Cập nhật hướng di chuyển
            self.dx = 1 if next_x > self.grid_x else (-1 if next_x < self.grid_x else 0)
            self.dy = 1 if next_y > self.grid_y else (-1 if next_y < self.grid_y else 0)
            
            # Di chuyển đến ô tiếp theo
            self.grid_x = next_x
            self.grid_y = next_y
            self.x = next_x * CELL_SIZE + CELL_SIZE // 2
            self.y = next_y * CELL_SIZE + CELL_SIZE // 2
            self.path_index += 1
    
    def draw(self, screen, offset_x=0, offset_y=0):
        """
        Vẽ người chơi AI và đường đi (để debug).
        """
        # Vẽ người chơi
        super().draw(screen, offset_x, offset_y)
        
        # Vẽ đường đi (để debug, có thể bỏ trong phiên bản cuối)
        # if self.path:
        #     for i, (x, y) in enumerate(self.path):
        #         if i >= self.path_index:  # Chỉ vẽ phần đường đi còn lại
        #             # Tạo hình tròn nhỏ cho mỗi điểm trên đường đi
        #             center_x = offset_x + x * CELL_SIZE + CELL_SIZE // 2
        #             center_y = offset_y + y * CELL_SIZE + CELL_SIZE // 2
        #             radius = max(2, CELL_SIZE // 10)
                    
        #             # Màu đậm dần theo tiến trình đường đi
        #             alpha = 50 + min(200, 50 * (len(self.path) - i) // max(1, len(self.path)))
        #             color = (0, 100, 255)
                    
        #             pygame.draw.circle(screen, color, (center_x, center_y), radius)