from maze.maze import Maze

class MazeGenerator:
    """
    Lớp cơ sở cho tất cả các thuật toán tạo mê cung.
    Các lớp con cần triển khai phương thức generate().
    """
    
    def generate(self, width, height):
        """
        Tạo một mê cung với kích thước cho trước.
        
        Args:
            width (int): Số ô theo chiều ngang
            height (int): Số ô theo chiều dọc
        
        Returns:
            Maze: Đối tượng mê cung đã được tạo
        """
        raise NotImplementedError("Các lớp con phải triển khai phương thức này")
    
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
    
    def _set_start_end(self, maze):
        """
        Thiết lập vị trí bắt đầu và kết thúc cho mê cung.
        Mặc định: Bắt đầu ở góc trên bên trái, kết thúc ở góc dưới bên phải.
        
        Args:
            maze (Maze): Mê cung cần thiết lập
        """
        maze.set_start(0, 0)
        maze.set_end(maze.width - 1, maze.height - 1)