import pygame as pg
import random
from configuracoes import *

vec = pg.math.Vector2

class Jogador(pg.sprite.Sprite):

    def __init__(self, game):
        self.grupos = game.sprites_geral
        pg.sprite.Sprite.__init__(self, self.grupos)
        self.image = pg.transform.scale(pg.image.load(JOGADOR_SPRITE), TAMANHO_JOGADOR)
        self.rect = self.image.get_rect()
        self.rect.center = (POSICAO_INICIAL)
        self.pos = vec(POSICAO_INICIAL)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.gravidade = GRAVIDADE_JOGADOR
        self.pulando = False
        self.game = game

        self.andando = False
        self.frame_atual = 0
        self.ultima_mudanca = 0
        self.direita = True
        self.carregar_imagens()

    def update(self):

        self.animar()
        self.acc = vec(0, self.gravidade)
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.acc.x = -ACC_JOGADOR
            self.direita = False
        elif keys[pg.K_RIGHT]:
            self.acc.x = ACC_JOGADOR
            self.direita = True

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
            self.game.audio_pulo.play()
            self.pulando = True
            self.vel.y = -PULO_JOGADOR

    def interromper_pulo(self):

        if self.pulando:
            if self.vel.y < -3:
                self.vel.y = -3

    def carregar_imagens(self):

        self.frame_pular_l = pg.transform.scale(pg.image.load(PULO_SPRITE), TAMANHO_JOGADOR)
        self.frame_pular_r = pg.transform.flip(self.frame_pular_l, True, False)

        self.frame_parado_l = [pg.transform.scale(pg.image.load(JOGADOR_SPRITE), TAMANHO_JOGADOR),
                            pg.transform.scale(pg.image.load(JOGADOR_SPRITE2), TAMANHO_JOGADOR)]
        self.frame_parado_r = []
        for frame in self.frame_parado_l:
            self.frame_parado_r.append(pg.transform.flip(frame, True, False))

        self.frame_andar_l = [pg.transform.scale(pg.image.load(ANDAR1_SPRITE), TAMANHO_JOGADOR),
                            pg.transform.scale(pg.image.load(ANDAR2_SPRITE), TAMANHO_JOGADOR)]
        self.frame_andar_r = []
        for frame in self.frame_andar_l:
            self.frame_andar_r.append(pg.transform.flip(frame, True, False))

        self.frame_cair_l = pg.transform.scale(pg.image.load(CAIR_SPRITE), TAMANHO_JOGADOR)
        self.frame_cair_r = pg.transform.flip(self.frame_cair_l, True, False)

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
        else:  # parado
            if agora - self.ultima_mudanca > 400:
                if self.direita:
                    self.ultima_mudanca = agora
                    self.frame_atual = (self.frame_atual + 1) % len(self.frame_parado_r) # BOOOOM
                    self.image = self.frame_parado_r[self.frame_atual]
                else:
                    self.ultima_mudanca = agora
                    self.frame_atual = (self.frame_atual + 1) % len(self.frame_parado_l) # BOOOOM
                    self.image = self.frame_parado_l[self.frame_atual]


class Plataforma(pg.sprite.Sprite):

    def __init__(self, game, x, y, fase):
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
        else:
            self.image = pg.image.load(random.choice(PLATAFORMA_FASE1))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if self.game.pontos >= 10:
            if random.randrange(100) < FREQUENCIA_PODER:
                Poder(self.game, self)


class Poder(pg.sprite.Sprite):

    def __init__(self, game, plat):
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
