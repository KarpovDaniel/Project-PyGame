import random
import sys

import pygame
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QBrush, QImage, QPalette
from PyQt5.QtWidgets import QMainWindow, QApplication
from pygame.locals import *

from main import Ui_MainWindow


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.game)
        self.pushButton_3.clicked.connect(self.exit)
        self.pushButton_2.clicked.connect(self.info)
        self.InitUI()

    def InitUI(self):
        self.oImage = QImage("color.jpg")
        self.sImage = self.oImage.scaled(QSize(520, 400))
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


pygame.init()


class DoodleJump:
    def __init__(self):
        self.green = pygame.image.load("data/green.png")
        self.score = score
        self.blue = pygame.image.load("data/blue.png")
        self.red = pygame.image.load("data/red.png")
        self.red_1 = pygame.image.load("data/red_1.png")
        self.playerRight = pygame.image.load("data/right.png")
        self.playerRight_1 = pygame.image.load("data/right_1.png")
        self.playerLeft = pygame.image.load("data/left.png")
        self.playerLeft_1 = pygame.image.load("data/left_1.png")
        self.spring = pygame.image.load("data/spring.png")
        self.spring_1 = pygame.image.load("data/spring_1.png")
        self.direction = 0
        self.camera = camera
        self.position_y = position_y
        self.position_x = position_x
        self.jump = 15
        self.gravity = 0
        self.xmovement = 0
        self.playerx = 400
        self.playery = 400
        self.score = score

    def updatePlayer(self, display):
        self.display = display
        if not self.jump:
            self.position_y += self.gravity
            self.gravity += 1
        elif self.jump:
            self.position_y -= self.jump
            self.jump -= 1
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if self.xmovement < 10:
                self.xmovement += 1
            self.direction = 0

        elif key[K_LEFT]:
            if self.xmovement > -10:
                self.xmovement -= 1
            self.direction = 1
        else:
            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1
        if self.position_x > 850:
            self.position_x = -50
        elif self.position_x < -50:
            self.position_x = 850
        self.position_x += self.xmovement
        if self.position_y - self.camera <= 200:
            self.camera -= 10
        if not self.direction:
            if self.jump:
                self.display.blit(self.playerRight_1, (self.position_x, self.position_y - self.camera))
            else:
                self.display.blit(self.playerRight, (self.position_x, self.position_y - self.camera))
        else:
            if self.jump:
                self.display.blit(self.playerLeft_1, (self.position_x, self.position_y - self.camera))
            else:
                self.display.blit(self.playerLeft, (self.position_x, self.position_y - self.camera))

    def updatePlatforms(self):
        print(1)
        for args in platforms:
            self.mask = pygame.mask.from_surface(self.green)
            if args[0] <= self.position_x <= args[0] + 150 and args[1] <= self.position_y <= args[1] + 50:
                if args[2] != 2:
                    self.jump = 15
                    self.gravity = 0
                else:
                    args[-1] = 1
            if args[2] == 1:
                if args[-1] == 1:
                    args[0] += 5
                    if args[0] > 550:
                        args[-1] = 0
                else:
                    args[0] -= 5
                    if args[0] <= 0:
                        args[-1] = 1

    def drawPlatforms(self, display):
        self.display = display
        for args in platforms:
            print(args)
            check = int(platforms[1][1]) - self.camera
            if check > 600:
                platform = random.randint(0, 1000)
                if platform < 800:
                    platform = 0
                elif platform < 900:
                    platform = 1
                else:
                    platform = 2
                platforms.append([random.randint(0, 700), platforms[-1][1] - 50, platform, 0])
                coords = platforms[-1]
                check = random.randint(0, 1000)
                if check > 900 and platform == 0:
                    springs.append([coords[0], coords[1] - 25, 0])
                platforms.pop(0)
                self.score += 100
            if args[2] == 0:
                display.blit(self.green, (args[0], args[1] - self.camera))
            elif args[2] == 1:
                display.blit(self.blue, (args[0], args[1] - self.camera))
            elif args[2] == 2:
                if not args[3]:
                    display.blit(self.red, (args[0], args[1] - self.camera))
                else:
                    display.blit(self.red_1, (args[0], args[1] - self.camera))

        for spring in springs:
            if spring[-1]:
                display.blit(self.spring_1, (spring[0], spring[1] - self.camera))
            else:
                display.blit(self.spring, (spring[0], spring[1] - self.camera))
            self.mask = pygame.mask.from_surface(self.green)
            if not pygame.sprite.collide_mask(self, DoodleJump):
                self.jump = 50
                self.camera -= 50

    def generatePlatforms(self):
        on = 600
        while on > -100:
            x = random.randint(0, 700)
            platform = random.randint(0, 1000)
            if platform < 800:
                platform = 0
            elif platform < 900:
                platform = 1
            else:
                platform = 2
            platforms.append([x, on, platform, 0])
            on -= 50

    def drawGrid(self, display):
        for x in range(80):
            pygame.draw.line(display, (222, 222, 222), (x * 12, 0), (x * 12, 600))
            pygame.draw.line(display, (222, 222, 222), (0, x * 12), (800, x * 12))


pygame.font.init()
clock = pygame.time.Clock()
position_x = 400
position_y = 400
camera = 0
score = 0
platforms = []
springs = []
font = pygame.font.SysFont("Times New Roman", 25)

doodle = DoodleJump()


def game():
    global score, position_y, position_x, camera, platforms
    size = 800, 600
    screen = pygame.display.set_mode(size)

    doodle.generatePlatforms()
    running = True
    while running:
        screen.fill((255, 255, 255))
        clock.tick(1000)
        screen.blit(font.render(str(score), -1, (0, 0, 0)), (25, 25))
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        if position_y - camera > 700:
            camera = 0
            score = 0
            platforms = platforms([[400, 500, 0, 0]])
            doodle.generatePlatforms()
            position_x = 400
            position_y = 400
        doodle.drawGrid(screen)
        doodle.drawPlatforms(screen)
        doodle.updatePlayer(screen)
        doodle.updatePlatforms()
        pygame.display.flip()


def info():
    pass


app = QApplication(sys.argv)
ex = Main()
ex.show()
sys.exit(app.exec())
