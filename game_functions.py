import sys
import pygame

from time import sleep
from random import randint

import button
from bullet import Bullet
from alien import Alien
from star import Star


def check_high_score(stats, sb):
    """Checks if there is a new record."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        with open('high score info.txt', 'w') as file:
            file.write(str(stats.score))


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fires a bullet if the maximum hasn't been reached yet."""
    # Create a new bullet and include it in the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        new_bullet.bullet_sound.play()


def check_keydown_events(event, ai_settings, screen, ship, bullets, aliens, stats, sb):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        check_play_p(ai_settings, screen, ship, bullets, aliens, stats, sb)


def check_keyup_event(ship, event):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def start_game(ai_settings, screen, ship, bullets, aliens, stats, sb):
    # Reset game statistics.
    stats.reset_stats()
    stats.game_active = True

    # Clean up lists of aliens and bullets
    aliens.empty()
    bullets.empty()

    # Reset images of scores and levels.
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_lives()

    # Create a new fleet and place the ship in the center.
    ship.center_ship()
    create_fleet(ai_settings, screen, aliens, ship)

    # The mouse pointer is hidden.
    pygame.mouse.set_visible(False)


def check_play_button(ai_settings, screen, ship, bullets, aliens, stats, sb, play_button, mouse_x, mouse_y):
    """Starts a new game when the Play button is pressed."""
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        start_game(ai_settings, screen, ship, bullets, aliens, stats, sb)


def check_play_p(ai_settings, screen, ship, bullets, aliens, stats, sb):
    """Starts a new game when the Play button is pressed."""
    if not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        start_game(ai_settings, screen, ship, bullets, aliens, stats, sb)


def check_events(ai_settings, screen, ship, bullets, aliens, stats, sb, play_button):
    """Handles keystrokes and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, aliens, stats, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_event(ship, event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, ship, bullets, aliens, stats, sb, play_button, mouse_x, mouse_y)



def get_number_rows(ai_settings, ship_height, alien_height):
    number_rows = int((ai_settings.screen_height - ship_height - alien_height * 3) / (2 * alien_height))
    return number_rows


def get_number_aliens_x(ai_settings, alien_wight):
    """Calculates the number of aliens in a row."""
    availabel_space_x = ai_settings.screen_wight - 2 * alien_wight
    number_aliens_x = int(availabel_space_x / (alien_wight * 2) - 7)
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Spawns an alien and places it in a row."""
    alien = Alien(ai_settings, screen)
    alien_wight = alien.rect.width

    alien.x = alien_wight + 3 * alien_wight * alien_number
    alien.rect.x = alien.x

    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number

    aliens.add(alien)


def create_fleet(ai_settings, screen, aliens, ship):
    """Creates an alien fleet."""
    # Create an alien and calculate the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def create_star_fon(ai_settings, screen, stars):
    star = Star(screen)
    star_width = star.rect.width
    star_height = star.rect.height
    number_star_x = int(ai_settings.screen_wight / (star_width * 2))
    number_star_y = int(ai_settings.screen_height / (star_height * 2))
    for y in range(number_star_y):
        for x in range(number_star_x):
            star = Star(screen)
            star.rect.x = star.rect.x + star.rect.width * 2 * x + randint(-70, 70)
            star.rect.y = star.rect.y + star.rect.height * 2 * y + randint(-70, 70)
            stars.add(star)


def change_fleet_direction(ai_settings, aliens):
    """Lowers the entire fleet and reverses the direction of the fleet."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_speed
    ai_settings.fleet_direction *= -1


def change_fleet_edges(ai_settings, aliens):
    """Reacts when an alien reaches the edge of the screen."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Handles ship-alien collision."""
    if stats.ships_left > 0:
        # Decrease ships_left
        stats.ships_left -= 1
        sb.prep_lives()

        # Clean up lists of aliens and bullets.
        bullets.empty()
        aliens.empty()

        # Clean up lists of aliens and bullets.
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()
        # pause
        sleep(0.5)
    else:
        stats.game_active = False
        # The mouse pointer is not hidden.
        pygame.mouse.set_visible(True)



def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Checks if the aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # The same happens as in a collision with a ship.
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break


def update_aliens(aliens, ai_settings, ship, stats, sb, screen, bullets):
    """
    Checks if the fleet has reached the edge of the screen,
    after which it updates the positions of all aliens in the fleet.
    """
    change_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

    # Check for aliens that have reached the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


def check_bullets_aliens_collisions(ai_settings, screen, ship, bullets, aliens, stats, sb):
    # Check for hits on aliens.
    # When a hit is found, remove the bullet and the alien.
    collision = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collision:
        for alien in collision.values():
            stats.score += ai_settings.alien_points * len(alien)

    sb.prep_score()
    check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, aliens, ship)

def update_bullets(ai_settings, screen, ship, bullets, aliens, stats, sb):
    bullets.update()
    check_bullets_aliens_collisions(ai_settings, screen, ship, bullets, aliens, stats, sb)

    # deleting extra bullets (upper then screen)
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def update_screen(ai_settings, screen, ship, bullets, aliens, fon, play_button, stats, sb):
    """Update the screen"""
    # the screen is redrawn on each iteration of the loop.
    screen.blit(fon, (0,0))
    #screen.fill(ai_settings.screen_color)

    # All bullets are displayed behind the images of the ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # The Play button is displayed if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Invoice output.
    sb.show_score()

    # display the last screen drawn.
    pygame.display.flip()
