import random
from maze.generators.base_generator import MazeGenerator

class KruskalGenerator(MazeGenerator):
    """
    Tạo mê cung sử dụng thuật toán Kruskal.
    Mê cung tạo ra sẽ không có vòng lặp (là cây khung).
    """
    
    def generate(self, width, height):
        """
        Tạo mê cung bằng thuật toán Kruskal.
        
        Args:
            width (int): Số ô theo chiều ngang
            height (int): Số ô theo chiều dọc
        
        Returns:
            Maze: Mê cung đã được tạo
        """
        # Khởi tạo mê cung toàn tường
        maze = self._init_grid(width, height)
        
        # Thực hiện Kruskal để đào đường đi
        self._kruskal_algorithm(maze, width, height)
        
        # Thiết lập vị trí bắt đầu và kết thúc
        self._set_start_end(maze)
        
        return maze
    
    def _kruskal_algorithm(self, maze, width, height):
        """
        Đào đường đi trong mê cung bằng thuật toán Kruskal.
        
        Args:
            maze (Maze): Mê cung
            width (int): Chiều rộng mê cung
            height (int): Chiều cao mê cung
        """
        # Danh sách tất cả các tường giữa các ô (là các cạnh trong đồ thị)
        walls = []
        
        # Thu thập tất cả các tường
        for y in range(0, height, 2):
            for x in range(0, width, 2):
                # Mỗi ô cách nhau 2 đơn vị vì ở giữa là tường
                # Tường bên phải
                if x + 2 < width:
                    walls.append(((x, y), (x + 2, y)))
                # Tường bên dưới
                if y + 2 < height:
                    walls.append(((x, y), (x, y + 2)))
        
        # Xáo trộn danh sách tường để chọn ngẫu nhiên
        random.shuffle(walls)
        
        # Cấu trúc dữ liệu Union-Find để kiểm tra chu trình
        # Mỗi ô ban đầu là một tập hợp riêng biệt
        sets = {}
        for y in range(0, height, 2):
            for x in range(0, width, 2):
                sets[(x, y)] = (x, y)
        
        # Tạo các ô trống (đường đi)
        for y in range(0, height, 2):
            for x in range(0, width, 2):
                maze.set_cell(x, y, False)
        
        # Hàm tìm đại diện của tập hợp (với nén đường dẫn)
        def find(cell):
            if sets[cell] != cell:
                sets[cell] = find(sets[cell])
            return sets[cell]
        
        # Hàm hợp nhất hai tập hợp
        def union(cell1, cell2):
            sets[find(cell1)] = find(cell2)
        
        # Xử lý từng tường
        for (x1, y1), (x2, y2) in walls:
            # Nếu hai ô không thuộc cùng một tập hợp (không tạo chu trình)
            if find((x1, y1)) != find((x2, y2)):
                # Loại bỏ tường giữa hai ô
                wall_x = (x1 + x2) // 2
                wall_y = (y1 + y2) // 2
                maze.set_cell(wall_x, wall_y, False)
                
                # Hợp nhất hai tập hợp
                union((x1, y1), (x2, y2))