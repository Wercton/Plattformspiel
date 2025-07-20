import pygame as pg
from src.configuracoes import SPACEX_CARRO, LAYER_NUVENS, BLACK, WIDTH, HEIGHT


class Astronaut(pg.sprite.Sprite):

    def __init__(self, game):

        self._layer = LAYER_NUVENS
        self.grupos = game.sprites_geral, game.cometa
        pg.sprite.Sprite.__init__(self, self.grupos)
        self.game = game

        self.image = pg.image.load(SPACEX_CARRO)

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = -10
        self.vel = 1

        self.ultima_mudanca = 0
        self.frame_atual = 0

    def update(self):

        agora = pg.time.get_ticks()
        if agora - self.ultima_mudanca > 100:
            self.rect.x -= self.vel
            self.ultima_mudanca = agora
        if self.rect.top > HEIGHT:
            self.kill()
