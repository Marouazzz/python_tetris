import pygame
import sys
import json
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Signal
from game_model import GameModel
from game_view import GameView


class GameController(QObject):
    game_started = Signal()
    game_ended = Signal(int)
    pause_changed = Signal(bool)


    def __init__(self, speed, difficulty_name, username):
        super().__init__()
        pygame.mixer.init()
        try:
            pygame.mixer.music.load("assets/music/game_music.mp3")
            pygame.mixer.music.set_volume(0.5)
        except pygame.error:
            print("Could not load music file")

        self.speed = speed
        self.username = username
        self.model = None
        self.view = None
        self.running = False
        self.key_bindings = self.load_key_bindings()
        self.difficulty_name = difficulty_name
        self.GAME_UPDATE = pygame.USEREVENT + 1



    def load_key_bindings(self):
        """Load key bindings from settings.json or fallback to defaults"""
        default_bindings = {
            pygame.K_LEFT: "left",
            pygame.K_RIGHT: "right",
            pygame.K_UP: "rotate",
            pygame.K_DOWN: "down",
            pygame.K_SPACE: "drop",
            pygame.K_p: "pause",
            pygame.K_r: "restart"
        }

        try:
            with open("settings.json", "r") as f:
                config = json.load(f)
                controls = config.get("controls", {})

                return {
                    pygame.K_LEFT: controls.get("left", "left"),
                    pygame.K_RIGHT: controls.get("right", "right"),
                    pygame.K_UP: controls.get("rotate", "rotate"),
                    pygame.K_DOWN: "down",  # Keep down hardcoded if not customizable
                    pygame.K_SPACE: controls.get("drop", "drop"),
                    pygame.K_p: controls.get("pause", "pause"),
                    pygame.K_r: "restart"
                }
        except Exception as e:
            print(f"Error loading settings: {e}")
            return default_bindings

    def start_game(self, player_name=None):
        name_to_use = player_name if player_name is not None else self.username
        self.model = GameModel(self.difficulty_name, name_to_use)
        self.model.base_speed = self.speed
        self.model.current_speed = self.speed
        self.view = GameView()
        self.running = True
        self.game_loop()

    def handle_key_press(self, key):
        self.model.paused = False
        if key not in self.key_bindings:
            return

        action = self.key_bindings[key]
        print(f"Key pressed: {key}, mapped action: {action}")  # Debug

        if self.model.game_over:
            if action == "restart":
                self.model.reset()
        elif action == "pause":
            self.model.paused = not self.model.paused
            self.pause_changed.emit(self.model.paused)
        elif not self.model.paused:
            if action == "left":
                self.model.move_left()
            elif action == "right":
                self.model.move_right()
            elif action == "down":
                self.model.move_down()
                self.model.update_score(0, 1)
            elif action == "rotate":
                self.model.rotate()
            elif action == "drop":
                while not self.model.game_over and self.model.block_fits():
                    self.model.move_down()
                    self.model.update_score(0, 2)

    def game_loop(self):
        clock = pygame.time.Clock()
        last_update = pygame.time.get_ticks()
        key_repeat_delay = 200
        key_repeat_interval = 100
        last_key_press = {}

        self.game_started.emit()

        while self.running:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and self.model.paused:
                    mouse_pos = event.pos
                    resume_rect, exit_rect = self.view.draw_pause_menu()
                    if resume_rect.collidepoint(mouse_pos):
                        self.model.paused = False
                        self.pause_changed.emit(False)
                    elif exit_rect.collidepoint(mouse_pos):
                        self.running = False

                if event.type == pygame.KEYDOWN:
                    self.handle_key_press(event.key)
                    last_key_press[event.key] = current_time


            if not self.model.game_over and not self.model.paused:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_LEFT]:
                    if (pygame.K_LEFT not in last_key_press or
                            current_time - last_key_press[pygame.K_LEFT] >= key_repeat_delay):
                        self.model.move_left()
                        last_key_press[pygame.K_LEFT] = current_time - key_repeat_delay + key_repeat_interval

                if keys[pygame.K_RIGHT]:
                    if (pygame.K_RIGHT not in last_key_press or
                            current_time - last_key_press[pygame.K_RIGHT] >= key_repeat_delay):
                        self.model.move_right()
                        last_key_press[pygame.K_RIGHT] = current_time - key_repeat_delay + key_repeat_interval

                if keys[pygame.K_DOWN]:
                    if (pygame.K_DOWN not in last_key_press or
                            current_time - last_key_press[pygame.K_DOWN] >= key_repeat_delay // 2):
                        self.model.move_down()
                        self.model.update_score(0, 1)
                        last_key_press[pygame.K_DOWN] = current_time - key_repeat_delay + key_repeat_interval // 2
                if keys[pygame.K_UP]:
                    if (pygame.K_UP not in last_key_press or
                            current_time - last_key_press[pygame.K_UP] >= key_repeat_delay):
                        self.model.rotate()
                        last_key_press[pygame.K_UP] = current_time - key_repeat_delay + key_repeat_interval

            if not self.model.game_over and not self.model.paused:
                if current_time - last_update >= self.model.current_speed:
                    self.model.move_down()
                    last_update = current_time

            if self.model.paused:
                resume_rect, exit_rect = self.view.draw(self.model)
                mouse_pos = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    if resume_rect and resume_rect.collidepoint(mouse_pos):
                        self.model.paused = False
                    elif exit_rect and exit_rect.collidepoint(mouse_pos):
                        return False

            self.view.draw(self.model)

            if self.model.game_over:
                self.game_ended.emit(self.model.score)


            clock.tick(60)

        self.view.close()
        pygame.mixer.music.stop()
        pygame.quit()
