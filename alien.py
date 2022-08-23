import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, ai_settings, screen):
        """Initializes the alien and sets its starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image and assign the rect attribute.
        self.image = pygame.image.load('images/alien-1.bmp')
        self.rect = self.image.get_rect()

        # Load the screen rect attribute.
        self.screen_rect = screen.get_rect()

        # Each new alien appears in the upper left corner of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        if self.rect.right >= self.screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        """Displays the alien at its current position."""
        self.screen.blit(self.image, self.rect)
