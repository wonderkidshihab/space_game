import math
import random as rand

import pygame
from pygame import mixer

from enemy import Enemy
from player import Player


class mainGame():
    playing = False
    music = True
    bulletImg = pygame.image.load('images/bullet.png')
    bulletX = 0
    bulletY = 0
    bulletXvel = 0
    bulletYvel = 0
    bulletState = False
    score = 0
    lastAddedEnemyScore = 0
    highscore = 0
    enemies = []
    enemycount = 5
    for i in range(enemycount):
        enemies.append(Enemy())
    # self.screen
    width, height = 800, 600
    screen = pygame.display.set_mode((width,height))
    pygame.init()
    # Images
    icon = pygame.image.load('images/game-icon.png')
    backgroundImg = pygame.image.load('images/background.png')

    pygame.display.set_caption("Space Game")
    pygame.display.set_icon(icon)
    font = pygame.font.Font("fonts/bigspace.ttf", 32)
    scorefont = pygame.font.Font("fonts/bigspace.ttf", 70)
    highscorefont = pygame.font.Font("fonts/bigspace.ttf", 50)
    player = Player()
    mixer.music.load('audio/background.wav')
    mixer.music.play(-1)
    bulletSound = mixer.Sound('audio/laser.wav')
    explosionSound = mixer.Sound('audio/explosion.wav')

    def inisialize(self):
        self.bulletX = 0
        self.bulletY = 0
        self.bulletXvel = 0
        self.bulletYvel = 0
        self.bulletState = False
        self.score = 0
        self.player.playerlife = 5
        self.enemies = []
        for i in range(5):
            self.enemies.append(Enemy())
        self.playing = True

    def play(self):

        if rand.randint(0, 10) <= 1 and len(self.enemies) < self.enemycount:
            self.enemies.append(Enemy())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.Xvel = -5
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.Xvel = 5
                if event.key == pygame.K_m:
                    if self.music:
                        self.music = False
                        mixer.music.set_volume(0)
                        self.bulletSound.set_volume(0.0)
                        self.explosionSound.set_volume(0.0)
                    else:
                        self.music = True
                if event.key == pygame.K_SPACE and self.bulletState is not True:
                    self.bulletX = self.player.X
                    self.fireBullet(self.bulletX + 32, self.bulletY + 25)
                    self.bulletSound.play()
                    self.bulletYvel = -7.5
                if event.key == pygame.K_RETURN:
                    self.enemies.clear()
                    self.inisialize()
                    self.playing = True
            if event.type == pygame.KEYUP:
                self.player.Xvel = 0.0

        if self.playing:

            if self.player.X <= 0:
                self.player.X = 0
            elif self.player.X >= self.width - 64:
                self.player.X = self.width - 64

            self.player.X += self.player.Xvel
            self.player.Y += self.player.Yvel

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.backgroundImg, (0, 0))

            self.screen.blit(self.player.playerImg, (self.player.X, self.player.Y))
            self.screen.blit(self.font.render("Score: " + str(self.score), True, (240, 240, 255)), (10, 10))
            self.screen.blit(self.font.render("Life: " + str(self.player.playerlife), True, (240, 240, 255)), (10, 50))

            if self.bulletY <= 0:
                self.bulletY = self.player.Y
                self.bulletState = False
            if self.bulletState:
                self.fireBullet(self.bulletX, self.bulletY)
                self.bulletY += self.bulletYvel
            for enemy in self.enemies:
                enemy.show(enemy.X, enemy.Y)
                enemy.update()
                if self.iscollided(enemy.X, self.bulletX, enemy.Y, self.bulletY):
                    self.explosionSound.play()
                    self.bulletState = False
                    self.bulletY = self.player.Y
                    if self.score - self.lastAddedEnemyScore == 10:
                        self.enemycount += 1
                        self.lastAddedEnemyScore = self.score
                    self.score += 1

                    if self.highscore < self.score:
                        self.highscore = self.score
                    self.enemies.remove(enemy)
                    self.enemies.append(Enemy())
                if enemy.Y >= 440:
                    if self.player.isDead():
                        self.playing = False
                    else:
                        self.enemies.remove(enemy)
                        self.enemies.append(Enemy())
                        self.player.playerhit()

        else:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.scorefont.render("Score: " + str(self.score), True, (240, 240, 255)), (250, 200))
            self.screen.blit(self.highscorefont.render("HighScore: " + str(self.highscore), True, (240, 240, 255)),
                             (250, 300))
            self.screen.blit(self.font.render("Press ENTER to play", True, (240, 240, 255)),
                             (250, 400))
        pygame.display.update()

    def fireBullet(self, x, y):
        self.bulletState = True
        self.screen.blit(self.bulletImg, (x, y))

    def iscollided(self, x1, x2, y1, y2):
        distance = math.hypot(x1 - x2, y1 - y2)
        if distance < 50 and self.bulletState:
            return True
        else:
            return False
