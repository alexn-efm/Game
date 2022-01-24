import pygame


class Screen:

	FPS = 60
	COLORS = {
		"white": (255, 255, 255),
		"black": (0, 0, 0),
		"gray": (128, 128, 128)
		}

	def __init__(self, size, fl) -> None:
		pygame.init()
		pygame.font.init()
		self.screen = pygame.display.set_mode(size, fl)
		self.clock = pygame.time.Clock()
		self.running = True
		self.size = size
		self.fl = fl
		self.screen.fill(self.COLORS["white"])
