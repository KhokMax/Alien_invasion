import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class for controlling bullets fired by a ship."""
    def __init__(self, ai_settings, screen, ship):
        """Creates a bullet object at the ship's current position."""
        super().__init__()
        self.screen = screen

        # Create a bullet at position (0,0) and assign the correct position.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_wight, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.center = float(self.rect.centery)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

        self.bullet_sound = pygame.mixer.Sound('music/vyistrelyi-iz-blastera-23706 (mp3cut.net).mp3')



    def update(self):
        """Moves the bullet up the screen."""
        # Update bullet position in floating point format.
        self.center -= self.speed_factor
        # Update the position of the rectangle.
        self.rect.centery  = self.center

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


