import pygame


class Fire(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imgs/fire.png")
        self.rect = self.image.get_rect(x=x, y=y)
        self.last_tick = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_tick > 80:
            self.kill()
