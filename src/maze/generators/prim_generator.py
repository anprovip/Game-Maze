import random
from maze.generators.base_generator import MazeGenerator

class PrimGenerator(MazeGenerator):
    """
    Tạo mê cung sử dụng thuật toán Prim.
    Mê cung tạo ra sẽ không có vòng lặp (là cây khung).
    """
    
    def generate(self, width, height):
        """
        Tạo mê cung bằng thuật toán Prim.
        
        Args:
            width (int): Số ô theo chiều ngang
            height (int): Số ô theo chiều dọc
        
        Returns:
            Maze: Mê cung đã được tạo
        """
        # Khởi tạo mê cung toàn tường
        maze = self._init_grid(width, height)
        
        # Bắt đầu từ một ô ngẫu nhiên
        start_x, start_y = random.randint(0, width // 2) * 2, random.randint(0, height // 2) * 2
        maze.set_cell(start_x, start_y, False)
        
        # Danh sách các cạnh tiềm năng
        walls = self._get_neighbors(start_x, start_y, maze)
        
        # Tiến hành mở rộng mê cung
        while walls:
            # Chọn một cạnh ngẫu nhiên
            wx, wy, nx, ny = random.choice(walls)
            
            # Kiểm tra nếu ô tiếp theo là tường (chưa được mở rộng)
            if maze.is_wall(nx, ny):
                # Mở rộng mê cung
                maze.set_cell(nx, ny, False)
                maze.set_cell(wx, wy, False)
                
                # Thêm các cạnh xung quanh ô mới vào danh sách các cạnh tiềm năng
                walls.extend(self._get_neighbors(nx, ny, maze))
            
            # Loại bỏ cạnh đã xử lý
            walls.remove((wx, wy, nx, ny))
        
        # Thiết lập vị trí bắt đầu và kết thúc
        self._set_start_end(maze)
        
        return maze
    
    def _get_neighbors(self, x, y, maze):
        """
        Lấy các ô lân cận chưa được khai phá quanh ô (x, y).
        
        Args:
            x (int): Tọa độ x
            y (int): Tọa độ y
            maze (Maze): Mê cung
        
        Returns:
            list: Danh sách các cạnh tiềm năng dưới dạng (wx, wy, nx, ny)
        """
        neighbors = []
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]  # Lên, phải, xuống, trái
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            wx, wy = x + dx // 2, y + dy // 2
            
            if 0 <= nx < maze.width and 0 <= ny < maze.height and maze.is_wall(nx, ny):
                neighbors.append((wx, wy, nx, ny))
        
        return neighbors
