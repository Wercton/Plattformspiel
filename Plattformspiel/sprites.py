import pygame as pg
import random
from configuracoes import *


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
            Poder(self.game, self)


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


class Mob(pg.sprite.Sprite):

    def __init__(self, game):

        self._layer = LAYER_MOB
        self.grupos = game.sprites_geral, game.mobs
        pg.sprite.Sprite.__init__(self, self.grupos)
        self.game = game

        self.image = pg.image.load(NYAH1)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice([-100, WIDTH + 100])
        self.imagem_esquerda = [pg.image.load(NYAH1), pg.image.load(NYAH2)]
        self.imagem_direita = [pg.transform.flip(self.imagem_esquerda[0], True, False), pg.transform.flip(self.imagem_esquerda[1], True, False)]
        self.imagens = self.imagem_direita
        self.ultima_mudanca = 0
        self.frame_atual = 0

        self.velx = random.randrange(1, 4)
        self.vely = 0
        if self.rect.centerx > WIDTH:
            self.imagens = self.imagem_esquerda
            self.velx *= -1
        self.rect.y = random.randrange(HEIGHT / -3, HEIGHT / 3)
        self.accy = 0.8  # aceleração para o y

    def update(self):
        self.rect.x += self.velx
        self.vely += self.accy
        if self.vely > 5 or self.vely < -5:
            self.accy *= -1

        centro = self.rect.center
        agora = pg.time.get_ticks()
        if agora - self.ultima_mudanca > 100:
            self.ultima_mudanca = agora
            self.frame_atual = (self.frame_atual + 1) % len(self.imagens)
            self.image = self.imagens[self.frame_atual]

        self.rect = self.image.get_rect()
        self.rect.center = centro

        self.rect.y += self.vely
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()


class Botao(pg.sprite.Sprite):

    def __init__(self, game, y, texto, selecionado=False):

        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.texto, self.texto_primeiro = texto, texto
        self.selecionado = selecionado

        if self.selecionado:
            self.image = pg.image.load(BOTAO_SELECIONADO)
        else:
            self.image = pg.image.load(BOTAO)
        self.rect = self.image.get_rect()
        self.rect.centerx = CENTRO_WIDTH
        self.rect.y = y

        self.game.tela.blit(self.image, self.rect)
        self.game.draw_texto(self.texto, 30, BLACK, self.rect.centerx, self.rect.centery - 15)


    def update(self):

        self.game.tela.blit(self.image, self.rect)
        self.game.draw_texto(self.texto, 30, BLACK, self.rect.centerx, self.rect.centery - 15)

    def selecionar(self):

        self.game.canal_efeito.play(self.game.audio_click)
        self.selecionado = True
        centro = self.rect.centerx
        y = self.rect.y

        self.image = pg.image.load(BOTAO_SELECIONADO)
        self.rect = self.image.get_rect()
        self.rect.centerx = centro
        self.rect.y = y

    def deselecionar(self):

        self.selecionado = False
        centro = self.rect.centerx
        y = self.rect.y

        self.image = pg.image.load(BOTAO)
        self.rect = self.image.get_rect()
        self.rect.centerx = centro
        self.rect.y = y

    def mudar_texto(self, novo_texto):

        self.texto = novo_texto
