from random import randint
from sys import exit

import pygame
import time
from pygame.locals import *

pygame.mixer.init()
pygame.init()
pygame.display.set_caption('Doodle Jump')


def generate_platform():
    global last_platform
    percent = randint(0, 100)
    if (score % (chastota * 1000) <
            (chastota * 1000 - 300) % (chastota * 1000) <
            (score + 1000) % (chastota * 1000) + 1000):
        last_platform = WhitePlatforms(randint(0, 500), last_platform.rect.y - 50)
    else:
        if percent < 25 and score > 500:
            last_platform = Monsters(randint(0, 500), last_platform.rect.y - 50)
        if percent < 85:
            last_platform = GreenPlatforms(randint(0, 500), last_platform.rect.y - 50)
        elif percent < 95:
            last_platform = BluePlatforms(randint(10, 490), last_platform.rect.y - 50)
        elif percent < 99:
            last_platform = RedPlatforms(randint(0, 500), last_platform.rect.y - 50)
        elif percent == 99 and score > 100:
            last_platform = BlackHoles(randint(0, 500), last_platform.rect.y - 50)


score = 0
chastota = randint(5, 10)


def game_over():
    screen = pygame.display.set_mode((500, 500))
    fon = pygame.image.load("data/image3.jpg")
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 65)
    string_rendered = font.render('Restart', 1, pygame.Color('green'))
    pygame.mouse.set_visible(True)
    rect = string_rendered.get_rect()
    rect.x = 175
    rect.y = 380
    pygame.mixer.music.load("data/gameover.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(1)
    screen.blit(string_rendered, rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 380 < event.pos[1] < rect.h + 380 and 175 < event.pos[0] < rect.w + 175:
                    game()
                    exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    window_answer()
                    pygame.quit()
                    exit(0)


class Doodle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, player)
        self.score = score
        self.image = pygame.image.load("data/doodle.png")
        self.rect = self.image.get_rect()
        self.last_image = self.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 262
        self.rect.y = 390
        self.time = 0
        self.v = 24
        self.direction = 1
        self.gravity = 1

    def update(self):
        global score, prev
        self.v -= self.gravity
        self.rect.y -= self.v
        if self.v < 0:
            for platform in platform_sprites:
                if pygame.sprite.collide_mask(self, platform):
                    if 40 < platform.rect.y - self.rect.y:
                        self.v = 24
                        pygame.mixer.music.load("data/jump.mp3")
                        pygame.mixer.music.set_volume(0.2)
                        pygame.mixer.music.play(1)
                        if prev.rect.y > platform.rect.y:
                            score += randint(75, 130)
                            prev = platform
        if self.v < 0:
            for platform in white_platform_sprites:
                if pygame.sprite.collide_mask(self, platform):
                    if 40 < platform.rect.y - self.rect.y:
                        self.v = 24
                        pygame.mixer.music.load("data/jump.mp3")
                        pygame.mixer.music.set_volume(0.2)
                        pygame.mixer.music.play(1)
                        if prev.rect.y > platform.rect.y:
                            prev = platform
                            score += randint(75, 130)
                        platform.jump()
        for hole in holes_sprites:
            if pygame.sprite.collide_mask(self, hole):
                if 3 < hole.rect.y - self.rect.y:
                    game_over()

        for monster in monster_sprite:
            if pygame.sprite.collide_mask(self, monster):
                if -20 < monster.rect.y - self.rect.y:
                    if self.v >= 0:
                        game_over()
                    else:
                        pygame.mixer.music.load("data/jump.mp3")
                        pygame.mixer.music.set_volume(0.2)
                        pygame.mixer.music.play(1)
                        self.v = 24
                        score += randint(200, 300)
                        monster.kill()
        key = pygame.key.get_pressed()
        if key[K_LEFT]:
            self.image = pygame.image.load("data/doodle.png")
            doodle.rect.x -= 10
        elif key[K_RIGHT]:
            doodle.rect.x += 10
            self.image = pygame.image.load("data/doodle1.png")
        if doodle.rect.x > 620:
            doodle.rect.x = -20
        if doodle.rect.x < -21:
            doodle.rect.x = 619
        if self.v < 0:
            for platform in red_platform_sprites:
                if pygame.sprite.collide_mask(self, platform):
                    if 40 < platform.rect.y - self.rect.y:
                        platform.jump()
        if self.rect.y >= 420:
            game_over()

    def update_pos(self, pos):
        self.rect.x += pos

    def fire(self):
        self.last_image = self.image
        self.image = pygame.image.load("data/doodle_2.png")
        MyFire((doodle.rect.x + doodle.rect.w // 2 + 15, doodle.rect.y))

    def recoil(self):
        self.image = self.last_image


class Monsters(pygame.sprite.Sprite):
    image = pygame.image.load("data/monster.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, monster_sprite)
        self.image = Monsters.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.v = 5

    def update(self):
        self.rect.x += self.v
        if not 0 < self.rect.x < 500:
            self.v = -self.v
        if self.rect.y > 1000:
            self.kill()
            generate_platform()


class WhitePlatforms(pygame.sprite.Sprite):
    image = pygame.image.load("data/glass.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, white_platform_sprites)
        self.image = WhitePlatforms.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        if self.rect.y > 1000:
            self.kill()
            generate_platform()

    def jump(self):
        self.kill()
        dead_platform_sprites.add(self)
        generate_platform()


class GreenPlatforms(pygame.sprite.Sprite):
    image = pygame.image.load("data/green.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, platform_sprites)
        self.image = GreenPlatforms.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        if self.rect.y > 1000:
            self.kill()
            generate_platform()


class BluePlatforms(pygame.sprite.Sprite):
    image = pygame.image.load("data/blue.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, platform_sprites)
        self.image = BluePlatforms.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.v = 5

    def update(self):
        self.rect.x += self.v
        if not 0 < self.rect.x < 500:
            self.v = -self.v
        if self.rect.y > 1000:
            self.kill()
            generate_platform()


class RedPlatforms(pygame.sprite.Sprite):
    image = pygame.image.load("data/red.png")
    image2 = pygame.image.load("data/red_1.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, red_platform_sprites)
        self.image = RedPlatforms.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.gravity = 0
        self.v = 0

    def jump(self):
        self.image = RedPlatforms.image2
        self.gravity = 1
        self.v = 2
        pos_x, pos_y = self.rect.x, self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y + 1

    def update(self):
        self.rect.y += self.v
        self.v += self.gravity
        if self.rect.y > 1000:
            self.kill()
            generate_platform()


class BlackHoles(pygame.sprite.Sprite):
    image = pygame.image.load("data/hole.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, holes_sprites)
        self.image = BlackHoles.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        if self.rect.y > 800:
            self.kill()
            generate_platform()


class Camera:
    def __init__(self):
        self.dy = 0

    def apply(self, obj):
        obj.rect.y += self.dy

    def update(self, target):
        self.dy = 800 // 2 - (target.rect.y + target.rect.h // 2)


player = pygame.sprite.Group()
holes_sprites = pygame.sprite.Group()
platform_sprites = pygame.sprite.Group()
red_platform_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
white_platform_sprites = pygame.sprite.Group()
camera = Camera()
dead_platform_sprites = pygame.sprite.Group()
monster_sprite = pygame.sprite.Group()
doodle = Doodle()
fire = pygame.sprite.Group()
last_platform = 900
font = pygame.font.SysFont("Times New Roman", 25)
prev = GreenPlatforms(200, 850)


def info():
    screen = pygame.display.set_mode((333, 250))
    fon = pygame.image.load("data/fon_1.jpg")
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 46)
    font_info = pygame.font.Font(None, 30)
    string = font.render('Разработчики:', 2, pygame.Color('Red'))
    string_info = font_info.render('1) Александр Максимов', 1, pygame.Color('Black'))
    str_info = font_info.render('2) Зобков Максим', 1, pygame.Color('Black'))
    rect = string_info.get_rect()
    rect_name = str_info.get_rect()
    rect_info = string.get_rect()
    rect.x = 25
    rect.y = 120
    rect_name.x = 25
    rect_name.y = 170
    rect_info.x = 25
    rect_info.y = 40
    screen.blit(string_info, rect)
    screen.blit(str_info, rect_name)
    screen.blit(string, rect_info)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return


class MyFire(pygame.sprite.Sprite):
    player_fire = pygame.image.load("data/fire_doodle.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = MyFire.player_fire
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0] - self.rect.w // 2 - 15
        self.rect.y = pos[1] + 35

    def update(self):
        self.rect.y -= 40
        if self.rect.y < -50:
            self.kill()
        for sprite in monster_sprite:
            if pygame.sprite.collide_mask(self, sprite):
                self.kill()
                sprite.kill()


def game():
    global score, prev
    score = 0
    global player, platform_sprites, red_platform_sprites, all_sprites, \
        doodle, last_platform, holes_sprites, monster_sprite
    size = width, height = 600, 800
    screen = pygame.display.set_mode(size)
    player = pygame.sprite.Group()
    platform_sprites = pygame.sprite.Group()
    holes_sprites = pygame.sprite.Group()
    monster_sprite = pygame.sprite.Group()
    red_platform_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    pygame.mouse.set_visible(False)
    camera = Camera()
    doodle = Doodle()
    last_platform = GreenPlatforms(300, 800)
    prev = GreenPlatforms(300, 800)
    for i in range(30):
        generate_platform()
    fon = pygame.image.load("data/fon.jpg").convert()
    screen.blit(fon, (0, 0))
    clock = pygame.time.Clock()
    MY_EVENT_TYPE = 31
    fire_on = 0
    running = True
    while running:
        screen.blit(fon, (0, 0))
        screen.blit(font.render(str(score), -1, (255, 255, 255)), (25, 25))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window_answer()
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    window_answer()
                    pygame.quit()
                    exit(0)
                if event.key == pygame.K_SPACE:
                    doodle.fire()
                    pygame.time.set_timer(MY_EVENT_TYPE, 600)
                    fire_on = 1
            if fire_on and event.type == MY_EVENT_TYPE:
                fire_on = 0
                doodle.recoil()
        all_sprites.update()
        camera.update(doodle)
        for sprite in all_sprites:
            camera.apply(sprite)
        for sprite in dead_platform_sprites:
            camera.apply(sprite)
        all_sprites.draw(screen)
        player.draw(screen)
        clock.tick(30)
        pygame.display.flip()


def window_answer():
    screen = pygame.display.set_mode((500, 500))
    fon = pygame.image.load("data/fon_main.jpg")
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 44)
    font_exit = pygame.font.Font(None, 65)
    font_yes = pygame.font.Font(None, 64)
    font_no = pygame.font.Font(None, 64)
    font_slash = pygame.font.Font(None, 80)
    string_rendered = font.render('Вернуться в главное меню', 1, pygame.Color('White'))
    string_exit = font_exit.render('Выйти из игры?', 1, pygame.Color('White'))
    string_yes = font_yes.render('Да', 1, pygame.Color('Red'))
    string_slash = font_slash.render('/', 1, pygame.Color('White'))
    string_no = font_no.render('Нет', 1, pygame.Color('Green'))
    pygame.mouse.set_visible(True)
    rect_no = string_no.get_rect()
    rect = string_rendered.get_rect()
    rect_exit = string_exit.get_rect()
    rect_yes = string_yes.get_rect()
    rect_slash = string_slash.get_rect()
    rect.x = 50
    rect.y = 375
    rect_exit.x = 70
    rect_exit.y = 140
    rect_yes.x = 110
    rect_yes.y = 250
    rect_slash.x = 250
    rect_slash.y = 247
    rect_no.x = 340
    rect_no.y = 250
    screen.blit(string_rendered, rect)
    screen.blit(string_exit, rect_exit)
    screen.blit(string_yes, rect_yes)
    screen.blit(string_slash, rect_slash)
    screen.blit(string_no, rect_no)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 375 < event.pos[1] < rect.h + 375 and 50 < event.pos[0] < rect.w + 300:
                    main()
                    exit(0)
                if 250 < event.pos[1] < rect_yes.h + 250 and 110 < event.pos[0] < rect_yes.w + 100:
                    pygame.display.quit()
                    pygame.quit()
                    exit(0)
                if 250 < event.pos[1] < rect.h + 250 and 340 < event.pos[0] < rect.w + 100:
                    game()
                    pygame.quit()
                    exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game()
                    pygame.quit()
                    exit(0)


def main():
    screen = pygame.display.set_mode((500, 500))
    fon = pygame.image.load("data/fon_main.jpg")
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 65)
    font_info = pygame.font.Font(None, 24)
    string_rendered = font.render('Начать игру', 1, pygame.Color('White'))
    string_exit = font.render('Выход', 1, pygame.Color('White'))
    string_info = font_info.render('О разработчиках', 1, pygame.Color('Grey'))
    pygame.mouse.set_visible(True)
    rect = string_rendered.get_rect()
    rect_exit = string_exit.get_rect()
    rect_info = string_info.get_rect()
    rect.x = 125
    rect.y = 180
    rect_exit.x = 175
    rect_exit.y = 300
    rect_info.x = 350
    rect_info.y = 450
    pygame.mixer.music.load("data/falling.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 180 < event.pos[1] < rect.h + 180 and 125 < event.pos[0] < rect.w + 175:
                    pygame.mixer_music.stop()
                    game()
                    pygame.mixer_music.play()
                if 300 < event.pos[1] < rect.h + 300 and 175 < event.pos[0] < rect.w + 175:
                    exit(0)
                if 450 < event.pos[1] < rect.h + 450 and 350 < event.pos[0] < rect.w + 350:
                    info()
            screen = pygame.display.set_mode((500, 500))
            screen.blit(fon, (0, 0))
            pygame.mouse.set_visible(True)
            screen.blit(string_rendered, rect)
            screen.blit(string_exit, rect_exit)
            screen.blit(string_info, rect_info)
            pygame.display.flip()


main()
