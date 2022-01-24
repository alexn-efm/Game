# -*- coding: cp1251 -*-
import sys
import pygame
import Start_Screen
from Screen import Screen
from Missions_Menu import Missions_Menu
from Missions.Mission import Mission


SIZE, FL = (900, 500), pygame.NOFRAME


class Missions_Screen(Screen):

    def run(self):
        self.__main_loop()

    def __set_options(self):
        self.missions_menu.add_mission("1", lambda: Mission(SIZE, FL, "maps/1.txt", "imgs/p47t.png"))
        self.missions_menu.add_mission("2", lambda: Mission(SIZE, FL, "maps/2.txt", "imgs/p47t.png"))

    def __terminate(self):
        self.running = not self.running

    def __main_loop(self):
        self.returned = False
        self.missions_menu = Missions_Menu()
        self.__set_options()
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RIGHT:
                        self.missions_menu.switch(1)
                    if e.key == pygame.K_LEFT:
                        self.missions_menu.switch(-1)
                    if e.key == pygame.K_SPACE:
                        self.returned = True
                        self.running = not self.running
                    if e.key == pygame.K_ESCAPE:
                        self.running = not self.running

            self.missions_menu.set_headling(self.screen, "Миссии")
            self.missions_menu.draw(self.screen)

            pygame.display.update()
            self.clock.tick(self.FPS)

    def return_mission(self):
        if self.returned:
            return self.missions_menu.select()
        else:
            return Start_Screen.Start_Screen(self.size, self.fl)
