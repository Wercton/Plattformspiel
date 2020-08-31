# classes de sprite para o jogo
import pygame as pg
from configuracoes import *
vec = pg.math.Vector2

class Jogador(pg.sprite.Sprite):

    def __init__(self):

        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load(JOGADOR_SPRITE), TAMANHO_JOGADOR)
        # self.rect = pg.Rect(POSICAO_INICIAL, TAMANHO_JOGADOR)
        self.rect = self.image.get_rect()
        self.rect.center = (POSICAO_INICIAL)
        self.pos = vec(POSICAO_INICIAL)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):

        self.acc = vec(0, GRAVIDADE_JOGADOR)
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.acc.x = -ACC_JOGADOR
        elif keys[pg.K_RIGHT]:
            self.acc.x = ACC_JOGADOR

        # aplica fricção
        self.acc.x += self.vel.x * FRICCAO_JOGADOR  # definido no x para não atrapalhar gravidade
        # equação de movimento
        self.vel += self.acc
        self.pos += self.vel + ACC_JOGADOR * self.acc
        # dando a volta na tela
        if self.pos.x > WIDTH:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def pular(self):
        if not self.vel.y: # se 0, verdadeiro
            self.vel.y = -PULO_JOGADOR


class Plataforma(pg.sprite.Sprite):

    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
