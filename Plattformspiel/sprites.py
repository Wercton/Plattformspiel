# classes de sprite para o jogo
import pygame as pg
from configuracoes import *
vec = pg.math.Vector2

class Jogador(pg.sprite.Sprite):

    def __init__(self):

        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load(JOGADOR_SPRITE), TAMANHO_JOGADOR)
        self.rect = self.image.get_rect()
        self.rect.center = (POSICAO_INICIAL)
        self.pos = vec(POSICAO_INICIAL)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.andando = False
        self.frame_atual = 0
        self.ultima_mudanca = 0
        self.carregar_imagens()

    def update(self):

        self.animar()
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

    def carregar_imagens(self):

        self.frame_pular_l = pg.transform.scale(pg.image.load(PULO_SPRITE), TAMANHO_JOGADOR)
        self.frame_pular_r = pg.transform.flip(self.frame_pular_l, True, False)

        self.frame_parado_l = [pg.transform.scale(pg.image.load(JOGADOR_SPRITE), TAMANHO_JOGADOR),
                            pg.transform.scale(pg.image.load(JOGADOR_SPRITE2), TAMANHO_JOGADOR)]
        self.frame_parado_r = []
        for frame in self.frame_parado_l:
            self.frame_parado_r.append(frame)

        self.frame_andar_r = [pg.transform.scale(pg.image.load(ANDAR1_SPRITE), TAMANHO_JOGADOR),
                            pg.transform.scale(pg.image.load(ANDAR2_SPRITE), TAMANHO_JOGADOR)]
        self.frame_andar_l = []
        for frame in self.frame_andar_r:
            self.frame_andar_l.append(pg.transform.flip(frame, True, False))

        self.frame_cair = pg.transform.scale(pg.image.load(CAIR_SPRITE), TAMANHO_JOGADOR)


    def animar(self):

        agora = pg.time.get_ticks()
        if self.vel.y < 0:
            self.image = self.frame_pular_l
        elif self.vel.y > 0:
            self.image = self.frame_cair
        elif not self.andando:
            if agora - self.ultima_mudanca > 500:
                self.ultima_mudanca = agora
                self.frame_atual = (self.frame_atual + 1) % len(self.frame_parado_l) # BOOOOM
                self.image = self.frame_parado_l[self.frame_atual]





class Plataforma(pg.sprite.Sprite):

    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
