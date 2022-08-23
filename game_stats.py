
class GameStats:
    """Stats tracking for Alien Invasion."""

    def __init__(self, ai_settings):
        """Initializes statistics."""

        # The Alien Invasion game starts in an active state.

        self.ai_settings = ai_settings

        # The record must not be reset.
        self.high_score = self.get_high_score()

        self.reset_stats()

        # The game starts in an inactive state.
        self.game_active = False

    def reset_stats(self):
        """Initializes statistics that change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def get_high_score(self):
        with open("high score info.txt", 'r') as file:
            return int(file.read())

