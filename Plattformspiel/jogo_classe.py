import pygame as pg
import sys
from configuracoes import *
from sprites import *

class Game:

    def __init__(self):
        # inicializa o jogo
        pg.init()
        pg.mixer.init()
        self.tela = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.jogando = True

    def novo(self):
        # começa um novo jogo
        self.sprites_geral = pg.sprite.Group()
        self.plataformas = pg.sprite.Group()

        self.jogador = Jogador()
        self.sprites_geral.add(self.jogador)

        for pltfrms in PLATAFORMAS_LISTA:
            p = Plataforma(*pltfrms)
            self.plataformas.add(p)
            self.sprites_geral.add(p)

        self.run()

    def run(self):
        # loop do jogo
        self.jogando = True
        while self.jogando:
            self.clock.tick(FPS)
            self.eventos()
            self.update()
            self.draw()

    def update(self):
        self.sprites_geral.update()
        if self.jogador.vel.y > -0.1: # colisão somente ao cair
            hits = pg.sprite.spritecollide(self.jogador, self.plataformas, False)
            if hits:
                self.jogador.pos.y = hits[0].rect.top + 1
                self.jogador.vel.y = 0


    def eventos(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.jogando = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.jogador.pular()


    def draw(self):

        self.tela.fill(BLACK)
        self.sprites_geral.draw(self.tela)
        pg.display.flip()


    def tela_inicial(self):
        pass

    def tela_saida(self):
        pass
