import pygame
import random
from pygame.sprite import Sprite

from laser import Laser

class Alien(Sprite):

    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('image/orangealien1.png')
        self.rect = self.image.get_rect()

        #  Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #  Store the alien's exact position.
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    #  Make sure the aliens don't hit the edge too hard
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    #  Move the alien
    def update(self, ai_settings, screen, lasers):
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        if pygame.time.get_ticks() % 50 == 0:
            self.shoot(ai_settings, screen, lasers)
        if pygame.time.get_ticks() % 200 <= 100:
            self.image = pygame.image.load('image/orangealien2.png')
        else:
            self.image = pygame.image.load('image/orangealien1.png')


    def shoot(self, ai_settings, screen, lasers):
        if (random.randint(1,100)) > 90:
            new_laser = Laser(ai_settings, screen, self)
            lasers.add(new_laser)