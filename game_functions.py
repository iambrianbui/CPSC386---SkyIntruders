import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien


#  Create an alien and find the number of aliens that can fit
def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


#  Determine how many rows can fit
def get_number_rows(ai_settings, plane_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - plane_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    #  Create an alien and place it into the row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


#  Create a full fleet of aliens
def create_fleet(ai_settings, screen, plane, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, plane.rect.height, alien.rect.height)

    #  Create the first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def update_bullets(ai_settings, screen, stats, sb, plane, aliens, bullets):
    bullets.update()
    #  Get rid of bullets that aren't on the screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, plane, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, plane, aliens, bullets):
    #  Check for any bullets that hit aliens
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        #  Erase all existing bullets and refresh the fleet + speed up + level up
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, plane, aliens)

        stats.level += 1
        sb.prep_level()


def check_keydown_events(event, ai_settings, screen, plane, bullets):
    if event.key == pygame.K_RIGHT:
        plane.moving_right = True

    elif event.key == pygame.K_LEFT:
        plane.moving_left = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, plane, bullets)

    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, plane, bullets):
    #  Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, plane)
        bullets.add(new_bullet)
        fire = pygame.mixer.Sound('sounds/fire.ogg')
        fire.play()


def check_keyup_events(event, plane):
    if event.key == pygame.K_RIGHT:
        plane.moving_right = False
    elif event.key == pygame.K_LEFT:
        plane.moving_left = False


#  Record key strokes
def check_events(ai_settings, screen, stats, sb, play_button, plane, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, plane, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, plane)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, plane, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, plane, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        #  Reset game settings
        ai_settings.initialize_dynamic_settings()

        #  Hide the cursor
        pygame.mouse.set_visible(False)

        stats.reset_stats()
        stats.game_active = True

        #  Reset the scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_planes()

        #  reload everything
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, plane, aliens)
        plane.center_plane()


#  Update the screen
def update_screen(ai_settings, screen, stats, sb, plane, aliens, bullets, play_button):
    #  Redraw every frame
    screen.fill(ai_settings.bg_color)
    #  Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    plane.blitme()
    aliens.draw(screen)

    #  display scoreboard
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    #  Show most current frame
    pygame.display.flip()


#  Check for edges
def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


#  Drop the fleet and change directions
def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def plane_hit(ai_settings, stats, sb, screen, plane, aliens, bullets):
    if stats.planes_left > 1:
        #  Decrement ships left
        stats.planes_left -= 1

        #  Update scoreboard
        sb.prep_planes()

        #  Reload aliens and bullets
        aliens.empty()
        bullets.empty()

        #  Reset fleet and plane
        create_fleet(ai_settings, screen, plane, aliens)
        plane.center_plane()

        #  Pause
        sleep(0.5)
    else:
        stats.game_active = False
        gameoversound = pygame.mixer.Sound('sounds/gameover.wav')
        gameoversound.play()
        pygame.mouse.set_visible(True)


def update_aliens(ai_settings, stats, sb, screen, plane, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #  Check alien-plane collisions
    if pygame.sprite.spritecollideany(plane, aliens):
        print("Ship hit!!!")
        plane_hit(ai_settings, stats, sb, screen, plane, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, sb, screen, plane, aliens, bullets)


#  Anything that hits the bottom
def check_aliens_bottom(ai_settings, stats, sb, screen, plane, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #  Treat it as if the ship got hit
            plane_hit(ai_settings, stats, sb, screen, plane, aliens, bullets)
            break


#  Check if there is a new high score.
def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()