import pygame
from pygame.sprite import Sprite

class Plane(Sprite):

#  Init the ship and starting position
    def __init__(self, ai_settings, screen):
        super(Plane, self).__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        #  Load the ship image and get its rect
        self.image = pygame.image.load('image/plane.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #  Start each new ship at the bottom center
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #  Store a decimal value for the ship's center
        self.center = float(self.rect.centerx)

        #  Ensures that player can only move in one direction
        self.moving_right = False
        self.moving_left = False

        #  See if the plane needs to be destroyed
        self.plane_alive = True
        self.index = 0


    def center_plane(self):
        self.center = self.screen_rect.centerx

#  Update the ship position based on movement flags
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.plane_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.plane_speed_factor
        self.rect.centerx = self.center


    def blitme(self):
        self.screen.blit(self.image, self.rect)