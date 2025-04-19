from maze.maze import Maze

class MazeGenerator:
    """
    Lớp cơ sở cho tất cả các thuật toán tạo mê cung.
    Phương thức generate() tạo mê cung mặc định nếu không được ghi đè.
    """
    
    def generate(self, width, height):
        """
        Tạo một mê cung mặc định là toàn tường.
        Chỉ có điểm bắt đầu và điểm kết thúc là đường đi.
        
        Args:
            width (int): Số ô theo chiều ngang
            height (int): Số ô theo chiều dọc
        
        Returns:
            Maze: Đối tượng mê cung đã được tạo
        """
        # Khởi tạo mê cung (tất cả là tường)
        maze = self._init_grid(width, height)
        
        # Thiết lập điểm bắt đầu và kết thúc
        start_x, start_y = 0, 0
        end_x, end_y = width - 1, height - 1
        
        # Đặt điểm bắt đầu và kết thúc là đường đi
        maze.set_cell(start_x, start_y, False)  # Điểm bắt đầu là đường đi
        maze.set_cell(end_x, end_y, False)      # Điểm kết thúc là đường đi
        
        # Thiết lập vị trí bắt đầu và kết thúc
        self._set_start_end(maze)
        
        return maze
    
    def _init_grid(self, width, height):
        """
        Khởi tạo mê cung trống (tất cả đều là tường).
        
        Args:
            width (int): Số ô theo chiều ngang
            height (int): Số ô theo chiều dọc
        
        Returns:
            Maze: Mê cung mới
        """
        maze = Maze(width, height)
        return maze
    
    # Thêm vào phương thức generate trong các generator để đảm bảo có đường đi
    def _set_start_end(self, maze):
        """
        Thiết lập vị trí bắt đầu và kết thúc cho mê cung.
        Đảm bảo các vị trí này là đường đi.
        
        Args:
            maze (Maze): Mê cung cần thiết lập
        """
        start_x, start_y = 0, 0
        end_x, end_y = maze.width - 1, maze.height - 1
        
        # Đảm bảo vị trí bắt đầu và kết thúc là đường đi
        maze.set_cell(start_x, start_y, False)
        maze.set_cell(end_x, end_y, False)
        
        maze.set_start(start_x, start_y)
        maze.set_end(end_x, end_y)