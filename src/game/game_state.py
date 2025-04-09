class GameState:
    """
    Lớp cơ sở cho các trạng thái game khác nhau.
    Mỗi trạng thái (menu, gameplay, pause, ...) sẽ kế thừa từ lớp này.
    """
    
    def __init__(self, manager):
        """
        Khởi tạo trạng thái game.
        
        Args:
            manager: Game Manager quản lý các trạng thái
        """
        self.manager = manager
    
    def enter(self):
        """
        Được gọi khi trạng thái bắt đầu.
        """
        pass
    
    def exit(self):
        """
        Được gọi khi thoát khỏi trạng thái.
        """
        pass
    
    def update(self, events):
        """
        Cập nhật trạng thái dựa trên sự kiện đầu vào.
        
        Args:
            events: Danh sách các sự kiện pygame
        """
        pass
    
    def draw(self):
        """
        Vẽ trạng thái lên màn hình.
        """
        pass