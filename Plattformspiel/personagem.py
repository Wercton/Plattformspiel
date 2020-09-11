import pygame as pg
import random
from configuracoes import *

vec = pg.math.Vector2

class Jogador(pg.sprite.Sprite):

    def __init__(self, game):
        self._layer = LAYER_JOGADOR
        self.grupos = game.sprites_geral
        pg.sprite.Sprite.__init__(self, self.grupos)
        self.game = game
        self.image = pg.transform.scale(self.game.jogador_spritesheet.selecionar_imagem(0, 0, 46, 50), TAMANHO_JOGADOR)
        self.rect = self.image.get_rect()
        self.rect.center = (POSICAO_INICIAL)
        self.pos = vec(POSICAO_INICIAL)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.gravidade = GRAVIDADE_JOGADOR
        self.pulando = False

        self.andando = False
        self.frame_atual = 0
        self.ultima_mudanca = 0
        self.direita = True
        self.carregar_imagens()


    def update(self):

        self.rect.midbottom = self.pos

        self.animar()
        self.acc = vec(0, self.gravidade)
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.acc.x = -ACC_JOGADOR
            self.direita = False
            self.andando = True
        elif keys[pg.K_RIGHT]:
            self.acc.x = ACC_JOGADOR
            self.direita = True
            self.andando = True
        else:
            self.andando = False


        # aplica fricção
        self.acc.x += self.vel.x * FRICCAO_JOGADOR  # definido no x para não atrapalhar gravidade
        # equação de movimento
        self.vel += self.acc
        if abs(self.vel.x) < 0.6:  # consertando bug no sprite que sempre andava
            self.vel.x = 0
        self.pos += self.vel + ACC_JOGADOR * self.acc
        # dando a volta na tela
        hits = pg.sprite.spritecollide(self, self.game.plataformas, False)
        if len(hits) == 0:
            if self.pos.x > WIDTH + TAMANHO_JOGADOR[1] / 2:
                self.pos.x = 0 - TAMANHO_JOGADOR[1] / 2
            elif self.pos.x < 0 - TAMANHO_JOGADOR[1] / 2:
                self.pos.x = WIDTH

        self.rect.midbottom = self.pos


    def pular(self):

        if not self.vel.y: # se 0, verdadeiro
            self.game.canal_efeito.play(self.game.audio_pulo)
            self.pulando = True
            self.vel.y = -PULO_JOGADOR


    def interromper_pulo(self):

        if self.pulando:
            if self.vel.y < -3:
                self.vel.y = -3


    def carregar_imagens(self):

        self.frame_esquerda = []
        for i in range(6):
            self.frame_esquerda.append(pg.transform.scale(self.game.jogador_spritesheet.selecionar_imagem(0, 50*i, 46, 50), TAMANHO_JOGADOR))
            self.frame_esquerda[i].set_colorkey(BLACK)

        self.frame_direita = []
        for i in range(6):
            self.frame_direita.append(pg.transform.scale(self.game.jogador_spritesheet.selecionar_imagem(46, 50*i, 46, 50), TAMANHO_JOGADOR))
            self.frame_direita[i].set_colorkey(BLACK)

        self.frame_parado_l = [self.frame_esquerda[0], self.frame_esquerda[1]]
        self.frame_parado_r = [self.frame_direita[0], self.frame_direita[1]]

        self.frame_andar_l = [self.frame_esquerda[2], self.frame_esquerda[3]]
        self.frame_andar_r = [self.frame_direita[2], self.frame_direita[3]]

        self.frame_pular_l = self.frame_esquerda[4]
        self.frame_pular_r = self.frame_direita[4]

        self.frame_cair_l = self.frame_esquerda[5]
        self.frame_cair_r = self.frame_direita[5]


    def animar(self):

        agora = pg.time.get_ticks()

        if self.vel.y < 0:  # pulando
            if self.direita:
                self.image = self.frame_pular_r
            else:
                self.image = self.frame_pular_l
        elif self.vel.y > 0:  # caindo
            if self.direita:
                self.image = self.frame_cair_r
            else:
                self.image = self.frame_cair_l
        elif self.vel.x != 0:  # andando
            if agora - self.ultima_mudanca > 150:
                if self.direita:
                    self.ultima_mudanca = agora
                    self.frame_atual = (self.frame_atual + 1) % len(self.frame_andar_r) # BOOOOM
                    self.image = self.frame_andar_r[self.frame_atual]
                else:
                    self.ultima_mudanca = agora
                    self.frame_atual = (self.frame_atual + 1) % len(self.frame_andar_l) # BOOOOM
                    self.image = self.frame_andar_l[self.frame_atual]
        elif not self.andando:  # parado
            if agora - self.ultima_mudanca > 300:
                if self.direita:
                    self.ultima_mudanca = agora
                    self.frame_atual = (self.frame_atual + 1) % len(self.frame_parado_r) # BOOOOM
                    self.image = self.frame_parado_r[self.frame_atual]
                else:
                    self.ultima_mudanca = agora
                    self.frame_atual = (self.frame_atual + 1) % len(self.frame_parado_l) # BOOOOM
                    self.image = self.frame_parado_l[self.frame_atual]
        self.mask = pg.mask.from_surface(self.image)
