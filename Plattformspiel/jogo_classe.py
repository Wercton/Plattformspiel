import pygame as pg
import random
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
        self.fonte_texto = pg.font.match_font(FONTE_TEXTO)


    def novo(self):
        # começa um novo jogo
        self.sprites_geral = pg.sprite.Group()
        self.plataformas = pg.sprite.Group()
        self.pontos = 0

        self.jogador = Jogador()
        self.sprites_geral.add(self.jogador)

        for pltfrms in PLATAFORMAS_LISTA:
            p = Plataforma(*pltfrms)
            self.plataformas.add(p)
            self.sprites_geral.add(p)

        self.run()


    def run(self):
        # loop do jogo
        self.partida = True
        while self.partida:
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
        # game over?
        if self.jogador.rect.top > HEIGHT:
            for sprite in self.sprites_geral:
                sprite.rect.y -= self.jogador.vel.y # limitar velocidade com max (..., 10)?
                if sprite.rect.bottom < 0:
                    sprite.kill()
            if not len(self.plataformas): # só quando some todas plataformas, novo jogo se inicia
                self.partida = False
                print("GAME OVER")
        else:
            # subindo a tela
            if self.jogador.rect.top <= HEIGHT / 4:
                self.jogador.pos.y += abs(self.jogador.vel.y)
                for pltfrms in self.plataformas:
                    pltfrms.rect.y += abs(self.jogador.vel.y) # usar -= no lugar de abs?
                    if pltfrms.rect.top >= HEIGHT:
                        pltfrms.kill()
                        self.pontos += 10
            # gerar novas plataformas
            while len(self.plataformas) < 5:
                width = random.randrange(40, 85)
                p = Plataforma(random.randrange(0, WIDTH - width),
                            random.randrange(-80, -40), width, WIDTH_PLAT)
                self.sprites_geral.add(p)
                self.plataformas.add(p)


    def eventos(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.partida = False
                self.jogando = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.jogador.pular()


    def draw(self):

        self.tela.fill(BLACK)
        self.sprites_geral.draw(self.tela)
        self.draw_texto(str(self.pontos), 20, YELLOW, WIDTH/2, 10)

        pg.display.flip()


    def draw_texto(self, texto, tamanho, cor, x, y):

        fonte = pg.font.Font(self.fonte_texto, tamanho)
        texto_surface = fonte.render(texto, True, cor) # True para anti-alising
        texto_rect = texto_surface.get_rect()
        texto_rect.midtop = (x, y)
        self.tela.blit(texto_surface, texto_rect)


    def tela_inicial(self):
        pass

    def tela_saida(self):
        pass
