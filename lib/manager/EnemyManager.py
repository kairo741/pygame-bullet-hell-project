from pygame import time, Surface
from random import randint
from object.Axis import Axis
from object.Ship import Ship
from utils.Constants import Constants
from utils.Utils import Utils


class EnemyManager:
    
    def __init__(self):
        super().__init__()
        self.enemy_sprite = Utils.scale_image(Constants.SPRITE_ENEMY_SHIP, 0.5)
        self.enemies = []
        self.last_enemy = 0

    def reset(self):
        self.enemies = []
        self.last_enemy = 0

    def spawn_enemy(self, x, y):
        
        if time.get_ticks() - self.last_enemy > 800:
            new_enemy = Ship(x=x, y=y, sprite=Surface.copy(self.enemy_sprite), speed=Axis(Utils.random_int(-4, 4), randint(0, 4)))
            new_enemy.set_size_with_sprite()
            new_enemy.center()
            self.enemies.append(new_enemy)
            self.last_enemy = time.get_ticks()
            
    def move_enemies(self, render_frame_time, screen_size):
        for e in self.enemies:
            e.x += e.speed.x * render_frame_time
            e.y += e.speed.y * render_frame_time
            
            if (self.check_enemy(screen_size, e)):
                self.enemies.remove(e)

    def check_enemy(self, screen_size, enemy):
        if (enemy.y < -enemy.size.y):
            return True

        elif (enemy.x < -enemy.size.x):
            return True

        elif (enemy.x > screen_size.x):
            return True

        elif (enemy.y > screen_size.y):
            return True

        return False

    def render_enemies(self, screen):
        for e in self.enemies:
            e.render(screen)
            if (e.health < 1):
                try:
                    Constants.SFX_EXPLOSION.play()
                    self.enemies.remove(e)
                except:
                    print("error removing enemy")
                

    def has_collided(self, object, action):
        for enemy in self.enemies:
            if enemy.collided_with(object, object.get_hitbox_rect()):
                try:
                    action()
                except:
                    print("error in enemy collision action")
                
                try:
                    self.enemies.remove(enemy)
                except:
                    print("error removing enemy")

                