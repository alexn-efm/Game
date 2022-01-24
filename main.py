import pygame
import Start_Screen


SIZE, FL = (900, 500), pygame.NOFRAME


if __name__ == "__main__":
	start_screen = Start_Screen.Start_Screen(SIZE, FL)
	start_screen.run()
