from maze.generators.kruskal_generator import KruskalGenerator
from config import DEFAULT_MAZE_WIDTH, DEFAULT_MAZE_HEIGHT
from maze.generators.dfs_generator import DFSGenerator
from maze.generators.prim_generator import PrimGenerator


class Level:
    """
    Quản lý cấp độ trong game, bao gồm kích thước mê cung và độ khó.
    """
    
    def __init__(self, level_number=1):
        """
        Khởi tạo cấp độ.
        
        Args:
            level_number (int): Số cấp độ
        """
        self.level_number = level_number
        self.maze_width, self.maze_height = self._get_size_for_level()
        
        # Khởi tạo các thuật toán tạo mê cung
        self.maze_generators = {
            "kruskal": KruskalGenerator(),
            "dfs": DFSGenerator(),
            "prim": PrimGenerator(),
       
        }
    
    def _get_size_for_level(self):
        """
        Xác định kích thước mê cung dựa trên cấp độ.
        
        Returns:
            tuple: (width, height) - Kích thước mê cung
        """
        # Cấp độ càng cao, mê cung càng lớn
        base_width = DEFAULT_MAZE_WIDTH
        base_height = DEFAULT_MAZE_HEIGHT
        
        # Tăng kích thước theo cấp độ
        if self.level_number <= 1:
            return base_width, base_height
        elif self.level_number <= 3:
            return base_width + 5, base_height + 3
        elif self.level_number <= 5:
            return base_width + 10, base_height + 6
        else:
            return base_width + 15, base_height + 10
    
    def generate_maze(self, generator_type):
        """
        Tạo mê cung với thuật toán đã chọn.
        
        Args:
            generator_type (str): Loại thuật toán tạo mê cung
        
        Returns:
            Maze: Mê cung đã tạo
        """
        if generator_type in self.maze_generators:
            generator = self.maze_generators[generator_type]
            return generator.generate(self.maze_width, self.maze_height)
        else:
            # Mặc định sử dụng DFS nếu không tìm thấy thuật toán
            return self.maze_generators["dfs"].generate(self.maze_width, self.maze_height)