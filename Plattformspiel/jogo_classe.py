import pygame as pg
import random
from configuracoes import *
from sprites import *
from os import path

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

        self.carregar_dados()


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

        self.tela.fill(BG_COR)
        self.sprites_geral.draw(self.tela)
        self.draw_texto(str(self.pontos), 20, YELLOW, CENTRO_WIDTH, 10)

        pg.display.flip()


    def draw_texto(self, texto, tamanho, cor, x, y):

        fonte = pg.font.Font(self.fonte_texto, tamanho)
        texto_surface = fonte.render(texto, True, cor) # True para anti-alising
        texto_rect = texto_surface.get_rect()
        texto_rect.midtop = (x, y)
        self.tela.blit(texto_surface, texto_rect)


    def tela_inicial(self):

        recorde_texto = "Recorde: " + str(self.recorde)

        self.tela.fill(BG_COR)
        self.draw_texto(recorde_texto, 20, WHITE, CENTRO_WIDTH, 10)
        self.draw_texto(TITLE, 40, YELLOW, CENTRO_WIDTH, HEIGHT/4)
        self.draw_texto('Ajude o jovem Pipipopo a alcançar', 20, BLACK, CENTRO_WIDTH, HEIGHT/2)
        self.draw_texto('seu objetivo no topo da montanha.', 20, BLACK, CENTRO_WIDTH, HEIGHT/2 + 20)
        self.draw_texto('Pressione qualquer tecla para começar.', 15, YELLOW,
                        CENTRO_WIDTH, HEIGHT - HEIGHT/4)
        pg.display.flip()

        self.esperando_comando()


    def tela_saida(self):

        self.tela.fill(BG_COR)

        if self.recorde < self.pontos:
            self.recorde = self.pontos
            texto_recorde = "Novo recorde: " + str(self.recorde) + "!"
            self.draw_texto(texto_recorde, 40, WHITE, CENTRO_WIDTH, HEIGHT/4+20)
            with open(path.join(self.dir, RECORDE_FILE), 'w') as f:
                f.write(str(self.pontos))
        else:
            texto_pontucao = 'Pontuação: ' + str(self.pontos)
            texto_recorde = "Recorde: " + str(self.recorde)
            self.draw_texto(texto_pontucao, 40, WHITE, CENTRO_WIDTH, HEIGHT/4)
            self.draw_texto(texto_recorde, 20, WHITE, CENTRO_WIDTH, HEIGHT/4 + 45)

        self.draw_texto('Não foi dessa vez! :(', 20, BLACK, CENTRO_WIDTH, HEIGHT/2 - 20)
        self.draw_texto('Mas não se procupe, não será uma', 18, BLACK, CENTRO_WIDTH, HEIGHT/2 + 20)
        self.draw_texto('"quedinha" que desmotivará Pipipopo.', 18, BLACK, CENTRO_WIDTH, HEIGHT/2 + 40)
        self.draw_texto('Ele passa bem e está pronto para', 18, BLACK, CENTRO_WIDTH, HEIGHT/2 + 60)
        self.draw_texto('tentar outra vez!', 18, BLACK, CENTRO_WIDTH, HEIGHT/2 + 80)
        pg.display.flip()

        self.esperando_comando()


    def esperando_comando(self):
        esperar = True
        while esperar:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.jogando = False
                    esperar = False
                elif event.type == pg.KEYDOWN:
                    esperar = False


    def carregar_dados(self):

        self.dir = path.dirname(__file__)
        try:
            with open(path.join(self.dir, RECORDE_FILE), 'r+') as f:
                try:
                    self.recorde = int(f.read())
                except:
                    self.recorde = 0
        except:
            with open(path.join(self.dir, RECORDE_FILE), 'w') as f:
                self.recorde = 0
