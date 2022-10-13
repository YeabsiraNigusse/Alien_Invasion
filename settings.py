class Settings:
    def __init__(self):

        
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 10
        self.fleet_drop_speed  = 15 
        self.ship_limit = 3
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.bg_color = (230,230,230)
        self.screen_width = 1100
        self.screen_height = 700

        self.initialize_dynamic_setting()

    def initialize_dynamic_setting(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        self.fleet_direction = 1
        self.alien_points = 1

    def increase_speed(self):
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.ship_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

        
