from game.game_state import GameState

class Screen(GameState):
    """
    Lớp cơ sở cho các màn hình trong game.
    Kế thừa từ GameState và cung cấp chức năng chung cho các màn hình.
    """
    
    def __init__(self, manager):
        """
        Khởi tạo màn hình.
        
        Args:
            manager: Game Manager quản lý các trạng thái
        """
        super().__init__(manager)
        self.screen = manager.screen