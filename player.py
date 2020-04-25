import math

import pygame


class Player():
    playerImg = pygame.image.load('images/player.png')
    X = 0
    Y = 0
    Xvel = 0
    Yvel = 0
    playerlife = 0
    def __init__(self):
        self.X = 360
        self.Y = 480
        self.Xvel = 0
        self.Yvel = 0
        self.playerlife = 5

    def isDead(self):
        if self.playerlife <= 1:
            return True
        else:
            return False
    def playerhit(self):
        self.playerlife -= 1