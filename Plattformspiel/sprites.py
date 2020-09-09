import pygame as pg
import random
from configuracoes import *


class Spritesheet:

    def __init__(self, filename):

        self.spritesheet = pg.image.load(filename).convert()

    def selecionar_imagem(self, x, y, width, height):

        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image


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
        self.rect.y = random.randrange(HEIGHT / -3, HEIGHT / 3)
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


class Botao(pg.sprite.Sprite):

    def __init__(self, game, y, texto, selecionado=False):

        self.__layer = LAYER_SISTEMA
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


class Nuvem(pg.sprite.Sprite):

    def __init__(self, game, fase):

        if random.random() > 0.5 and fase > 1:
            self._layer = LAYER_NUVENS_FRENTE
            self.frente = True
        else:
            self._layer = LAYER_NUVENS
            self.frente = False
        self.grupos = game.sprites_geral, game.nuvens
        pg.sprite.Sprite.__init__(self, self.grupos)
        self.game = game

        self.nuvens_imagem = []
        width, height = 56, 23
        for i in range(4):
            self.nuvens_imagem.append(self.game.spritesheet.selecionar_imagem(0, height*i, width, height))
            self.nuvens_imagem.append(pg.transform.flip(self.nuvens_imagem[-1], True, False))
        self.image = random.choice(self.nuvens_imagem)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        if not self.frente:
            scale = random.randrange(150, 250) / 100
        else:
            scale = 3
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale), int(self.rect.height * scale)))
        if self.frente:
            self.rect.x = -self.rect.width
        else:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-500, -50)

    def update(self):
        if self.rect.top > HEIGHT:
            self.kill()
        if self.frente:
            self.rect.x += 1
            if self.rect.left > WIDTH + 50:
                self.rect.right = -self.rect.width


    class Fundo(pg.sprite.Sprite):

        def __init__(self):

            self.__layer = 0
            self.grupos = game.sprites_geral
            pg.sprite.Sprite.__init__(self, self.grupos)

            self.image = pg.image.load(montanhas)
            self.rect = self.image.get_rect()
            self.rect.y = 200
            self.rect.x = 200

        def update(self):
            self.rect.y = 200
            self.rect.x = 200
