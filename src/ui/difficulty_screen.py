import pygame
from ui.screen import Screen
from ui.button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE

class DifficultyScreen(Screen):
    """
    Màn hình chọn độ khó: Easy, Medium, Hard.
    """
    def __init__(self, manager):
        super().__init__(manager)
        btn_w, btn_h = 200, 50
        x = SCREEN_WIDTH // 2 - btn_w // 2
        y0 = 200
        self.easy_btn = Button(x, y0, btn_w, btn_h, "Easy", (100,150,200), (130,180,230))
        self.med_btn = Button(x, y0+70, btn_w, btn_h, "Medium", (100,200,150), (130,230,180))
        self.hard_btn = Button(x, y0+140, btn_w, btn_h, "Hard", (200,100,150), (230,130,180))
        self.font = pygame.font.SysFont(None, 48)
        # Back button to return to main menu
        self.back_button = Button(20, 20, 100, 40, "Back", (150,150,150), (200,200,200))

    def enter(self): pass
    def exit(self): pass

    def update(self, events):
        mpos = pygame.mouse.get_pos()
        clicked = False
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                clicked = True
        # back button
        self.back_button.check_hover(mpos)
        if self.back_button.is_clicked(mpos, clicked):
            self.manager.change_state("menu")
            return
        # hover
        for btn in (self.easy_btn, self.med_btn, self.hard_btn):
            btn.check_hover(mpos)
        # clicks
        if self.easy_btn.is_clicked(mpos, clicked):
            self.manager.difficulty = "easy"
            self.manager.change_state("game")
        if self.med_btn.is_clicked(mpos, clicked):
            self.manager.difficulty = "medium"
            self.manager.change_state("game")
        if self.hard_btn.is_clicked(mpos, clicked):
            self.manager.difficulty = "hard"
            self.manager.change_state("game")

    def draw(self):
        self.screen.fill((40,40,80))
        # title
        surf = self.font.render("Select Difficulty", True, WHITE)
        rect = surf.get_rect(center=(SCREEN_WIDTH//2, 120))
        self.screen.blit(surf, rect)
        # buttons
        self.back_button.draw(self.screen)
        self.easy_btn.draw(self.screen)
        self.med_btn.draw(self.screen)
        self.hard_btn.draw(self.screen)