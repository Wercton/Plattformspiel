import pygame as pg
from src.configuracoes import (
    CENTRO_WIDTH,
    BLACK,
    WHITE,
    BOTAO_COR,
    BOTAO_COR_SELECIONADO,
    BOTAO_SOMBRA,
)


class Botao(pg.sprite.Sprite):
    def __init__(self, game, y, texto, selecionado=False):
        self.__layer = 10
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.texto, self.texto_primeiro = texto, texto
        self.selecionado = selecionado
        self.rect = pg.Rect(0, 0, 220, 50)
        self.rect.centerx = CENTRO_WIDTH
        self.rect.y = y

    def update(self):
        # Sombra
        sombra_rect = self.rect.copy()
        sombra_rect.y += 6
        pg.draw.rect(self.game.tela, BOTAO_SOMBRA, sombra_rect, border_radius=16)

        # Botão principal
        cor = BOTAO_COR_SELECIONADO if self.selecionado else BOTAO_COR
        pg.draw.rect(self.game.tela, cor, self.rect, border_radius=16)

        # Borda
        pg.draw.rect(self.game.tela, WHITE, self.rect, width=2, border_radius=16)

        # Texto centralizado
        fonte = pg.font.Font(self.game.fonte_texto, 30)
        texto_surface = fonte.render(
            self.texto, True, WHITE if self.selecionado else BLACK
        )
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        self.game.tela.blit(texto_surface, texto_rect)

    def selecionar(self):
        self.game.canal_efeito.play(self.game.audio_click)
        self.selecionado = True

    def deselecionar(self):
        self.selecionado = False

    def mudar_texto(self, novo_texto):
        self.texto = novo_texto
