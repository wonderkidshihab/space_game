import random as rand

import pygame

screen = pygame.display.set_mode((800, 600))


class Enemy():
    # enemy
    enemyImg = pygame.image.load('images/enemy.png')
    X, Y, Xvel, Yvel = (0, 0, 0, 0)

    def __init__(self):
        self.X = rand.randint(10, 800 - 64)
        self.Y = rand.randint(-120,-70)
        self.Xvel = rand.randint(3, 8)
        self.Yvel = rand.randint(5, 8)/10

    def show(self, x, y):
        screen.blit(self.enemyImg, (x, y))

    def update(self):
        if self.X <= 0:
            self.Xvel *= -1
        elif self.X >= 800 - 64:
            self.Xvel *= -1

        self.X += self.Xvel
        self.Y += self.Yvel
