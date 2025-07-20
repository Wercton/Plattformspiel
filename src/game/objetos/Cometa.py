import pygame as pg
from src.configuracoes import COMETA1, COMETA2, BLACK, LAYER_NUVENS, WIDTH, HEIGHT


class Cometa(pg.sprite.Sprite):

    def __init__(self, game):

        self._layer = LAYER_NUVENS
        self.grupos = game.sprites_geral, game.cometa
        pg.sprite.Sprite.__init__(self, self.grupos)
        self.game = game

        self.imagens = [pg.image.load(COMETA1), pg.image.load(COMETA2)]
        self.image = self.imagens[0]
        self.image.set_colorkey(BLACK)

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
            self.rect.y += self.vel
            self.ultima_mudanca = agora
            self.frame_atual = not self.frame_atual
            self.image = self.imagens[self.frame_atual]
        if self.rect.top > HEIGHT:
            self.kill()
