import sys

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from plane import Plane
from alien import Alien
import game_functions as gf

def run_game():
    #  Initialize game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Sky Intruders")

    clock = pygame.time.Clock()

    #  Make play button
    play_button = Button(ai_settings, screen, "Play")

    #  Create an instance to store game stats and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    #  Make a ship
    plane = Plane(ai_settings, screen)
    #  Make an alien
    alien = Alien(ai_settings, screen)
    #  Make a group to store bullets in
    bullets = Group()
    #  Make a group to store aliens in
    aliens = Group()
    #  Make a lasers group
    lasers = Group()

    #  Create the fleet of aliens
    gf.create_fleet(ai_settings, screen, plane, aliens)

    #  Start the main loop for the game.

    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, plane, aliens, bullets)

        if stats.game_active:
            plane.update()
            gf.update_bullets(ai_settings, screen, stats, sb, plane, aliens, bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, plane, aliens, bullets, lasers)
            gf.update_lasers(ai_settings, stats, sb, screen, plane, aliens, bullets, lasers)

        gf.update_screen(ai_settings, screen, stats, sb, plane, aliens, bullets, play_button, lasers)

        #  What for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        #  Make the most recently drawn screen visible.
        pygame.display.flip()
        clock.tick(60)

run_game()