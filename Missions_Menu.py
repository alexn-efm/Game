import pygame

class Missions_Menu:

	def __init__(self):
		pygame.font.init()
		self.font = pygame.font.SysFont("Verdana", 20)
		self._levels = []
		self._callbacks = []
		self._current_index = 0

	def __create_two_dimensional_list(self, arr):
		ret_arr = []
		for i in range(len(arr)):
			if i % 8 == 0 and i != 0:
				ret_arr.append("|")
			ret_arr.append(arr[i])
		return [[x for x in a.split(" ") if x] for a in " ".join(ret_arr).split("|")]

	def set_headling(self, surf, txt, color=(0, 0, 0)):
		pygame.font.init()
		txt = pygame.font.SysFont("Verdana", 25).render(txt, True, color)
		surf.blit(txt, txt.get_rect(center=(surf.get_rect().w / 2, 35)))

	def add_mission(self, level_name: str, callback, color=(0, 0, 0), select_color=(200, 200, 200)):
		self.select_color = select_color
		self.color = color
		self._levels.append(level_name)
		self._callbacks.append(callback)
		self.arr = self.__create_two_dimensional_list(self._levels)

	def switch(self, vector):
		self._current_index = max(0, min(self._current_index + vector, len(self._levels) - 1))

	def select(self):
		return self._callbacks[self._current_index]()

	def draw(self, surf):
		a = 75
		for y in range(len(self.arr)):
			for x in range(len(self.arr[y])):
				if self._levels.index(self.arr[y][x]) == self._current_index:
					pygame.draw.rect(surf, self.select_color, (x * (a + a / 2) + a / 2 / 2, y * (a + a / 2) + a + a / 4, 75, 75), 2, 10)
					txt = self.font.render(self.arr[y][x], True, self.select_color)
					txt_rect = txt.get_rect(center=(x * (a + a / 2) + a / 2, y * (a + a / 2) + a + a / 2))
				else:
					pygame.draw.rect(surf, self.color, (x * (a + a / 2) + a / 2 / 2, y * (a + a / 2) + a + a / 4, 75, 75), 1, 10)
					txt = self.font.render(self.arr[y][x], True, self.color)
					txt_rect = txt.get_rect(center=(x * (a + a / 2) + a / 2, y * (a + a / 2) + a + a / 2))
				surf.blit(txt, txt_rect)
