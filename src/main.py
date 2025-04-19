from logging import config
import pygame
import sys
from game.game_manager import GameManager
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE,FPS

def main():
    # Khởi tạo pygame
    pygame.init()
    pygame.display.set_caption(TITLE)
    
    # Tạo cửa sổ game
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Khởi tạo game manager
    game_manager = GameManager(screen)
    
    # Clock để kiểm soát FPS
    clock = pygame.time.Clock()
    pygame.mixer.init()
    # Vòng lặp game chính
    while True:
        # Xử lý các sự kiện
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Cập nhật trạng thái game
        game_manager.update(events)
        
        # Vẽ màn hình
        game_manager.draw()
        
        # Cập nhật màn hình
        pygame.display.flip()
        
        # Giới hạn FPS
        clock.tick(60)

if __name__ == "__main__":
    main()