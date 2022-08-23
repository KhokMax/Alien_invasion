class Settings:
    """Class for saving the main settings of project Alien Invasion"""
    def __init__(self):
        """Initializes the game settings."""
        self.screen_wight = 1600
        self.screen_height = 800
        self.screen_color = (0, 33, 29)

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_wight = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 3

        # Speed up the game
        self.speedup_scale = 1.2
        self.speedup_scale_ship_bullets = 1.1
        # The growth rate of the value of aliens
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 2.5
        self.bullet_speed_factor = 2.5

        # alien settings
        self.alien_speed_factor = 1
        self.alien_drop_speed = 50

        # fleet_direction = 1 means moving to the right; and -1 - to the left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed_factor *= self.speedup_scale_ship_bullets
        self.bullet_speed_factor *= self.speedup_scale_ship_bullets
        self.alien_speed_factor *= self.speedup_scale
        self.alien_drop_speed *= self.speedup_scale
        self.alien_points = int(self.score_scale * self.alien_points)

