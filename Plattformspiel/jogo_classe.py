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
        self.jogador = Jogador()
        self.sprites_geral.add(self.jogador)
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

    def eventos(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.jogando = False

    def draw(self):

        self.tela.fill(BLACK)
        self.sprites_geral.draw(self.tela)
        # depois de desenhar tudo, flip o display ???
        pg.display.flip()


    def tela_inicial(self):
        pass

    def tela_saida(self):
        pass
