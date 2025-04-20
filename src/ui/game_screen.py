import pygame
import sys
import os
import random
from collections import deque
from ui.screen import Screen
from ui.button import Button
from game.level import Level
from entities.player import Player
from entities.ai_player import AIPlayer
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, RED, GREEN, BLUE, CELL_SIZE, FPS
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

class GameScreen(Screen):
    """
    Màn hình chơi game.
    """
    
    def __init__(self, manager):
        """
        Khởi tạo màn hình game.
        
        Args:
            manager: Game Manager quản lý các trạng thái
        """
        super().__init__(manager)
        self.show_hint = False
        self.hint_path = []
        self.is_paused = False
        self.show_confirm_popup = False
        
        victory_sound_path = os.path.join(project_root, 'assets', 'sounds', 'victory.mp3')
        self.victory_sound = pygame.mixer.Sound(victory_sound_path)
        # Nút quay về menu
        self.back_button = Button(
            20, 20, 100, 40, "Back", (150, 150, 150), (200, 200, 200)
        )

        # Nút tạm dừng
        self.pause_button = Button(
            130, 20, 100, 40, "Pause", (150, 150, 150), (200, 200, 200)
        )
        
        # Nút xác nhận trong pop-up
        self.confirm_return_button = Button(
            SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 20, 110, 45,
            "Return", (200, 100, 100), (255, 150, 150)
        )
        self.confirm_continue_button = Button(
            SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 20, 110, 45,
            "Continue", (100, 200, 100), (150, 255, 150)
        )
        
        # Biến game
        self.maze = None
        self.players = []
        self.current_level = None
        self.game_over = False
        self.winner = None
        
        # Font
        self.font = pygame.font.SysFont(None, 36)
        # Thống kê thời gian dừng
        self.pause_start_ticks = None

        # Animation effect list and index counter
        enum_effects = ['fade', 'flip', 'flipfade', 'wipe', 'spiral', 'shuffle', 'dissolve']
        self.anim_effects = enum_effects
        self.anim_index = 0

        # Generation direction list and index counter
        self.gen_dirs = ['vertical', 'horizontal_l2r', 'horizontal_r2l']
        self.gen_index = 0

        # Load volume toggle icons
        self.volume_img = pygame.transform.scale(
            pygame.image.load(os.path.join(project_root, 'assets', 'img', 'volume.png')),
            (40, 40)
        )
        self.mute_img = pygame.transform.scale(
            pygame.image.load(os.path.join(project_root, 'assets', 'img', 'volume-mute.png')),
            (40, 40)
        )
        self.music_btn_rect = self.volume_img.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        self.music_on = True
    
    def enter(self):
        """
        Được gọi khi chuyển sang màn hình game.
        """
        # Tạo mê cung mới cho cấp độ hiện tại
        self.current_level = Level(self.manager.level)
        self.maze = self.current_level.generate_maze(self.manager.maze_generator_type)
        
        # Lấy vị trí bắt đầu từ mê cung
        start_x, start_y = self.maze.start_pos
        
        # Khởi tạo người chơi tại vị trí bắt đầu
        self.players = []
        
        if self.manager.game_mode == "single":
            self.players.append(Player(start_x, start_y))
        elif self.manager.game_mode == "two_players":
            self.players.append(Player(start_x, start_y))
            self.players.append(Player(start_x, start_y, color=GREEN, image_path=os.path.join(project_root, 'assets', 'img', 'cat.png') ))
        elif self.manager.game_mode == "vs_ai":
            self.players.append(Player(start_x, start_y))
            # Use the selected difficulty for AI
            ai = AIPlayer(start_x, start_y, difficulty=self.manager.difficulty, image_path = os.path.join(project_root, 'assets', 'img', 'cat.png'))
            # reset freeze cycle timers
            ai.last_freeze_cycle_tick = pygame.time.get_ticks()
            ai.hard_freezing = False
            self.players.append(ai)
        
        # Biến trạng thái
        self.game_over = False
        self.winner = None
        self.show_hint = False
        self.hint_path = []
        self.is_paused = False
        self.show_confirm_popup = False
        
        # Debug: In ra cấu trúc mê cung
        print("Cấu trúc mê cung:")
        for y in range(self.maze.height):
            row = ""
            for x in range(self.maze.width):
                if (x, y) == self.maze.start_pos:
                    row += "S"
                elif (x, y) == self.maze.end_pos:
                    row += "E"
                elif self.maze.is_wall(x, y):
                    row += "#"
                else:
                    row += "."
            print(row)
        
        # Thêm khởi tạo time/step giới hạn
        self.start_ticks = pygame.time.get_ticks()
        # Tính đường ngắn nhất
        self.calculate_hint_path()
        shortest = len(self.hint_path)
        self.show_hint = False
        diff = self.manager.difficulty
        if diff == "easy":
            self.time_limit = random.randint(120, 160)
            self.step_limit = None
        elif diff == "medium":
            self.time_limit = None
            self.step_limit = shortest + 16
        else:
            self.time_limit = random.randint(90, 120)
            self.step_limit = shortest + 8
        # Bộ đếm bước
        self.step_counts = [0] * len(self.players)
        # Setup animation for maze generation
        self.final_grid = [row[:] for row in self.maze.grid]
        self.animating = True
        self.anim_frames = 0
        self.total_anim_frames = FPS * 4  # 4 seconds animation

        # Choose next effect in sequence
        self.anim_effect = self.anim_effects[self.anim_index]
        self.anim_index = (self.anim_index + 1) % len(self.anim_effects)

        # Prepare extra data for effects
        self.slide_dir = 1  # slide from left by default
        # build spiral order once
        tmp_cells = [(x, y) for y in range(self.maze.height) for x in range(self.maze.width)]
        spiral = []
        min_x, min_y, max_x, max_y = 0, 0, self.maze.width-1, self.maze.height-1
        while min_x <= max_x and min_y <= max_y:
            for x in range(min_x, max_x+1): spiral.append((x, min_y))
            for y in range(min_y+1, max_y+1): spiral.append((max_x, y))
            if min_y < max_y:
                for x in range(max_x-1, min_x-1, -1): spiral.append((x, max_y))
            if min_x < max_x:
                for y in range(max_y-1, min_y, -1): spiral.append((min_x, y))
            min_x += 1; max_x -= 1; min_y += 1; max_y -= 1
        self.spiral_order = spiral
        # shuffle rows for 'shuffle' effect
        self.row_order = list(range(self.maze.height))
        random.shuffle(self.row_order)
        # random dissolve order for 'dissolve' effect
        self.dissolve_order = random.sample(tmp_cells, len(tmp_cells))

        # Choose next generation direction in sequence
        self.gen_dir = self.gen_dirs[self.gen_index]
        self.gen_index = (self.gen_index + 1) % len(self.gen_dirs)

        # Play game background music
        bg2_path = os.path.join(project_root, 'assets', 'sounds', 'bg-2.mp3')
        pygame.mixer.music.load(bg2_path)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    
    def exit(self):
        """
        Được gọi khi thoát khỏi màn hình.
        """
        pass
    
    def calculate_hint_path(self):
        """
        Tính toán đường đi gợi ý từ vị trí người chơi đến đích bằng thuật toán BFS.
        """
        if not self.players:
            return
        
        player = self.players[0]
        start = (player.grid_x, player.grid_y)
        end = self.maze.end_pos
        
        if start == end:
            self.hint_path = []
            return
        
        queue = deque([start])
        visited = {start: None}
        
        while queue:
            x, y = queue.popleft()
            if (x, y) == end:
                break
            
            neighbors = self.maze.get_neighbors(x, y)
            for nx, ny in neighbors:
                if (nx, ny) not in visited:
                    queue.append((nx, ny))
                    visited[(nx, ny)] = (x, y)
        
        if end in visited:
            path = []
            current = end
            while current != start:
                path.append(current)
                current = visited[current]
            path.reverse()
            self.hint_path = path
        else:
            self.hint_path = []
    
    def update(self, events):
        """
        Cập nhật màn hình game dựa trên sự kiện đầu vào.
        
        Args:
            events: Danh sách các sự kiện pygame
        """
        
        # Animate maze generation
        if hasattr(self, 'animating') and self.animating:
            self.anim_frames += 1
            if self.anim_frames >= self.total_anim_frames:
                self.animating = False
            return

        if self.game_over:
            # Phát âm thanh chiến thắng nếu chưa phát
            if not hasattr(self, 'victory_sound_played') or not self.victory_sound_played:
                self.victory_sound.play()
                self.victory_sound_played = True  # Đảm bảo âm thanh chỉ phát một lần

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        self.manager.change_state("menu")
            return
                
        if self.is_paused or self.show_confirm_popup:
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = False
            
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True
            
            # Kiểm tra hover và click cho nút trong pop-up
            if self.show_confirm_popup:
                self.confirm_return_button.check_hover(mouse_pos)
                self.confirm_continue_button.check_hover(mouse_pos)
                
                if self.confirm_return_button.is_clicked(mouse_pos, mouse_clicked):
                    self.manager.change_state("menu")
                    return
                if self.confirm_continue_button.is_clicked(mouse_pos, mouse_clicked):
                    # resume from confirm popup
                    paused_dur = pygame.time.get_ticks() - self.pause_start_ticks
                    self.start_ticks += paused_dur
                    self.pause_start_ticks = None
                    self.show_confirm_popup = False
                    self.is_paused = False
            else:
                # Khi paused, nhấp bất kỳ để tiếp tục
                if mouse_clicked:
                    # resume from simple pause
                    paused_dur = pygame.time.get_ticks() - self.pause_start_ticks
                    self.start_ticks += paused_dur
                    self.pause_start_ticks = None
                    self.is_paused = False
            return
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Regenerate maze and reset players
                    self.enter()
                elif event.key == pygame.K_q and self.manager.game_mode == "single":
                    if not self.show_hint:
                        self.calculate_hint_path()
                    self.show_hint = not self.show_hint
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.music_btn_rect.collidepoint(event.pos):
                    self.music_on = not self.music_on
                    pygame.mixer.music.set_volume(0.5 if self.music_on else 0)
                    mouse_clicked = False
        
        # Kiểm tra nút pause và back
        self.pause_button.check_hover(mouse_pos)
        self.back_button.check_hover(mouse_pos)
        
        if self.pause_button.is_clicked(mouse_pos, mouse_clicked):
            if not self.is_paused:
                self.pause_start_ticks = pygame.time.get_ticks()
            self.is_paused = True
        if self.back_button.is_clicked(mouse_pos, mouse_clicked):
            if not self.is_paused:
                self.pause_start_ticks = pygame.time.get_ticks()
            self.show_confirm_popup = True
            self.is_paused = True
        
        # Xử lý đầu vào cho người chơi
        keys = pygame.key.get_pressed()
        
        # Track previous positions to count steps
        prev_positions = [(p.grid_x, p.grid_y) for p in self.players]
        
        if len(self.players) > 0:
            self.players[0].handle_input(keys, 1)
            self.players[0].update(self.maze)
            if self.players[0].is_at_end(self.maze):
                self.game_over = True
                self.winner = 0
        
        if self.show_hint and self.manager.game_mode == "single":
            self.calculate_hint_path()
        
        if len(self.players) > 1:
            if isinstance(self.players[1], AIPlayer):
                # Truyền vị trí người chơi vào update của AI
                self.players[1].update(self.maze, player_pos=(self.players[0].grid_x, self.players[0].grid_y))
            else:
                self.players[1].handle_input(keys, 2)
                self.players[1].update(self.maze)
            if self.players[1].is_at_end(self.maze):
                self.game_over = True
                self.winner = 1
                
        # Sau khi update người chơi, đếm bước
        for idx, p in enumerate(self.players):
            if (p.grid_x, p.grid_y) != prev_positions[idx]:
                self.step_counts[idx] += 1
        
        # Kiểm tra giới hạn
        elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
        if self.manager.game_mode == "single":
            if self.time_limit and elapsed > self.time_limit:
                self.game_over = True
                self.winner = None
            if self.step_limit and self.step_counts[0] > self.step_limit:
                self.game_over = True
                self.winner = None
        elif self.manager.game_mode == "two_players":
            if self.time_limit and elapsed > self.time_limit:
                if not self.players[0].is_at_end(self.maze) and not self.players[1].is_at_end(self.maze):
                    self.game_over = True
                    self.winner = None
                    self.both_timeout = True
            if self.step_limit:
                over = [cnt > self.step_limit for cnt in self.step_counts]
                if over[0] and not over[1]:
                    self.game_over = True
                    self.winner = 1
                elif over[1] and not over[0]:
                    self.game_over = True
                    self.winner = 0
                elif over[0] and over[1]:
                    self.game_over = True
                    self.winner = None
        elif self.manager.game_mode == "vs_ai":
            # Người chơi thua nếu vượt quá thời gian
            if self.time_limit and elapsed > self.time_limit:
                self.game_over = True
                self.winner = 1
            # Người chơi thua nếu vượt quá số bước
            if self.step_limit and self.step_counts[0] > self.step_limit:
                self.game_over = True
                self.winner = 1
    
    def draw(self):
        """
        Vẽ màn hình game.
        """
        # Compute positions
        maze_pixel_width = self.maze.width * CELL_SIZE
        maze_pixel_height = self.maze.height * CELL_SIZE
        offset_x = (SCREEN_WIDTH - maze_pixel_width) // 2
        offset_y = (SCREEN_HEIGHT - maze_pixel_height) // 2

        # Animate maze drawing
        if getattr(self, 'animating', False):
            self.screen.fill((50, 80, 50))
            progress = self.anim_frames / self.total_anim_frames
            h, w = self.maze.height, self.maze.width
            offx, offy = offset_x, offset_y

            if self.gen_dir == 'vertical':
                total = h; full = int(progress * total); frac = (progress*total) - full
                # draw fully revealed rows
                for y in range(full):
                    for x in range(w):
                        pos = (offx + x*CELL_SIZE, offy + y*CELL_SIZE)
                        self.screen.blit(self.maze.wall_img if self.final_grid[y][x] and (x,y)!=self.maze.end_pos else self.maze.bg_img, pos)
                # animate current row 'full'
                if full < h:
                    for x in range(w):
                        cell_pos = (offx + x*CELL_SIZE, offy + full*CELL_SIZE)
                        is_wall = self.final_grid[full][x] and (x,full)!=self.maze.end_pos
                        # existing per-cell effect code for fade/flip etc replacing base_pos with cell_pos and index x
                        if self.anim_effect == 'fade':
                            alpha = int(frac * 255)
                            img = self.maze.wall_img.copy() if is_wall else self.maze.bg_img
                            img.set_alpha(alpha)
                            self.screen.blit(img, cell_pos)
                        elif self.anim_effect == 'flip':
                            if frac < 0.5:
                                scale_h = int((1 - frac * 2) * CELL_SIZE)
                                img_base = self.maze.wall_img if is_wall else self.maze.bg_img
                            else:
                                scale_h = int((frac - 0.5) * 2 * CELL_SIZE)
                                img_base = pygame.transform.flip(self.maze.wall_img if is_wall else self.maze.bg_img, False, True)
                            if scale_h > 0:
                                temp = pygame.transform.scale(img_base, (CELL_SIZE, scale_h))
                                y_off = (CELL_SIZE - scale_h) // 2
                                self.screen.blit(temp, (cell_pos[0], cell_pos[1] + y_off))
                        else:  # 'flipfade'
                            alpha = int(frac * 255)
                            if frac < 0.5:
                                scale_h = int((1 - frac * 2) * CELL_SIZE)
                                img_base = self.maze.wall_img if is_wall else self.maze.bg_img
                            else:
                                scale_h = int((frac - 0.5) * 2 * CELL_SIZE)
                                img_base = pygame.transform.flip(self.maze.wall_img if is_wall else self.maze.bg_img, False, True)
                            if scale_h > 0:
                                temp = pygame.transform.scale(img_base, (CELL_SIZE, scale_h))
                                temp.set_alpha(alpha)
                                y_off = (CELL_SIZE - scale_h) // 2
                                self.screen.blit(temp, (cell_pos[0], cell_pos[1] + y_off))
                return
            else:
                total = w; full = int(progress * total); frac = (progress*total) - full
                # determine revealed and current column
                if self.gen_dir == 'horizontal_l2r':
                    reveal_cond = lambda x: x < full
                    current_col = full if full < w else None
                else:  # horizontal_r2l
                    reveal_cond = lambda x: x >= w-full
                    current_col = w-full-1 if full < w else None
                for y in range(h):
                    for x in range(w):
                        pos = (offx + x*CELL_SIZE, offy + y*CELL_SIZE)
                        if reveal_cond(x):
                            self.screen.blit(self.maze.wall_img if self.final_grid[y][x] and (x,y)!=self.maze.end_pos else self.maze.bg_img, pos)
                        elif x == current_col:
                            cell_pos = pos; is_wall = self.final_grid[y][x] and (x,y)!=self.maze.end_pos
                            # existing per-cell effect code for fade/flip etc using frac, cell_pos
                            if self.anim_effect == 'fade':
                                alpha = int(frac * 255)
                                img = self.maze.wall_img.copy() if is_wall else self.maze.bg_img
                                img.set_alpha(alpha)
                                self.screen.blit(img, cell_pos)
                            elif self.anim_effect == 'flip':
                                if frac < 0.5:
                                    scale_h = int((1 - frac * 2) * CELL_SIZE)
                                    img_base = self.maze.wall_img if is_wall else self.maze.bg_img
                                else:
                                    scale_h = int((frac - 0.5) * 2 * CELL_SIZE)
                                    img_base = pygame.transform.flip(self.maze.wall_img if is_wall else self.maze.bg_img, False, True)
                                if scale_h > 0:
                                    temp = pygame.transform.scale(img_base, (CELL_SIZE, scale_h))
                                    y_off = (CELL_SIZE - scale_h) // 2
                                    self.screen.blit(temp, (cell_pos[0], cell_pos[1] + y_off))
                            else:  # 'flipfade'
                                alpha = int(frac * 255)
                                if frac < 0.5:
                                    scale_h = int((1 - frac * 2) * CELL_SIZE)
                                    img_base = self.maze.wall_img if is_wall else self.maze.bg_img
                                else:
                                    scale_h = int((frac - 0.5) * 2 * CELL_SIZE)
                                    img_base = pygame.transform.flip(self.maze.wall_img if is_wall else self.maze.bg_img, False, True)
                                if scale_h > 0:
                                    temp = pygame.transform.scale(img_base, (CELL_SIZE, scale_h))
                                    temp.set_alpha(alpha)
                                    y_off = (CELL_SIZE - scale_h) // 2
                                    self.screen.blit(temp, (cell_pos[0], cell_pos[1] + y_off))
                        else:
                            self.screen.blit(self.maze.bg_img, pos)
                return

        self.screen.fill((50, 80, 50))
        
        self.maze.draw(self.screen, offset_x, offset_y)
        
        if self.show_hint and self.hint_path:
            for i, (x, y) in enumerate(self.hint_path):
                center_x = offset_x + x * CELL_SIZE + CELL_SIZE // 2
                center_y = offset_y + y * CELL_SIZE + CELL_SIZE // 2
                radius = CELL_SIZE // 6
                color_value = 255 - min(200, 10 * i)
                pygame.draw.circle(self.screen, (0, color_value, 0), (center_x, center_y), radius)
        
        for player in self.players:
            player.draw(self.screen, offset_x, offset_y)
        
        if self.manager.game_mode == "single":
            hint_text = "Press Q for hint" if not self.show_hint else "Press Q to hide"
            hint_surface = self.font.render(hint_text, True, WHITE)
            self.screen.blit(hint_surface, (SCREEN_WIDTH - 220, 20))
        
        self.pause_button.draw(self.screen)
        self.back_button.draw(self.screen)
        
        if self.is_paused and not self.show_confirm_popup:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))
            
            text_surface = self.font.render("Click anywhere to continue", True, WHITE)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)
        
        if self.show_confirm_popup:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))
            
            popup_surface = pygame.Surface((400, 150))
            popup_surface.fill((50, 50, 50))
            popup_rect = popup_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(popup_surface, popup_rect)
            
            text_surface = self.font.render("Return to menu?", True, WHITE)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(text_surface, text_rect)
            
            self.confirm_return_button.draw(self.screen)
            self.confirm_continue_button.draw(self.screen)
        
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))
            
            if self.winner is not None:
                if self.manager.game_mode == "vs_ai":
                    win_text = "You win!" if self.winner == 0 else "AI wins!"
                else:
                    win_text = f"Player {self.winner + 1} wins!"
                
                text_surface = self.font.render(win_text, True, WHITE)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
                self.screen.blit(text_surface, text_rect)
            
            if getattr(self, 'both_timeout', False):
                msg = self.font.render("Time Out! Both players lose. No players win.", True, WHITE)
                rect = msg.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
                self.screen.blit(msg, rect)
            
            hint_surface = self.font.render("Press Enter to return to menu", True, WHITE)
            hint_rect = hint_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(hint_surface, hint_rect)

        # calculate elapsed seconds for time display
        # Tính thời gian đã trôi qua, xem xét trạng thái tạm dừng
        if self.is_paused or self.show_confirm_popup:
            # Nếu đang tạm dừng, sử dụng thời điểm bắt đầu tạm dừng để tính
            elapsed = (self.pause_start_ticks - self.start_ticks) / 1000
        else:
            # Nếu đang chơi bình thường, tính thời gian hiện tại
            elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000

        if self.time_limit is not None:
            t = max(0, self.time_limit - elapsed)
            surf = self.font.render(f"Time: {t:.0f}s", True, WHITE)
            self.screen.blit(surf, (400, 60))
        if self.step_limit is not None:
            if self.manager.game_mode == "two_players":
                # Steps for both players
                surf1 = self.font.render(f"P1 Steps: {self.step_counts[0]}/{self.step_limit}", True, WHITE)
                surf2 = self.font.render(f"P2 Steps: {self.step_counts[1]}/{self.step_limit}", True, WHITE)
                self.screen.blit(surf1, (600, 60))
                self.screen.blit(surf2, (800, 60))
            else:
                # Single or VS AI shows only first counter
                surf = self.font.render(f"Steps: {self.step_counts[0]}/{self.step_limit}", True, WHITE)
                self.screen.blit(surf, (600, 60))
            
        # Thông báo regenerate maze
        text = self.font.render("Press R to regenerate the whole maze", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        self.screen.blit(text, text_rect)

        # Draw music toggle icon
        icon = self.volume_img if self.music_on else self.mute_img
        self.screen.blit(icon, self.music_btn_rect)