"""A class that handles all of the settings for Alien Invasion."""


class Settings():

    """Initialize game settings."""
    def __init__(self):
        #  Screen settings:
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (115, 196, 252)

        #  Ship settings:
        self.plane_limit = 2

        #  Bullet settings:
        self.bullet_width = 6
        self.bullet_height = 20
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 5

        #  Laser settings:
        self.laser_width = 3
        self.laser_height = 15
        self.laser_color = 255, 10, 10
        self.laser_freq = 70

        #  Alien settings
        self.fleet_drop_speed = 10

        #  How much game scaling
        self.speedup_scale = 1.1
        #  How quickly the points scale
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.plane_speed_factor = 3
        self.bullet_speed_factor = 3
        self.laser_speed_factor = 3
        self.alien_speed_factor = 3

        #  1 is right, -1 is left
        self.fleet_direction = 1

        #  Scoring
        self.alien_points = 50

    def increase_speed(self):
        self.plane_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)