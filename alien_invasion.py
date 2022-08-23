import pygame

import game_functions as gf

from scoreboard import Scoreboard
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button



def run_game():
    # Initialize the game and create the screen object.
    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load("music/man-is-he-mega-glbml-22045.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)


    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_wight, ai_settings.screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption('Alien_invasion')
    fon = pygame.image.load('images/fon.jpg')

    # Create a ship, a group of bullets and a group of aliens.
    ship = Ship(screen, ai_settings)
    bullets = Group()
    aliens = Group()

    # Create an instance to store game statistics.
    # Create instances of GameStats and Scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Creating Play button
    play_button = Button(ai_settings, screen, "Play")

    # creating alien`s fleet
    gf.create_fleet(ai_settings, screen, aliens, ship)

    # starting of the main cycle
    while True:
        # tracking mouse and keyboard actions
        gf.check_events(ai_settings, screen, ship, bullets, aliens, stats, sb, play_button)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, bullets, aliens, stats, sb)
            gf.update_aliens(aliens, ai_settings, ship, stats, sb, screen, bullets)

        # update the screenq
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, fon, play_button, stats, sb)


run_game()