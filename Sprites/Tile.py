import pygame


class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h, filename=False):
        pygame.sprite.Sprite.__init__(self)
        if not filename:
            self.image = pygame.Surface((w, h))
            self.image.fill((0, 0, 0))
        else:
            self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
