import pygame
import sys
from Screen import Screen
from Menu import Menu
from Missions_Screen import Missions_Screen


class Start_Screen(Screen):

	def run(self):
		self.__main_loop()
		# self.all_game_running = True

	def __leave_game(self):
		self.all_game_running = False
		sys.exit()

	def __set_headling_game(self):
		font = pygame.font.SysFont("Verdana", 45)
		tfs = font.render("Heroes of WWII", True, self.COLORS["black"])
		self.screen.blit(tfs, (self.screen.get_rect().w / 2 - tfs.get_rect().w / 2, 60))

	def __to_missions_screen(self):
		mission_screen = Missions_Screen(self.size, pygame.NOFRAME)
		mission_screen.run()
		mission_screen.return_mission().run()

	def __set_text_menu(self):
		self.menu.add_option("Начать игру", self.__to_missions_screen)
		self.menu.add_option("Выйти из игры", self.__leave_game)

	def __main_loop(self):
		self.menu = Menu()
		self.__set_text_menu()
		while self.running:
			for e in pygame.event.get():
				if e.type == pygame.QUIT or \
						e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
					self.__leave_game()
				if e.type == pygame.KEYDOWN:
					if e.key == pygame.K_UP:
						self.menu.switch(-1)
					if e.key == pygame.K_DOWN:
						self.menu.switch(1)
					if e.key == pygame.K_SPACE:
						self.menu.select()
						if self.menu.current_index == 1:
							self.__leave_game()
					if e.key == pygame.K_ESCAPE:
						self.running = not self.running
						# self.__terminate()
			self.__set_headling_game()
			self.menu.draw(self.screen, 0, 150, 75, True)

			pygame.display.update()

			self.clock.tick(self.FPS)
