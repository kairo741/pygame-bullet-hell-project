from pygame import draw, time
from utils.Constants import Constants
from utils.Presets import Presets

from .Axis import Axis
from .Ship import Ship


class Player(Ship):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", weapon="", health=100, layout=Presets.PRIMARY_KB_LAYOUT):
        super().__init__(x, y, size, speed, sprite, weapon, health)
        self.layout = layout

    def take_damage(self, value):
        super().take_damage(value)
        if not self.is_alive():
            self.disable()


    def move(self, direction, render_frame_time, limit):
        if self.is_alive():
            if direction == "r":
                if self.x + self.size.x < limit.x:
                    self.x += self.speed.x * render_frame_time

            if direction == "l":
                if self.x > 2:
                    self.x -= self.speed.x * render_frame_time

            if direction == "u":
                if self.y > 2:
                    self.y -= self.speed.y * render_frame_time

            if direction == "d":
                if self.y + self.size.y < limit.y:
                    self.y += self.speed.y * render_frame_time

    def shoot(self, bullet_manager):
        if self.is_alive():
            if time.get_ticks() - self.last_bullet > self.weapon.shoot_delay:
                for generated_bullet in self.weapon.make_bullets(self.get_middle()):
                    bullet_manager.shoot(generated_bullet)

                Constants.SFX_LASER.play()
                self.last_bullet = time.get_ticks()


    def ult(self, *conditions, action):
        if self.is_alive():
            if all(conditions[0]):
                action()


    def control_ship(self, keys, render_frame_time, limit):
        if self.is_alive():
            if keys[self.layout.right]:
                self.move("r", render_frame_time, limit)

            if keys[self.layout.left]:
                self.move("l", render_frame_time, limit)

            if keys[self.layout.up]:
                self.move("u", render_frame_time, limit)

            if keys[self.layout.down]:
                self.move("d", render_frame_time, limit)


    def control_shoot(self, keys, bullet_manager):
        if keys[self.layout.shoot]:
            self.shoot(bullet_manager)
                

    def control_ultimate(self, keys, *conditions, action):
        if keys[self.layout.ultimate]:
            self.ult(conditions, action=action)

    
    def control_ship_joystick(self, joystick, render_frame_time, limit):
        axis = Axis(joystick.get_axis(0), joystick.get_axis(1))

        if axis.x > self.layout.right:
            self.move("r", render_frame_time, limit)

        if axis.x < self.layout.left:
            self.move("l", render_frame_time, limit)

        if axis.y < self.layout.up:
            self.move("u", render_frame_time, limit)

        if axis.y > self.layout.down:
            self.move("d", render_frame_time, limit)

    def control_shoot_joystick(self, joystick, bullet_manager):
        if joystick.get_button(self.layout.shoot):
            self.shoot(bullet_manager)

    def control_ultimate_joystick(self, joystick, *conditions, action):
        if joystick.get_button(self.layout.ultimate):
            self.ult(conditions, action)



    def render(self, screen):
        super().render(screen)
        lifebar_size = Axis(self.size.x, self.size.y / 10)
        draw.rect(screen, (255, 100, 100),
                  (self.x, self.size.y + self.y + lifebar_size.y * 2, lifebar_size.x, lifebar_size.y))
        draw.rect(screen, (100, 255, 100),
                  (self.x, self.size.y + self.y + lifebar_size.y * 2, lifebar_size.x * (self.health / 100),
                   lifebar_size.y))
        draw.rect(screen, (75, 255, 75), self.get_hitbox_rect(), border_radius=100)
