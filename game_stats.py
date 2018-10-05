class GameStats():


#  init stats
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        #  Set the game to active
        self.game_active = False

        #  High score
        self.high_score = 0


    def reset_stats(self):
        self.planes_left = self.ai_settings.plane_limit
        self.score = 0
        self.level = 1