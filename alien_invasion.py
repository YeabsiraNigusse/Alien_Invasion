from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from gamestats import GameStats
from button import Button
from scoreboard import ScorBoard
from time import sleep
from pygame import mixer
import sys
import pygame
 
class AlienInvasion:
    """Over all class to manage game asset and behaviour"""

    def __init__(self):
        """Initialize the game and creat game resource"""
        pygame.init()

        self.settings = Settings()
        
        
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')
        self.ship = Ship(self)
        self.stats = GameStats(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.sb = ScorBoard(self)

        self._creat_fleet()
        self.play_button = Button(self, 'Play')


    def run_game(self):
        """start the main loop for the game"""
        mixer.music.load(r'C:\Users\User\Desktop\python\Projects\Alien_Invasion\Musics\samiMusic.mp3')
        mixer.music.play(-1)
        while True:
            #watch for keyboard and mouse events
            self.__check_events__()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_alien() 
            self.__update_screen__()
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_alien(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        self._check_alien_bottom()

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._creat_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _check_alien_bottom(self):
        screen_rect = self.screen.get_rect()
        for  alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _creat_fleet(self):
        alien = Alien(self)
        alien_width,alien_hight = alien.rect.size
        availabel_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = availabel_space_x// (2*alien_width)

        ship_height = self.ship.rect.height
        availabel_space_y = (self.settings.screen_height - (3 * alien_hight) - ship_height)
        number_rows = availabel_space_y // (2 * alien_hight)

        for row_number in range(number_rows):
          for alien_number in range(number_aliens_x):
           self._creat_alien(alien_number,row_number)

    def _creat_alien(self,alien_number, row_number):
         alien = Alien(self)
         alien_width, alien_height = alien.rect.size
         alien.x = alien_width + 2 * alien_width * alien_number
         alien.rect.x = alien.x
         alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
         self.aliens.add(alien)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
        self._check_alien_bullet_collision()
        
    def _check_alien_bullet_collision(self):
        collision = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collision:
            for alien in collision.values():
               self.stats.score += self.settings.alien_points * len(alien)
            self.sb.prep_score()
            self.sb._check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._creat_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()
        

    def __check_events__(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                elif event.type == pygame.KEYDOWN:
                     self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                     self._check_keyup_events(event)
    def _check_play_button(self,mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active :
            self.settings.initialize_dynamic_setting()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._creat_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)
    
    def _check_keydown_events(self,event):
         if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
         elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
         elif event.key == pygame.K_SPACE:
            if self.stats.game_active:
              bullet_sound = mixer.Sound(r'C:\Users\User\Desktop\python\Projects\Alien_Invasion\Musics\shotgun.mp3')
              bullet_sound.play()
            self._fire_Bullet()
         elif event.key == pygame.K_q:
            sys.exit()
    
    def _fire_Bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
          new_bullet = Bullet(self)
          self.bullets.add(new_bullet)
        
    
    def _check_keyup_events(self,event):
         if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
         elif event.key == pygame.K_LEFT:
              self.ship.moving_left = False


    def __update_screen__(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.Draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
            
        #make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    #make the game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
    
