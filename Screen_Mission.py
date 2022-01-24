import sys
import pygame
from Screen import Screen
from Menu_Screen_Mission import Menu_Screen_Mission


class Screen_Mission(Screen):

    def __init__(self, size, fl, name, txt, callbacks: dict):
        super().__init__(size, fl)
        self.callbacks = callbacks
        self.name = name
        self.txt = txt

    def run(self):
        self.__main_loop()

    def __set_text_menu(self):
        pygame.font.init()
        name = pygame.font.SysFont("Verdana", 45).render(self.name, True, self.COLORS["black"])
        txt = pygame.font.SysFont("Verdana", 22).render(self.txt, True, self.COLORS["black"])
        self.screen.blit(name, (self.screen.get_rect().w / 2 - name.get_rect().w / 2, 40))
        self.screen.blit(txt, (txt.get_rect(centerx=self.screen.get_width() // 2, y=100)))
        for key in self.callbacks:
            self.menu.add_option(key, self.callbacks[key])

    def __main_loop(self):
        self.menu = Menu_Screen_Mission()
        self.__set_text_menu()
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP:
                        self.menu.switch(-1)
                    if e.key == pygame.K_DOWN:
                        self.menu.switch(1)
                    if e.key == pygame.K_SPACE:
                        self.menu.select().run()
                        self.running = not self.running

            self.menu.draw(self.screen, 0, 150, 75, True)

            self.clock.tick(self.FPS)
            pygame.display.update()
