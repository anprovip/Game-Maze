import random
from maze.generators.base_generator import MazeGenerator

class DFSGenerator(MazeGenerator):
    """
    Tạo mê cung sử dụng thuật toán Depth-First Search (DFS).
    Mê cung tạo ra sẽ không có vòng lặp (là cây khung).
    """
    
    def generate(self, width, height):
        """
        Tạo mê cung bằng thuật toán DFS.
        
        Args:
            width (int): Số ô theo chiều ngang
            height (int): Số ô theo chiều dọc
        
        Returns:
            Maze: Mê cung đã được tạo
        """
        # Khởi tạo mê cung toàn tường
        maze = self._init_grid(width, height)
        
        # Thực hiện DFS để đào đường đi
        self._carve_passages(maze, 0, 0)
        
        # Thiết lập vị trí bắt đầu và kết thúc
        self._set_start_end(maze)
        
        return maze
    
    def _carve_passages(self, maze, x, y):
        """
        Đào đường đi trong mê cung bằng thuật toán DFS.
        
        Args:
            maze (Maze): Mê cung
            x (int): Tọa độ x hiện tại
            y (int): Tọa độ y hiện tại
        """
        # Đánh dấu ô hiện tại là đường đi
        maze.set_cell(x, y, False)
        
        # Xác định các hướng di chuyển ngẫu nhiên
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]  # Lên, phải, xuống, trái
        random.shuffle(directions)
        
        # Xét từng hướng
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Kiểm tra ô tiếp theo có trong mê cung không
            if 0 <= nx < maze.width and 0 <= ny < maze.height and maze.is_wall(nx, ny):
                # Đào tường ở giữa
                maze.set_cell(x + dx//2, y + dy//2, False)
                
                # Đệ quy sang ô tiếp theo
                self._carve_passages(maze, nx, ny)