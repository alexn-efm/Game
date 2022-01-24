import pygame


class Enemy_Aircraft(pygame.sprite.Sprite):

    def __init__(self, x, y, img_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
