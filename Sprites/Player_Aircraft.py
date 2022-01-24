import pygame
from Sprites.Bullet import Bullet
from Sprites.Boom import Boom
from Sprites.Fire import Fire


class Player_Aircraft(pygame.sprite.Sprite):

    def __init__(self, x, y, dynamic_group, all_groups, img_path, ammo):
        pygame.sprite.Sprite.__init__(self)
        pygame.font.init()
        pygame.mixer.init()
        self.font = pygame.font.SysFont("Verdana", 20)
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.speed, self.a = 0, 0.05
        self.dynamic_group = dynamic_group
        self.all_groups = all_groups
        self.pitch_speed = 5
        self.crashed = False
        self.ammo = ammo
        self.power = 0
        self.shoot_sound = pygame.mixer.Sound("Sounds/shoot.mp3")
        self.plain_ammo_sound = pygame.mixer.Sound("Sounds/plain_ammo.mp3")
        self.engine_sound = pygame.mixer.Sound("Sounds/engine.mp3")
        self.engine_sound.set_volume(0.06)
        self.engine_sound_play = True

    def update(self):
        self.run()
        self.__check_stall()
        self.__engine_power_check()

    def shoot(self, bullets, all_groups):
        if self.ammo > 0:
            bullet = Bullet(self.rect.x + self.rect.w, self.rect.y + self.rect.h / 2 / 2)
            fire = Fire(self.rect.x + self.rect.w, self.rect.y + self.rect.h / 2 / 2)
            bullets.add([bullet, fire])
            all_groups.add([bullet, fire])
            pygame.mixer.find_channel(True).play(self.shoot_sound)

            self.ammo -= 1
        else:
            pygame.mixer.find_channel(True).play(self.plain_ammo_sound)

    def start_engine(self):
        if self.speed < 6 and not self.crashed:
            self.speed += self.a
            self.power += 1
        if self.power > 100:
            self.power = 100
        # self.engine_sound.play()

    def off_engine(self):
        if self.speed > 0:
            self.speed -= self.a
            self.power -= 1
        if self.power < 0:
            self.power = 0

    def update_pitch(self, vector, stall_speed=0):
        if vector > 0 and self.speed > 4 and self.rect.y > 0:
            self.rect.y -= self.pitch_speed
        elif vector < 0 and self.rect.y < 400:
            self.rect.y += self.pitch_speed - stall_speed

    def __engine_power_check(self):
        if self.power == 0:
            self.engine_sound.set_volume(0)
        elif self.power < 25:
            self.engine_sound.set_volume(0.04)
        elif self.power < 50:
            self.engine_sound.set_volume(0.06)
        elif self.power < 75:
            self.engine_sound.set_volume(0.08)
        elif self.power < 100:
            self.engine_sound.set_volume(0.1)
        if self.engine_sound_play:
            pygame.mixer.find_channel(True).play(self.engine_sound)
        else:
            self.engine_sound.stop()

    def run(self):
        for sprite in self.dynamic_group:
            if not self.crashed:
                sprite.rect.x -= self.speed
                if sprite.rect.x < -200:
                    sprite.kill()

    def __draw_ammo(self, surf):
        bullet_icon = pygame.image.load("imgs/Icons/bullet-icon.png")
        txt = self.font.render(str(self.ammo), True, (0, 0, 0))
        surf.blit(txt, txt.get_rect(centerx=50, centery=30))
        surf.blit(bullet_icon, bullet_icon.get_rect(centerx=30, centery=30))

    def __draw_engine_power(self, surf):
        engine_icon = pygame.image.load("imgs/Icons/engine-icon.png")
        txt = self.font.render(str(self.power) + "%", True, (0, 0, 0))
        surf.blit(txt, txt.get_rect(centerx=140, centery=30))
        surf.blit(engine_icon, engine_icon.get_rect(centerx=90, centery=30))

    def draw_player_info(self, surf):
        self.__draw_ammo(surf)
        self.__draw_engine_power(surf)

    def crush(self):
        self.rect.x = self.rect.x - 10
        self.rect.y = self.rect.y - 10
        self.crashed = True
        boom = Boom(self.rect.centerx, self.rect.y - self.rect.w / 2 / 2, 150, 150)
        self.dynamic_group.add(boom)
        self.all_groups.add(boom)
        self.kill()

    def __check_stall(self):
        if self.speed < 3:
            self.update_pitch(-1, 3)
