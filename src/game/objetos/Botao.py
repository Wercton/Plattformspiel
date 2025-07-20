import pygame as pg
from src.configuracoes import BOTAO, BOTAO_SELECIONADO, LAYER_SISTEMA, CENTRO_WIDTH, BLACK


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
        