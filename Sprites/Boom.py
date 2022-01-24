import pygame


class Boom(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.w = w
        self.h = h
        self.boom_animation = []
        self.__add_images()
        self.image = self.boom_animation[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.frame = 0
        self.last_tick = pygame.time.get_ticks()
        self.frame_rate = 50
        self.finished = False

    def update(self):
        now_tick = pygame.time.get_ticks()
        if now_tick - self.last_tick > self.frame_rate:
            self.last_tick = now_tick
            self.frame += 1
            if self.frame == len(self.boom_animation):
                self.kill()
                self.finished = True
            else:
                x = self.rect.x
                y = self.rect.y
                self.image = self.boom_animation[self.frame]
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y

    def __add_images(self):
        for i in range(11):
            filename = f"imgs/Booms/boom{i}.png"
            img = pygame.transform.scale(pygame.image.load(filename), (self.w, self.h))
            self.boom_animation.append(img)
