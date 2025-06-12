import random
import pygame
# import config
import time
import json
import os
import sys
from grid import Grid
from blocks import *
from colors import *


class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.level = 1  # 1: Easy, 2: Medium, 3: Hard
        self.fall_speed = {1: 500, 2: 300, 3: 150}  # milliseconds between auto-moves
        self.score_multiplier = {1: 1, 2: 1.5, 3: 2}
        pygame.init()            # Initialise tous les modules Pygame
        pygame.mixer.init()      # ✅ Initialise le mixer (son)

        # Charge le son maintenant que le mixer est prêt
        self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")

        pygame.mixer.music.load("Sounds/music.ogg")
        pygame.mixer.music.play(-1)


    def set_level(self, level):
        """Set difficulty level (1-3)"""
        if level in [1, 2, 3]:
            self.level = level
            return True
        return False

    def update_score(self, lines_cleared, move_down_points):
        base_points = 0
        if lines_cleared == 1:
            base_points = 100
        elif lines_cleared == 2:
            base_points = 300
        elif lines_cleared == 3:
            base_points = 500

        # Apply level multiplier
        multiplied_points = int(base_points * self.score_multiplier[self.level])
        self.score += multiplied_points + move_down_points

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
        if self.block_fits() == False:
            self.game_over = True

    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
        else:
            self.rotate_sound.play()

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)

        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270)

        # Draw level indicator
        title_font = pygame.font.Font(None, 40)
        level_names = {1: "Easy", 2: "Medium", 3: "Hard"}
        level_text = level_names.get(self.level, "Unknown")
        level_surface = title_font.render(f"Level: {level_text}", True, Colors.white)
        screen.blit(level_surface, (365, 400))



