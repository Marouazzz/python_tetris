import pygame
from colors import Colors

class GameView:
    def __init__(self):
        pygame.init()
        self.width = 500
        self.height = 620
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Python Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 42)


        try:
            icon = pygame.image.load("ui/block_tetris.jpg")
            pygame.display.set_icon(icon)
        except:
            print("Could not load window icon")

    def draw(self, model):
        self.screen.fill(Colors.dark_blue)

        # Dimensions et positions
        margin_x = 320
        width = 170
        height_score = 60
        height_next = 180
        height_difficulty = 60
        spacing = 45

        # Rectangles UI
        score_rect = pygame.Rect(margin_x, 55, width, height_score)
        difficulty_rect = pygame.Rect(margin_x, score_rect.bottom + spacing, width, height_difficulty)
        next_rect = pygame.Rect(margin_x, difficulty_rect.bottom + spacing, width, height_next)

        # Titres avec ombre (placés au-dessus des rectangles)
        self._draw_text_with_shadow("SCORE", margin_x, score_rect.y - 35, width, 30, Colors.white, self.title_font)
        self._draw_text_with_shadow("DIFFICULTY", margin_x, difficulty_rect.y - 35, width, 30, Colors.white,
                                    self.title_font)
        self._draw_text_with_shadow("NEXT", margin_x, next_rect.y - 35, width, 30, Colors.white, self.title_font)

        # Boîtes avec dégradé
        self._draw_gradient_rect(score_rect, Colors.light_blue, Colors.dark_blue)
        self._draw_gradient_rect(difficulty_rect, Colors.light_blue, Colors.dark_blue)
        self._draw_gradient_rect(next_rect, Colors.light_blue, Colors.dark_blue)

        self._draw_centered_text(str(model.score), score_rect.x, score_rect.y, width, height_score, Colors.white, 40)

        # Difficulté
        difficulty_name = model.get_difficulty_name() if hasattr(model, 'get_difficulty_name') else "Medium"
        self._draw_centered_text(difficulty_name, difficulty_rect.x, difficulty_rect.y, width, height_difficulty,
                                 Colors.white, 35)

        # Grille et blocs
        model.grid.draw(self.screen)
        model.current_block.draw(self.screen, 11, 11)

        # Calculate position for next block - shifted slightly left
        block_size = 30  # Size of each block cell
        block_width = model.next_block.get_width() * block_size
        block_height = model.next_block.get_height() * block_size

        # Calculate centered position with left adjustment
        next_block_x = next_rect.x + (next_rect.width - block_width) // 2 - 80
        next_block_y = next_rect.y + (next_rect.height - block_height) // 2 + 25

        # Draw the next block
        model.next_block.draw(self.screen, next_block_x, next_block_y)

        # Game over message - adjusted to fit container better
        if model.game_over:
            # Create a semi-transparent overlay
            overlay = pygame.Surface((500, 620), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Dark semi-transparent
            self.screen.blit(overlay, (0, 0))

            # Game over window dimensions
            window_width, window_height = 350, 200
            window_x = (500 - window_width) // 2
            window_y = (620 - window_height) // 2

            # Draw window background
            pygame.draw.rect(self.screen, (30, 40, 60),
                             (window_x, window_y, window_width, window_height),
                             border_radius=20)
            pygame.draw.rect(self.screen, (80, 100, 150),
                             (window_x, window_y, window_width, window_height),
                             3, border_radius=20)

            # Game Over title
            title = self.title_font.render("GAME OVER", True, Colors.red)
            self.screen.blit(title,
                             (window_x + (window_width - title.get_width()) // 2,
                              window_y + 30))

            # Score display
            score_text = self.font.render(f"Final Score: {model.score}", True, Colors.white)
            self.screen.blit(score_text,
                             (window_x + (window_width - score_text.get_width()) // 2,
                              window_y + 80))

            # Restart instruction
            restart_text = self.font.render("Press R to restart", True, Colors.white)
            self.screen.blit(restart_text,
                             (window_x + (window_width - restart_text.get_width()) // 2,
                              window_y + 120))
        # Menu pause
        if getattr(model, "paused", False):
            self.draw_pause_menu()

        pygame.display.flip()
        self.clock.tick(60)

    def _draw_centered_text(self, text, x, y, width, height, color, font_size):
        font = pygame.font.Font(None, font_size)
        surface = font.render(str(text), True, color)
        rect = surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(surface, rect)

    def _draw_text_with_shadow(self, text, x, y, width, height, color, font=None):
        font = font or self.font
        # Ombre
        shadow = font.render(text, True, Colors.black)
        shadow_rect = shadow.get_rect(center=(x + width // 2 + 2, y + height // 2 + 2))
        self.screen.blit(shadow, shadow_rect)
        # Texte principal
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surf, text_rect)

    def _draw_gradient_rect(self, rect, color1, color2):
        """Dessine un rectangle avec dégradé"""
        for y in range(rect.top, rect.bottom):
            ratio = (y - rect.top) / rect.height
            r = int(color1[0] + (color2[0] - color1[0]) * ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * ratio)
            b = int(color1[2] + (color2[2] - color1[2]) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (rect.left, y), (rect.right, y))
        pygame.draw.rect(self.screen, Colors.white, rect, 2, border_radius=10)

    def draw_pause_menu(self):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        # Draw pause text
        font = pygame.font.SysFont('Arial', 50)
        text = font.render('PAUSED', True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.screen.blit(text, text_rect)

        # Draw buttons
        resume_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 20, 200, 50)
        exit_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 90, 200, 50)

        pygame.draw.rect(self.screen, (0, 200, 0), resume_button)
        pygame.draw.rect(self.screen, (200, 0, 0), exit_button)

        font = pygame.font.SysFont('Arial', 30)
        resume_text = font.render('Resume', True, (0, 0, 0))
        exit_text = font.render('Exit', True, (0, 0, 0))

        self.screen.blit(resume_text, (resume_button.centerx - resume_text.get_width() // 2,
                                       resume_button.centery - resume_text.get_height() // 2))
        self.screen.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2,
                                     exit_button.centery - exit_text.get_height() // 2))

        return resume_button, exit_button
    def close(self):
        pygame.quit()