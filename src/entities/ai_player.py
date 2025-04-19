import os
import pygame
import random
from collections import deque
from entities.player import Player
from config import BLUE, CELL_SIZE

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
image_path = os.path.join(project_root, 'assets', 'img', 'cat.png')

class AIPlayer(Player):
    """
    Lớp đại diện cho người chơi AI sử dụng BFS, với khả năng đi đến điểm trung gian để đánh lừa.
    Độ khó ảnh hưởng đến tốc độ, tần suất điểm trung gian, và phản ứng với người chơi.
    """

    def __init__(self, x, y, difficulty="easy", image_path=image_path):
        super().__init__(x, y, color=BLUE, image_path=image_path)
        self.difficulty = difficulty
        self.path = []
        self.path_index = 0
        self.move_timer = 0
        self.update_rate = self._get_update_rate()
        self.recalculate_counter = 0
        self.hard_freezing = False
        self.last_freeze_cycle_tick = pygame.time.get_ticks()
        self.freeze_start_tick = None
        self.target = None  # Điểm mục tiêu hiện tại (điểm trung gian hoặc đích)
        self.hesitation_timer = 0  # Bộ đếm để giả vờ "do dự"
        self.hesitation_duration = 30  # Số khung hình dừng lại để do dự
        self.is_hesitating = False  # Trạng thái do dự

    def _get_update_rate(self):
        """Xác định tốc độ di chuyển dựa trên độ khó."""
        if self.difficulty == "easy":
            return 10  # Chậm hơn một chút để người chơi dễ vượt
        elif self.difficulty == "medium":
            return 10  # Tốc độ trung bình
        else:  # hard
            return 12  # Rất nhanh để cạnh tranh

    def _get_neighbors(self, x, y, maze):
        """Lấy các ô lân cận hợp lệ."""
        neighbors = []
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Lên, phải, xuống, trái
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < maze.width and 0 <= ny < maze.height and not maze.is_wall(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def _bfs(self, maze, start, goal):
        """Tìm đường ngắn nhất từ start đến goal bằng BFS."""
        queue = deque([(start, [])])
        visited = {start}
        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == goal:
                return path + [(x, y)]
            for nx, ny in self._get_neighbors(x, y, maze):
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(x, y)]))
        return []

    def _get_random_waypoint(self, maze, goal, player_pos):
        """Chọn điểm trung gian ngẫu nhiên, tránh gần đích hoặc người chơi."""
        valid_points = [
            (x, y) for x in range(maze.width) for y in range(maze.height)
            if not maze.is_wall(x, y) and (x, y) != goal and (x, y) != (self.grid_x, self.grid_y)
        ]
        # Lọc điểm dựa trên khoảng cách
        min_distance_to_goal = 4 if self.difficulty == "hard" else 2
        valid_points = [
            p for p in valid_points
            if abs(p[0] - goal[0]) + abs(p[1] - goal[1]) >= min_distance_to_goal
            and abs(p[0] - player_pos[0]) + abs(p[1] - player_pos[1]) >= 2
        ]
        return random.choice(valid_points) if valid_points else None

    def calculate_path(self, maze, player_pos=None):
        """Tính toán đường đi đến điểm trung gian hoặc đích."""
        current_pos = (self.grid_x, self.grid_y)
        goal = maze.end_pos

        # Nếu đã ở đích, xóa đường đi
        if current_pos == goal:
            self.path = []
            self.path_index = 0
            self.target = None
            return

        # Kiểm tra khoảng cách đến đích
        bot_dist = abs(current_pos[0] - goal[0]) + abs(current_pos[1] - goal[1])
        player_dist = abs(player_pos[0] - goal[0]) + abs(player_pos[1] - goal[1]) if player_pos else float('inf')

        # Quyết định mục tiêu dựa trên độ khó và vị trí người chơi
        if self.difficulty == "hard" or player_dist < bot_dist * 0.8:
            self.target = goal  # Đi thẳng đến đích
            self.update_rate = 8
        elif not self.target or current_pos == self.target or random.random() < 0.1:
            # Chọn điểm trung gian mới nếu chưa có, đã đến điểm hiện tại, hoặc ngẫu nhiên
            self.target = self._get_random_waypoint(maze, goal, player_pos) or goal
        # Nếu mục tiêu là đích, có xác suất chọn lại điểm trung gian
        elif self.target == goal and random.random() < 0.3 and self.difficulty != "hard":
            self.target = self._get_random_waypoint(maze, goal, player_pos) or goal

        # Tính đường đi đến mục tiêu
        self.path = self._bfs(maze, current_pos, self.target)
        self.path_index = 0
        print(f"AI target: {self.target}, Path length: {len(self.path)}")

    def update(self, maze, player_pos=None):
        """Cập nhật vị trí AI dựa trên đường đi và trạng thái."""
        now = pygame.time.get_ticks()

        # Xử lý chế độ đóng băng ở hard
        if self.difficulty == "hard":
            if not self.hard_freezing and now - self.last_freeze_cycle_tick >= 10000:
                self.hard_freezing = True
                self.freeze_start_tick = now
            if self.hard_freezing:
                if now - self.freeze_start_tick < 1000:
                    return
                self.hard_freezing = False
                self.last_freeze_cycle_tick = now

        # Xử lý trạng thái do dự (hesitation) để đánh lừa
        if self.is_hesitating:
            self.hesitation_timer += 1
            if self.hesitation_timer >= self.hesitation_duration:
                self.is_hesitating = False
                self.hesitation_timer = 0
            return

        # Thỉnh thoảng giả vờ do dự (trừ chế độ hard)
        if self.difficulty != "hard" and random.random() < 0.05 and not self.is_hesitating:
            self.is_hesitating = True
            self.hesitation_timer = 0
            return

        # Tăng bộ đếm
        self.move_timer += 1
        self.recalculate_counter += 1

        # Tính lại đường đi định kỳ hoặc khi cần
        if self.recalculate_counter >= 60 or not self.path or (self.path_index >= len(self.path)):
            self.calculate_path(maze, player_pos)
            self.recalculate_counter = 0

        # Chỉ di chuyển khi đủ thời gian
        if self.move_timer < self.update_rate:
            return

        # Reset bộ đếm thời gian
        self.move_timer = 0

        # Di chuyển theo đường đi
        if self.path and self.path_index < len(self.path):
            next_x, next_y = self.path[self.path_index]
            self.dx = 1 if next_x > self.grid_x else (-1 if next_x < self.grid_x else 0)
            self.dy = 1 if next_y > self.grid_y else (-1 if next_y < self.grid_y else 0)
            self.grid_x = next_x
            self.grid_y = next_y
            self.x = next_x * CELL_SIZE + CELL_SIZE // 2
            self.y = next_y * CELL_SIZE + CELL_SIZE // 2
            self.path_index += 1

    def draw(self, screen, offset_x=0, offset_y=0):
        """Vẽ AI và điểm trung gian (để debug)."""
        super().draw(screen, offset_x, offset_y)
        
        # Vẽ điểm trung gian nếu có (chỉ để debug)
        if self.target and True:  # Đổi False thành True để debug
            tx, ty = self.target
            pygame.draw.circle(
                screen, (255, 255, 0),
                (offset_x + tx * CELL_SIZE + CELL_SIZE // 2, offset_y + ty * CELL_SIZE + CELL_SIZE // 2),
                5
            )