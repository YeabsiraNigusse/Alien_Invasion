from pathlib import Path

class GameStats:

    def __init__(self, ai_game):
        self.settings =  ai_game.settings
        self.reset_stats()
        self.game_active = False
        path = Path(r'C:\Users\User\Desktop\python\Projects\Alien_Invasion\files\high_score.txt')
        try:
            with open(path) as file:
                content = file.read()
        except FileNotFoundError:
            self.high_score = 0
        else:
            if content == '0':
               self.high_score = 0
            else:
                self.high_score = 0
                self.high_score = int(content)
       

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1  