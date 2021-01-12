import pygame as pg
import random
from configuracoes import LAYER_PODER, FOGUETÃO


class Poder(pg.sprite.Sprite):

    def __init__(self, game, plat):
        self._layer = LAYER_PODER
        self.grupos = game.sprites_geral, game.poderes
        pg.sprite.Sprite.__init__(self, self.grupos)
        self.game = game
        self.plat = plat
        self.tipo = random.choice(['impulso'])
        self.image = pg.image.load(FOGUETÃO)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top

    def update(self):
        self.rect.bottom = self.plat.rect.top - 2
        self.rect.centerx = self.plat.rect.centerx
        if not self.game.plataformas.has(self.plat):
            self.kill()