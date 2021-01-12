import pygame as pg
import random


class Spritesheet:

    def __init__(self, filename):

        self.spritesheet = pg.image.load(filename).convert()

    def selecionar_imagem(self, x, y, width, height):

        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image