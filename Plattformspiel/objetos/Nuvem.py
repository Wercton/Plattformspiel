import pygame as pg
import random
from configuracoes import LAYER_NUVENS, LAYER_NUVENS_FRENTE, WIDTH, HEIGHT, BLACK


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


    '''class Fundo(pg.sprite.Sprite):

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
            self.rect.x = 200'''

