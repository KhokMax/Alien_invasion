import pygame.image
from pygame.sprite import Sprite


class Live(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load('images/heart.png')
        self.rect = self.image.get_rect()
        self.width = self.rect.width

    def blit(self):
        self.screen.blit(self.image, self.rect)