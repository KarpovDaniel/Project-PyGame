from random import randint
from sys import exit, argv

import pygame
from PyQt5.QtGui import QBrush, QImage, QPalette
from PyQt5.QtWidgets import QMainWindow, QApplication
from pygame.locals import *

from main import Ui_MainWindow

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
        if percent < 82:
            last_platform = GreenPlatforms(randint(0, 500), last_platform.rect.y - 50)
        elif percent < 92:
            last_platform = BluePlatforms(randint(0, 500), last_platform.rect.y - 50)
        elif percent < 98:
            last_platform = RedPlatforms(randint(0, 500), last_platform.rect.y - 50)
        else:
            last_platform = BlackHoles(randint(0, 500), last_platform.rect.y - 50)


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.game)
        self.pushButton_3.clicked.connect(self.exit)
        self.pushButton_2.clicked.connect(self.info)
        self.InitUI()

    def InitUI(self):
        self.sImage = QImage("data/color.jpg")
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(self.sImage))
        self.setPalette(self.palette)

    def game(self):
        self.hide()
        game()

    def exit(self):
        self.hide()
        exit(0)

    def info(self):
        self.hide()
        info()


score = 0
chastota = randint(5, 10)


class Doodle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, player)
        self.score = score
        self.image = pygame.image.load("data/doodle.png")
        self.image2 = pygame.transform.flip(self.image, 1, 0)
        self.rect = self.image.get_rect()
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
                        if prev.rect.y > platform.rect.y:
                            score += randint(75, 130)
                            prev = platform
        if self.v < 0:
            for platform in white_platform_sprites:
                if pygame.sprite.collide_mask(self, platform):
                    if 40 < platform.rect.y - self.rect.y:
                        self.v = 24
                        if prev.rect.y > platform.rect.y:
                            prev = platform
                            score += randint(75, 130)
                        platform.jump()
        for hole in holes_sprites:
            if pygame.sprite.collide_mask(self, hole):
                if 1 < hole.rect.y - self.rect.y:
                    game_over()
        key = pygame.key.get_pressed()
        if key[K_LEFT]:
            doodle.rect.x -= 10
            self.direction = 1
        elif key[K_RIGHT]:
            doodle.rect.x += 10
            self.direction = 0
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
            pygame.display.quit()
            game_over()

    def update_pos(self, pos):
        self.rect.x += pos


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
doodle = Doodle()
last_platform = 900
font = pygame.font.SysFont("Times New Roman", 25)
prev = GreenPlatforms(200, 850)
monster_sprites = pygame.sprite.Group()


def game():
    global score, prev
    score = 0
    global player, platform_sprites, red_platform_sprites, all_sprites, \
        doodle, last_platform, holes_sprites
    size = width, height = 600, 800
    screen = pygame.display.set_mode(size)
    player = pygame.sprite.Group()
    platform_sprites = pygame.sprite.Group()
    holes_sprites = pygame.sprite.Group()
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
    running = True
    while running:
        screen.blit(fon, (0, 0))
        screen.blit(font.render(str(score), -1, (255, 255, 255)), (25, 25))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit()
                    main()
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
                if 380 < event.pos[1] < rect.h + 380 and 175 < event.pos[0] < rect.w + 180:
                    pygame.display.quit()
                    game()
                    pygame.quit()
                    exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    game()
                    pygame.quit()
                    exit(0)


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


def main():
    ex = Main()
    ex.show()
    exit(404)


app = QApplication(argv)
ex = Main()
ex.show()
exit(app.exec())
