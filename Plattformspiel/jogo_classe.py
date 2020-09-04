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
        self.BG_COR = [0, 155, 155]

        self.carregar_dados()


    def novo(self):
        # começa um novo jogo
        self.sprites_geral = pg.sprite.Group()
        self.plataformas = pg.sprite.Group()
        self.plataformas_movendo_direita = pg.sprite.Group()
        self.plataformas_movendo_esquerda = pg.sprite.Group()
        self.pontos = 0
        self.fase = 1

        self.jogador = Jogador(self)
        self.sprites_geral.add(self.jogador)

        for pltfrms in PLATAFORMAS_LISTA:
            p = Plataforma(self, *pltfrms, self.pontos)
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

        hits = pg.sprite.spritecollide(self.jogador, self.plataformas, False)
        for hit in hits:
            if self.jogador.vel.y > -0.1:
                if self.jogador.pos.x < hit.rect.right + 15 and \
                self.jogador.rect.x > hit.rect.left - 35:  # cai quando as duas perninhas dele sai da plataforma
                    if self.jogador.pos.y - 5 <= hit.rect.bottom - 2:  # corrigindo bug de transportar para o topo sem alcançar
                        self.jogador.pos.y = hit.rect.top + 1
                        self.jogador.vel.y = 0
                        self.jogador.pulando = False
                # se move junto com a plataforma
                if hit in self.plataformas_movendo_direita:
                    self.jogador.pos.x += 2
                elif hit in self.plataformas_movendo_esquerda:
                    self.jogador.pos.x -= 2

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
                        if self.BG_COR[1] > 6:
                            self.BG_COR[1] -= 1
                            self.BG_COR[2] -= 1

            # PLATAFORMAS SE MOVENDO
            for plat in self.plataformas_movendo_direita:
                plat.rect.right += 2
                if plat.rect.left > WIDTH:
                    plat.rect.right = 0
                    if plat.rect.colliderect(self.jogador.rect):  # por que nunca entra?
                        print('hm')
                        self.jogador.pos.x = plat.rect.left + posicao_jogador_plataforma
                else:
                    posicao_jogador_plataforma = plat.rect.left - self.jogador.pos.x

            for plat in self.plataformas_movendo_esquerda:
                plat.rect.left -= 2
                if plat.rect.left < plat.rect.size[0] * -1:
                    plat.rect.right = WIDTH + plat.rect.size[0]


            if not self.pontos % 100:
                self.definir_fase_e_distancia_plataforma()

            while len(self.plataformas) < 5:
                p = Plataforma(self, random.randrange(0, WIDTH - 50),
                            random.randrange(self.mais_alto, self.mais_baixo), self.fase)
                if self.fase >= 3:
                    r = random.random()
                    if r < 0.3:
                        self.plataformas_movendo_direita.add(p)
                    elif r < 0.6:
                        self.plataformas_movendo_esquerda.add(p)
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
                    if self.jogador.pulando:
                        self.audio_pulo.play()
            elif event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.jogador.interromper_pulo()


    def draw(self):

        self.tela.fill(self.BG_COR)
        self.sprites_geral.draw(self.tela)
        self.tela.blit(self.jogador.image, self.jogador.rect)  # colocando jogador na frente
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

        self.soundtrack.play(-1)
        self.tela.fill(self.BG_COR)
        self.draw_texto(recorde_texto, 20, WHITE, CENTRO_WIDTH, 10)
        self.draw_texto(TITLE, 40, YELLOW, CENTRO_WIDTH, HEIGHT/4)
        self.draw_texto('Ajude o jovem Pipipopo a alcançar', 20, BLACK, CENTRO_WIDTH, HEIGHT/2)
        self.draw_texto('seu objetivo no topo da montanha.', 20, BLACK, CENTRO_WIDTH, HEIGHT/2 + 20)
        self.draw_texto('Pressione qualquer tecla para começar.', 15, YELLOW,
                        CENTRO_WIDTH, HEIGHT - HEIGHT/4)
        pg.display.flip()

        self.esperando_comando()


    def tela_saida(self):

        self.soundtrack.fadeout(1000)
        self.audio_gameover.play(-1)
        self.BG_COR = [0, 155, 155]
        self.tela.fill(self.BG_COR)

        if self.recorde < self.pontos:
            self.recorde = self.pontos
            texto_recorde = "Novo recorde: " + str(self.recorde) + "!"
            self.draw_texto(texto_recorde, 40, WHITE, CENTRO_WIDTH, HEIGHT/4+20)
            with open(path.join(self.dir, RECORDE_FILE), 'w') as f:
                f.write(str(self.pontos))
        else:
            texto_pontucao = 'Pontuação: ' + str(self.pontos)
            texto_recorde = "Recorde: " + str(self.recorde)
            self.draw_texto(texto_pontucao, 30, WHITE, CENTRO_WIDTH, HEIGHT/4)
            self.draw_texto(texto_recorde, 20, WHITE, CENTRO_WIDTH, HEIGHT/4 + 45)

        self.draw_texto('Não foi dessa vez! :(', 20, BLACK, CENTRO_WIDTH, HEIGHT/2 - 20)
        self.draw_texto('Mas não se procupe, não será uma', 18, BLACK, CENTRO_WIDTH, HEIGHT/2 + 20)
        self.draw_texto('"quedinha" que desmotivará Pipipopo.', 18, BLACK, CENTRO_WIDTH, HEIGHT/2 + 40)
        self.draw_texto('Ele passa bem e está pronto para', 18, BLACK, CENTRO_WIDTH, HEIGHT/2 + 60)
        self.draw_texto('tentar outra vez!', 18, BLACK, CENTRO_WIDTH, HEIGHT/2 + 80)
        pg.display.flip()

        self.esperando_comando()

        self.audio_gameover.fadeout(500)
        self.soundtrack.play(-1)


    def esperando_comando(self):
        esperar = True
        while esperar:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.jogando = False
                    esperar = False
                elif event.type == pg.KEYDOWN:
                    esperar = False


    def definir_fase_e_distancia_plataforma(self):

        # gerar novas plataformas
        mais_alto = HEIGHT
        for pltfrms in self.plataformas:
            if mais_alto > pltfrms.rect.top:
                mais_alto = pltfrms.rect.top

        # pegar fase e distância
        if self.pontos == 800:
            self.fase = 3
            self.mais_alto = mais_alto - HEIGHT//2.8
            self.mais_baixo = mais_alto - HEIGHT//2.81 #3.2
        if self.pontos == 500:
            self.fase = 3
            self.mais_alto = mais_alto - HEIGHT//3.2
            self.mais_baixo = mais_alto - HEIGHT//3.7
        elif self.pontos == 200:
            self.fase = 2
            self.mais_alto = mais_alto - HEIGHT//4
            self.mais_baixo = mais_alto - HEIGHT//4.5
        elif self.pontos == 0:
            self.mais_alto = mais_alto - HEIGHT//5
            self.mais_baixo = mais_alto - HEIGHT//5.5


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

        # música
        self.sound_dir = path.join(self.dir, 'audio')
        self.soundtrack = pg.mixer.Sound(path.join(self.sound_dir, main_track))
        self.soundtrack.set_volume(0.15) #0.15
        self.audio_pulo = pg.mixer.Sound(path.join(self.sound_dir, jump_sound_dir))
        self.audio_pulo.set_volume(0.04) #0.04
        self.audio_gameover = pg.mixer.Sound(path.join(self.sound_dir, game_over_audio))
        self.audio_gameover.set_volume(0.1) #0.1
