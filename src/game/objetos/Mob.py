import pygame as pg
import random
from src.configuracoes import LAYER_MOB, NYAH1, NYAH2, WIDTH, HEIGHT, ATENCAO1, ATENCAO2


class Mob(pg.sprite.Sprite):

    def __init__(self, game):

        self._layer = LAYER_MOB
        self.grupos = game.sprites_geral, game.mobs
        pg.sprite.Sprite.__init__(self, self.grupos)
        self.game = game

        self.image = pg.image.load(NYAH1)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice([-85, WIDTH + 85])
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
        self.rect.y = random.randrange(int(HEIGHT / -3), int(HEIGHT / 3))
        self.accy = 0.8  # aceleração para o y

        Atencao(self.game, self)

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
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = centro

        self.rect.y += self.vely
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()


class Atencao(pg.sprite.Sprite):

    def __init__(self, game, mob):

        self._layer = LAYER_MOB
        self.grupos = game.sprites_geral
        pg.sprite.Sprite.__init__(self, self.grupos)
        self.mob = mob

        self.imagens = [pg.image.load(ATENCAO1), pg.image.load(ATENCAO2)]
        self.image = self.imagens[0]
        self.ultima_mudanca = 0
        self.frame_atual = 0

        self.rect = self.image.get_rect()
        self.rect.centerx = self.mob.rect.centerx
        self.rect.y = self.mob.rect.y

    def update(self):

        if self.mob.rect.centerx < - self.mob.rect.width // 2:
            self.rect.x = 10
        elif self.mob.rect.centerx > WIDTH + self.mob.rect.width // 2:
            self.rect.x = WIDTH - 10
        else:
            self.kill()

        centro = self.rect.center
        agora = pg.time.get_ticks()
        if agora - self.ultima_mudanca > 100:
            self.ultima_mudanca = agora
            self.frame_atual = (self.frame_atual + 1) % len(self.imagens)
            self.image = self.imagens[self.frame_atual]

        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = centro

        self.rect.y = self.mob.rect.y
