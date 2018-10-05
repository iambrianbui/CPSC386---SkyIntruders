import pygame.font
from pygame.sprite import Group

from plane import Plane

class Scoreboard():


    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        #  Font
        self.text_color = (0, 100, 10)
        self.font = pygame.font.SysFont(None, 48)

        #  Prepare the HUD
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_planes()


    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        #  Display the score at the top right
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def show_score(self):
        #  Actually draw the scoreboard
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.planes.draw(self.screen)


    def prep_high_score(self):
        #  Turn the high score into a rendered image.
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        #  Center the high score at the top
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top


    def prep_level(self):
        #  Turn the level into a rendered image.
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)

        #  Place it below the score
        self.level_rect =  self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10


    #  Show how many ships are left
    def prep_planes(self):
        self.planes = Group()
        for plane_number in range(self.stats.planes_left):
            plane = Plane(self.ai_settings, self.screen)
            plane.rect.x = 10 + plane_number * plane.rect.width
            plane.rect.y = 10
            self.planes.add(plane)