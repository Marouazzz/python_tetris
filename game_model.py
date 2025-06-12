import random
import pygame
import json
import os
import datetime
from grid import Grid
from game import Game
from blocks import *

class GameModel:
    LEVEL_THRESHOLDS = [0, 10, 20, 30, 40]  # Lines cleared to reach each level
    # Update these constants
    DIFFICULTY_SPEEDS = {
        "Easy": 800,    # Slowest speed
        "Medium": 400,   # Medium speed
        "Hard": 200     # Fastest starting speed
    }

    # Speed decreases by this percentage each level (making the game faster)
    SPEED_DECREMENT = 0.05  # 5% faster each level

    def __init__(self, difficulty="Medium", player_name="Guest", user_id=None):
        self.game = Game()
        self.grid = Grid()
        self.reset_blocks()
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()

        # Game state
        self.game_over = False
        self.paused = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0

        # Player info
        self.player_name = player_name
        self.user_id = user_id

        # Difficulty setup
        self.difficulty_name = difficulty
        self.base_speed = self.DIFFICULTY_SPEEDS.get(difficulty, 400)
        self.current_speed = self.base_speed
        self.min_speed = 50

        # High scores
        self.HIGH_SCORES_FILE = "high_scores.json"

        # Initialize audio
        self.sounds = {}  # Initialize empty sounds dictionary first
        self.load_audio_settings()
        self.init_audio()  # This will properly set up all audio components

    def init_audio(self):
        """Initialize all audio components"""
        try:
            pygame.mixer.init()

            # Initialize with silent sounds first to prevent attribute errors
            silent_sound = pygame.mixer.Sound(buffer=bytearray(44))
            self.sounds = {
                'rotate': silent_sound,
                'drop': silent_sound,
                'clear': silent_sound,
                'gameover': silent_sound
            }

            # Try to load actual sounds
            try:
                self.sounds['rotate'] = pygame.mixer.Sound("Sounds/rotate.ogg")
                self.sounds['clear'] = pygame.mixer.Sound("Sounds/clear.ogg")
                # Uncomment these if you add the sound files later
                # self.sounds['drop'] = pygame.mixer.Sound("Sounds/drop.ogg")
                # self.sounds['gameover'] = pygame.mixer.Sound("Sounds/gameover.ogg")
            except Exception as e:
                print(f"Couldn't load some sound files: {e}")

            # Set initial volume
            self.update_volume(self.config.get("volume", 0.5))

            # Load and play music
            self.load_music(self.config.get("music_file", "Sounds/music.ogg"))

        except Exception as e:
            print(f"Error initializing audio: {e}")
            # Ensure sounds dictionary exists even if initialization fails
            silent_sound = pygame.mixer.Sound(buffer=bytearray(44))
            self.sounds = {
                'rotate': silent_sound,
                'drop': silent_sound,
                'clear': silent_sound,
                'gameover': silent_sound
            }

    # Remove the duplicate play_sound method and keep only this one:
    def play_sound(self, sound_name):
        """Play specified sound effect"""
        if hasattr(self, 'sounds') and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Error playing sound {sound_name}: {e}")

    # Dans GameModel
    def get_difficulty_name(self):
        return self.difficulty_name

    def load_audio_settings(self):
        """Load audio settings from config file"""
        config_path = "settings.json"
        default_config = {
            "volume": 0.5,
            "music_file": "Sounds/music.ogg",
            "controls": {
                "left": "left",
                "right": "right",
                "rotate": "up",
                "drop": "space",
                "pause": "p"
            }
        }

        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    self.config = json.load(f)
                    # Ensure all keys exist
                    for key in default_config:
                        if key not in self.config:
                            self.config[key] = default_config[key]
            else:
                self.config = default_config
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = default_config

    def init_audio(self):
        """Initialize all audio components"""
        try:
            pygame.mixer.init()

            # Load sound effects
            self.sounds = {
                'rotate': pygame.mixer.Sound("Sounds/rotate.ogg"),
                # 'drop': pygame.mixer.Sound("Sounds/drop.ogg"),
                'clear': pygame.mixer.Sound("Sounds/clear.ogg"),
                # 'gameover': pygame.mixer.Sound("Sounds/gameover.ogg")
            }

            # Set initial volume
            self.update_volume(self.config["volume"])

            # Load and play music
            self.load_music(self.config["music_file"])

        except Exception as e:
            print(f"Error initializing audio: {e}")
            self.sounds = {}

    def load_music(self, music_file):
        """Load and play background music"""
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # Loop indefinitely
        except Exception as e:
            print(f"Error loading music: {e}")

    def update_volume(self, volume):
        """Update volume for all sounds"""
        self.config["volume"] = volume
        pygame.mixer.music.set_volume(volume)
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def update_music(self, music_file):
        """Change background music"""
        self.config["music_file"] = music_file
        self.load_music(music_file)

    def play_sound(self, sound_name):
        """Play specified sound effect"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def update_game_speed(self):
        """Update game speed based on current level"""
        self.current_speed = max(50, self.base_speed - ((self.level - 1) * self.SPEED_DECREMENT))

    def reset(self):
        """Reset the game to initial state"""
        self.grid.reset()
        self.reset_blocks()
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.update_game_speed()

    def check_level_up(self):
        """Check if player should level up based on lines cleared"""
        new_level = 1
        for i, threshold in enumerate(self.LEVEL_THRESHOLDS):
            if self.lines_cleared >= threshold:
                new_level = i + 2  # Start from level 2

        if new_level > self.level:
            self.level = new_level
            self.update_game_speed()
            return True
        return False

    def update_score(self, lines_cleared, move_down_points=0):
        """Update score based on lines cleared and movement"""
        line_scores = {
            1: 100,
            2: 300,
            3: 500,
            4: 800
        }

        if lines_cleared in line_scores:
            self.score += line_scores[lines_cleared] * self.level

        self.score += move_down_points
        self.lines_cleared += lines_cleared
        self.check_level_up()

    def reset_blocks(self):
        """Reset the available blocks"""
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        return self.blocks

    def get_random_block(self):
        """Get a random block from available blocks"""
        if len(self.blocks) == 0:
            self.reset_blocks()
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def block_fits(self):
        """Check if current block fits in its position"""
        tiles = self.current_block.get_cell_positions()
        return all(self.grid.is_empty(tile.row, tile.column) for tile in tiles)

    def rotate(self):
        """Rotate current block if possible"""
        # Save the current rotation state
        original_rotation = self.current_block.rotation_state
        original_offset = self.current_block.offset.copy()

        # Try rotating
        self.current_block.rotate()

        # If rotation causes collision or goes out of bounds
        if not self.block_inside() or not self.block_fits():
            # Try wall kicks - move left/right to find a valid position
            kicks = [0, -1, 1, -2, 2]  # Try center, then left/right by 1, then by 2

            for kick in kicks:
                self.current_block.move(0, kick)
                if self.block_inside() and self.block_fits():
                    self.play_sound('rotate')
                    return  # Found valid position

                # Undo the kick attempt
                self.current_block.move(0, -kick)

            # If no valid position found, revert rotation
            self.current_block.rotation_state = original_rotation
            self.current_block.offset = original_offset
        else:
            self.play_sound('rotate')

    def block_inside(self):
        """Check if current block is within grid boundaries"""
        tiles = self.current_block.get_cell_positions()
        return all(self.grid.is_inside(tile.row, tile.column) for tile in tiles)

    def move_left(self):
        """Move block left if possible"""
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        """Move block right if possible"""
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        """Move block down if possible"""
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()
        else:
            self.play_sound('drop')

    def lock_block(self):
        """Lock the current block in place and check for completed rows"""
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id

        self.current_block = self.next_block
        self.next_block = self.get_random_block()

        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.play_sound('clear')
            self.update_score(rows_cleared, 0)

        if not self.block_fits():
            self.game_over = True
            self.play_sound('gameover')
            self.save_score()

    def save_score(self):
        """Save the current score to high scores file"""
        try:
            if os.path.exists(self.HIGH_SCORES_FILE):
                with open(self.HIGH_SCORES_FILE, 'r') as f:
                    scores = json.load(f)
            else:
                scores = []

            score_entry = {
                "player": self.player_name if self.player_name else "Guest",  # Ensure we have a name
                "score": self.score,
                "difficulty": self.difficulty_name,
                "level": self.level,
                "lines": self.lines_cleared,
                "timestamp": datetime.datetime.now().isoformat(),
                "user_id": self.user_id if self.user_id else None  # Include user_id if available
            }

            scores.append(score_entry)
            # Sort by score descending, then by timestamp (newer scores first for ties)
            scores.sort(key=lambda x: (-x["score"], x["timestamp"]))
            scores = scores[:10]  # Keep only top 10

            with open(self.HIGH_SCORES_FILE, 'w') as f:
                json.dump(scores, f, indent=4)
        except Exception as e:
            print(f"Error saving score: {e}")