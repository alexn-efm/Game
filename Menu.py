import pygame


class Menu:

    def __init__(self) -> None:
        self.font = pygame.font.SysFont("Verdana", 30)
        self._options = []
        self._callbacls = []
        self.current_index = 0

    def add_option(self, txt, callback, color=(0, 0, 0), select_color=(200, 200, 200)):
        self.select_color = select_color
        self._options.append(self.font.render(txt, True, color))
        self._callbacls.append(callback)

    def switch(self, vector):
        self.current_index = max(0, min(self.current_index + vector, len(self._options) - 1))

    def select(self):
        self._callbacls[self.current_index]()

    def draw(self, surf, x, y, padding_y, center=False):

        for i, opt in enumerate(self._options):
            opt_rect = opt.get_rect()
            if center:
                opt_rect.topleft = (surf.get_rect().w / 2 - opt_rect.w / 2, y + i * padding_y)
            else:
                opt_rect.topleft = (x, y + i * padding_y)
            if i == self.current_index:
                pygame.draw.rect(surf, self.select_color, opt_rect)
            else:
                pygame.draw.rect(surf, (255, 255, 255), opt_rect)
            surf.blit(opt, opt_rect)

    def get_opt_rects(self):
        return [opt.get_rect() for opt in self._options]
