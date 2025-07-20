import pygame as pg
import random
from src.game.objetos import Poder
from src.configuracoes import (
    LAYER_PLATAFORMA,
    PLATAFORMA_FASE1,
    PLATAFORMA_FASE2,
    PLATAFORMA_FASE3,
    PLATAFORMA_FASE4,
    PLATAFORMA_INICIAL,
    PLATAFORMA_RARA,
    ASTEROIDES,
)


class Plataforma(pg.sprite.Sprite):

    def __init__(self, game, x, y, fase):
        self._layer = LAYER_PLATAFORMA
        self.grupos = game.sprites_geral, game.plataformas
        pg.sprite.Sprite.__init__(self, self.grupos)
        self.game = game
        if fase == 4:
            self.image = pg.image.load(random.choice(ASTEROIDES))
        elif fase == 3:
            if random.random() < 0.05:
                self.image = pg.image.load(PLATAFORMA_RARA)
            else:
                self.image = pg.image.load(random.choice(PLATAFORMA_FASE3))
        elif fase == 2:
            self.image = pg.image.load(random.choice(PLATAFORMA_FASE2))
        elif fase == 1:
            self.image = pg.image.load(random.choice(PLATAFORMA_FASE1))
        elif fase == -1:
            self.image = pg.image.load(PLATAFORMA_INICIAL)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if random.randrange(100) < self.game.freq_poder:
            Poder.Poder(self.game, self)
