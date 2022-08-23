import pygame.font

from pygame.sprite import Group
from lives import Live


class Scoreboard:
    def __init__(self, ai_settings, screen, stats):
        """Class for displaying game information."""
        self.ai_settings = ai_settings
        self.stats = stats
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Font settings for invoice output.
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.lives = Group()

        # Preparing the original image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_lives()

    def prep_score(self):
        """Converts the current score to a graphic."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Converts the record score to a graphic."""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)

        # The record is centered on the top s
        self.high_score_rect = self.score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.score_rect.top = self.score_rect.top

    def prep_level(self):
        """Converts the record level to a graphic."""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color)

        # The level is displayed under the current account.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.score_rect.bottom + 10
        self.level_rect.right = self.score_rect.right

    def prep_lives(self):
        # Group of lives
        self.lives = Group()

        for ship_number in range(self.stats.ships_left):
            live = Live(self.screen)
            live.rect.top = live.screen_rect.top
            live.rect.x = live.rect.width * ship_number + 10
            self.lives.add(live)

    def show_score(self):
        """Displays the score on the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.lives.draw(self.screen)