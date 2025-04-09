import pygame
from config import WHITE, BLACK, GRAY

class Button:
    """
    Lớp đại diện cho nút bấm trong giao diện người dùng.
    """
    
    def __init__(self, x, y, width, height, text, color=(200, 200, 200), hover_color=(220, 220, 220), text_color=BLACK):
        """
        Khởi tạo nút bấm.
        
        Args:
            x (int): Tọa độ x của góc trên bên trái
            y (int): Tọa độ y của góc trên bên trái
            width (int): Chiều rộng của nút
            height (int): Chiều cao của nút
            text (str): Chữ hiển thị trên nút
            color (tuple): Màu nền của nút (R, G, B)
            hover_color (tuple): Màu nền khi di chuột qua (R, G, B)
            text_color (tuple): Màu chữ (R, G, B)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
        # Font cho text
        self.font = pygame.font.SysFont(None, 32)
    
    def draw(self, screen):
        """
        Vẽ nút lên màn hình.
        
        Args:
            screen: Bề mặt pygame để vẽ
        """
        # Chọn màu phù hợp
        current_color = self.hover_color if self.is_hovered else self.color
        
        # Vẽ nút
        pygame.draw.rect(screen, current_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=5)  # Viền
        
        # Vẽ text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, mouse_pos):
        """
        Kiểm tra xem chuột có đang di chuyển qua nút không.
        
        Args:
            mouse_pos (tuple): Vị trí chuột (x, y)
        
        Returns:
            bool: True nếu chuột đang di chuyển qua nút
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
    
    def is_clicked(self, mouse_pos, mouse_clicked):
        """
        Kiểm tra xem nút có được nhấn không.
        
        Args:
            mouse_pos (tuple): Vị trí chuột (x, y)
            mouse_clicked (bool): True nếu chuột được nhấn
        
        Returns:
            bool: True nếu nút được nhấn
        """
        return self.rect.collidepoint(mouse_pos) and mouse_clicked