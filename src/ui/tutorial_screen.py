import pygame
from ui.screen import Screen
from ui.button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE

class TutorialScreen(Screen):
    def __init__(self, manager):
        super().__init__(manager)
        self.back_button = Button(
            20, 20, 120, 40, "Back", (200,200,200), (230,230,230)
        )
        self.font = pygame.font.SysFont("Times New Roman", 28)
        self.lines = [
          "Điều khiển:",
          "- W  or  ↑: Di chuyển lên trên",
          "- A  or  ←: Di chuyển sang trái",
          "- S  or  ↓: Di chuyển xuống dưới",
          "- D  or  →: Di chuyển sang phải",
          "",
          "Luật chơi:",
          "- Cố gắng tìm đường đến đích bằng cách di chuyển hợp lý để có thể lấy được kho báu của mê cung.",
          "- Bạn không thể đi qua tường.",
          "- Nhấn Q để tìm kiếm sự trợ giúp.",
          "- Màn chơi 1 người: Bạn sẽ chơi một mình và cố gắng tìm đường đến đích trong thời gian nhất định.",
          "- Màn chơi 2 người: Bạn sẽ chơi với một người khác và cố gắng tìm đường đến đích trước họ.",
          "- Màn chơi với máy: Bạn sẽ chơi với một AI và cố gắng tìm đường đến đích trước nó.",
          "- Nhấn ESC để tạm dừng game.",
        ]
    
    def enter(self): pass
    def exit(self): pass

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.back_button.is_clicked(pygame.mouse.get_pos(), True):
                    self.manager.change_state("menu")
        self.back_button.check_hover(mouse_pos)

    def draw(self):
        self.screen.fill((30,30,60))
        for i, line in enumerate(self.lines):
            surf = self.font.render(line, True, WHITE)
            self.screen.blit(surf, (50, 80 + i*30))
        self.back_button.draw(self.screen)