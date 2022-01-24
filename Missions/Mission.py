import sys
import pygame
import io
import os
import random
import Start_Screen
from Screen import Screen
from Sprites.Player_Aircraft import Player_Aircraft
from Sprites.Enemy_Aircraft import Enemy_Aircraft
from Sprites.Tile import Tile
from Sprites.Boom import Boom
from Screen_Mission import Screen_Mission


class Mission(Screen):

    def __init__(self, size, fl, map_path, player_img_path):
        Screen.__init__(self, size, fl)
        pygame.mixer.init()
        self.player_img_path = player_img_path
        self.fl = fl
        self.map_path = map_path
        self.enemy_imgs_path = self.__load_enemies_path()
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.dynamic_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.player = Player_Aircraft(self.__get_player_pos()[0], self.__get_player_pos()[1], self.dynamic_sprites,
                                      self.all_sprites, self.player_img_path, 8)
        self.buildings = self.__load_buildings_path()
        self.enemy_count = 0
        self.boom_player_sound = pygame.mixer.Sound("Sounds/boom.mp3")
        self.boom_enemy_sound = pygame.mixer.Sound("Sounds/shoot_1.mp3")
        self.txt = "Защитите аэродром от вражеских самолётов!"
        self.last_tick = pygame.time.get_ticks()

    def __set_first_txt(self):
        now = pygame.time.get_ticks()
        txt = pygame.font.SysFont("Verdana", 30).render(self.txt, True, self.COLORS["gray"])
        self.screen.blit(txt, txt.get_rect(center=(self.screen.get_rect().w / 2, self.screen.get_rect().h / 2 - 60)))
        if now - self.last_tick > 2000:
            pygame.draw.rect(self.screen, self.COLORS["white"], txt.get_rect(
                center=(self.screen.get_rect().w / 2, self.screen.get_rect().h / 2 - 60)))

    def __load_enemies_path(self):
        for root, dirs, files in os.walk("imgs/Enemies"):
            return files

    def __load_buildings_path(self):
        for root, dirs, files in os.walk("imgs/Buildings"):
            return files

    def __get_player_pos(self):
        with io.open(self.map_path) as f:
            level = [x.rstrip("\n") for x in f]
        for y in range(len(level)):
            for x, el in enumerate(level[y]):
                if el == "*":
                    return (x - 1) * 70, y * 50

    def load_map(self):
        with io.open(self.map_path) as f:
            level = [x.rstrip("\n") for x in f]
        for y in range(len(level)):
            for x, el in enumerate(level[y]):
                if el == "<":
                    self.__create_enemy((x - 1) * 125, y * 50, "imgs/Enemies/" + random.choice(self.enemy_imgs_path))
                    self.enemy_count += 1
                elif el == "|":
                    self.__create_tile((x - 1) * 125, y * 50, 10, 50)
                elif el == "_":
                    self.__create_tile((x - 1) * 125, y * 50, 125, 50)
                elif el == "-":
                    self.__create_tile((x - 1) * 125, y * 45, 125, 60, "imgs/Plants/grass.png")
                elif el == "!":
                    self.__create_tile((x - 1) * 125, (y - 2) * 50, 200, 200, "imgs/waterTower.png")
                elif el == "\\":
                    self.__create_tile((x - 1) * 125, (y - 4) * 50, 125, 250, "imgs/Tower.png")
                elif el == "^":
                    self.__create_tile((x - 1) * 125, (y - 2) * 50, 125, 150, "imgs/Plants/spruce.png")
                elif el == "?":
                    self.__create_tile((x - 1) * 125, (y - 2) * 60, 125, 100, "imgs/Buildings/" +
                                       random.choice(self.buildings))

    def __terminate(self, screen):
        self.player.engine_sound.stop()
        self.screen.fill(self.COLORS["white"])
        screen.run()
        self.running = not self.running

    def __draw_enemy_count(self):
        pygame.font.init()
        blade_icon = pygame.image.load("imgs/Icons/blade.png")
        txt = pygame.font.SysFont("Verdana", 20).render(str(self.enemy_count), True, self.COLORS["black"])
        self.screen.blit(blade_icon, blade_icon.get_rect(centerx=200, centery=30))
        self.screen.blit(txt, txt.get_rect(centerx=230, centery=30))

    def __check_win(self):
        if 400 <= self.player.rect.y >= 390 and self.enemy_count == 0 and self.player.power < 5:
            self.__terminate(self.win_screen)

    def __check_lose(self):
        for enemy in self.enemy_sprites:
            if enemy.rect.x < 0:
                self.__create_lose_screen("Противник уничтожил наш аэродром")
                self.__lose()

    def __lose(self):
        pygame.mixer.find_channel(True).play(self.boom_player_sound)
        self.player.crush()
        self.__terminate(self.lose_screen)

    def __create_lose_screen(self, txt):
        self.lose_screen = Screen_Mission(self.size, self.fl, "Миссия провалена!", txt, {
            "Начать заново": lambda: Mission(self.size, self.fl, self.map_path, self.player_img_path,),
            "Выйти в меню": lambda: Start_Screen.Start_Screen(self.size, self.fl)
        })

    def __add_to_dynamic_sprites(self, sprite):
        self.all_sprites.add(sprite)
        self.dynamic_sprites.add(sprite)

    def __create_tile(self, x, y, w, h, img_path=None):
        if img_path:
            self.__add_to_dynamic_sprites(Tile(x, y, w, h, img_path))
        else:
            self.__add_to_dynamic_sprites(Tile(x, y, w, h))

    def __player_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.start_engine()
        if keys[pygame.K_s]:
            self.player.off_engine()
        if keys[pygame.K_UP]:
            self.player.update_pitch(1)
        if keys[pygame.K_DOWN]:
            self.player.update_pitch(-1)

    def __create_enemy(self, x, y, img_path):
        enemy = Enemy_Aircraft(x, y, img_path)
        self.__add_to_dynamic_sprites(enemy)
        self.enemy_sprites.add(enemy)

    def __collide_player_and_dynamic_sprites(self):
        hits = pygame.sprite.spritecollide(self.player, self.dynamic_sprites, False)
        for hit in hits:
            if type(hit) is not Boom:
                self.__create_lose_screen("Разбился")
                self.__lose()
                break
            if type(hit) is Enemy_Aircraft:
                hit.kill()
                self.__create_lose_screen("Разбился")
                self.__lose()
                break

    def __collide_bullets_and_enemies(self):
        hits = pygame.sprite.groupcollide(self.enemy_sprites, self.bullets, True, True)
        for hit in hits:
            self.__add_to_dynamic_sprites(Boom(hit.rect.centerx, hit.rect.y - hit.rect.w / 2 / 2, 150, 150))
            self.enemy_count -= 1
            pygame.mixer.music.load("Sounds/boom_enemy.mp3")
            pygame.mixer.music.play()

    def __collide_bullets_and_tiles(self):
        hits = pygame.sprite.groupcollide(self.dynamic_sprites, self.bullets, False, True)
        for hit in hits:
            if type(hit) is not Boom:
                self.__add_to_dynamic_sprites(Boom(hit.rect.x, hit.rect.y, hit.rect.w, hit.rect.h))
                pygame.mixer.music.load("Sounds/boom_enemy.mp3")
                pygame.mixer.music.play()

    def __check_collides(self):
        self.__collide_bullets_and_enemies()
        self.__collide_bullets_and_tiles()
        self.__collide_player_and_dynamic_sprites()

    def run(self):
        self.__main_loop()

    def __main_loop(self):

        self.win_screen = Screen_Mission(self.size, self.fl, "Миссия выполнена!", "Все цели уничтожены", {
            "Начать заново": lambda: Mission(self.size, self.fl, self.map_path, self.player_img_path),
            "Выйти в меню": lambda: Start_Screen.Start_Screen(self.size, self.fl)
        })

        self.load_map()

        self.all_sprites.add(self.player)

        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    self.player.shoot(self.bullets, self.all_sprites)

            self.screen.fill(self.COLORS["white"])

            self.__set_first_txt()

            self.player.draw_player_info(self.screen)

            self.__check_win()
            self.__check_lose()

            self.__draw_enemy_count()

            self.__player_events()

            self.__check_collides()

            self.all_sprites.draw(self.screen)

            self.clock.tick(self.FPS)
            pygame.display.update()

            self.all_sprites.update()
