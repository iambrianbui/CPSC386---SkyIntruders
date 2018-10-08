import pygame
from pygame.sprite import Sprite

#  Laser handling


class Laser(Sprite):

    def __init__(self, ai_settings, screen, alien):
        super(Laser, self).__init__()
        self.screen = screen

        #  Create a laser rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, ai_settings.laser_width, ai_settings.laser_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.top

        #  Store the laser position as a float
        self.y = float(self.rect.y)

        self.color = ai_settings.laser_color
        self.speed_factor = ai_settings.laser_speed_factor

    def update(self):
        #  Update the position of the laser
        self.y += self.speed_factor
        #  Update the rect position
        self.rect.y = self.y

    def draw_laser(self):
        #  Draw the actual laser
        pygame.draw.rect(self.screen, self.color, self.rect)


