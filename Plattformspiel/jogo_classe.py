import pygame as pg
import random
from configuracoes import *
from personagem import *
from sprites import *
from os import path

class Game:

    def __init__(self):
        # inicializa o jogo
        pg.init()
        pg.mixer.init()
        self.canal_musica = pg.mixer.Channel(0)
        self.canal_efeito = pg.mixer.Channel(1)
        self.audio = 1
        self.sorte = 0
        self.freq_poder = FREQUENCIA_PODER
        self.audio_efeitos = 1

        self.tela = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.jogando = True
        self.fonte_texto = pg.font.match_font(FONTE_TEXTO)
        self.BG_COR = [0, 155, 155]

        self.menu = True
        self.game_over = False

        self.carregar_dados()


    def novo(self):
        # começa um novo jogo
        self.canal_musica.play(self.soundtrack, loops = -1)

        self.game_over = False
        self.sprites_geral = pg.sprite.LayeredUpdates()
        self.plataformas = pg.sprite.Group()
        self.plataformas_movendo_direita = pg.sprite.Group()
        self.plataformas_movendo_esquerda = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.poderes = pg.sprite.Group()
        self.pontos = 0
        self.fase = 1
        self.velocidade_plat = 0
        self.prob_plat_movimento = 0
        self.tempo_mob = 0

        self.jogador = Jogador(self)

        p = Plataforma(self, -20, HEIGHT - 15, -1)

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
        self.verificar_colisoes()

        if not self.verificar_game_over():

            self.subir_tela()  # muda as cores também
            self.movimentar_plataformas()  # aumentar precisão

            if not self.pontos % 100:
                self.configurar_fases()

            self.spawnar()


    def eventos(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.partida = False
                self.jogando = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.jogador.pular()
                elif event.key == pg.K_ESCAPE:
                    self.partida = False
            elif event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.jogador.interromper_pulo()


    def draw(self):

        self.tela.fill(self.BG_COR)
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

        pg.mixer.fadeout(1000)

        self.decidindo = True
        self.botao_selecionado = 0
        self.botao_jogar = Botao(self, 125, "JOGAR", True)
        self.botao_opcoes = Botao(self, 200, "OPÇÕES")
        self.botao_sair = Botao(self, 275, "SAIR")
        self.botoes = [self.botao_jogar, self.botao_opcoes, self.botao_sair]
        self.opcoes = False

        while self.decidindo:

            self.tela.fill(self.BG_COR)
            self.draw_texto(TITLE, 30, BLACK, 185, 20)

            for botao in self.botoes:
                botao.update()

            self.tela_inicial_eventos()

            if self.opcoes:
                self.tela_opcoes()

            pg.display.flip()


    def tela_inicial_eventos(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.decidindo = False
                self.jogando = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    self.botoes[self.botao_selecionado].deselecionar()
                    if self.botao_selecionado < 2:
                        self.botao_selecionado += 1
                        self.botoes[self.botao_selecionado].selecionar()
                    else:
                        self.botao_selecionado = 0
                        self.botoes[self.botao_selecionado].selecionar()
                elif event.key == pg.K_UP:
                    self.botoes[self.botao_selecionado].deselecionar()
                    if self.botao_selecionado > 0:
                        self.botao_selecionado -= 1
                        self.botoes[self.botao_selecionado].selecionar()
                    else:
                        self.botao_selecionado = 2
                        self.botoes[self.botao_selecionado].selecionar()
                elif event.key == pg.K_RETURN:
                    if not self.botao_selecionado:
                        self.decidindo = False
                    elif self.botao_selecionado == 1:
                        self.opcoes = True
                    elif self.botao_selecionado == 2:
                        self.decidindo = False
                        self.jogando = False


    def tela_opcoes(self):

        self.botao_selecionado = 0

        if self.audio:
            self.botao_audio = Botao(self, 125, "AUDIO ON", True)
        else:
            self.botao_audio = Botao(self, 125, "AUDIO OFF", True)

        if self.audio_efeitos:
            self.botao_efeitos = Botao(self, 200, "EFEITOS ON", False)
        else:
            self.botao_efeitos = Botao(self, 200, "EFEITOS OFF", False)

        if self.sorte:
            self.botao_sorte = Botao(self, 275, "SORTE ON", False)
        else:
            self.botao_sorte = Botao(self, 275, "SORTE OFF", False)

        self.botao_retornar = Botao(self, 350, "RETORNAR", False)

        self.botoes_opcoes = [self.botao_audio, self.botao_efeitos, \
                            self.botao_sorte, self.botao_retornar]

        while self.opcoes:

            self.tela.fill(self.BG_COR)
            self.draw_texto("OPÇÕES", 30, BLACK, 185, 20)

            for botao in self.botoes_opcoes:
                botao.update()

            self.tela_opcoes_eventos()

            pg.display.flip()


    def tela_opcoes_eventos(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.decidindo = False
                self.jogando = False
                self.opcoes = False
            elif event.type == pg.KEYDOWN:


                if event.key == pg.K_DOWN:
                    self.botoes_opcoes[self.botao_selecionado].deselecionar()
                    if self.botao_selecionado < 3:
                        self.botao_selecionado += 1
                        self.botoes_opcoes[self.botao_selecionado].selecionar()
                    else:
                        self.botao_selecionado = 0
                        self.botoes_opcoes[self.botao_selecionado].selecionar()
                elif event.key == pg.K_UP:
                    self.botoes_opcoes[self.botao_selecionado].deselecionar()
                    if self.botao_selecionado > 0:
                        self.botao_selecionado -= 1
                        self.botoes_opcoes[self.botao_selecionado].selecionar()
                    else:
                        self.botao_selecionado = 3
                        self.botoes_opcoes[self.botao_selecionado].selecionar()

                elif event.key == pg.K_RETURN:
                    # RETORNAR
                    if self.botao_selecionado == 3:
                        self.opcoes = False
                        self.botao_selecionado = 1
                    # EFEITOS
                    elif self.botao_selecionado == 1:
                        if self.audio_efeitos:
                            self.botoes_opcoes[1].mudar_texto("EFEITOS OFF")
                            self.canal_efeito.set_volume(0)
                        else:
                            self.botoes_opcoes[1].mudar_texto("EFEITOS ON")
                            self.canal_efeito.set_volume(1)
                        self.audio_efeitos = 0 if self.audio_efeitos else 1
                    # AUDIO
                    elif not self.botao_selecionado:
                        if self.audio:
                            self.botoes_opcoes[0].mudar_texto("AUDIO OFF")
                            self.canal_musica.set_volume(0)
                        else:
                            self.botoes_opcoes[0].mudar_texto("AUDIO ON")
                            self.canal_musica.set_volume(1)
                        self.audio = 0 if self.audio else 1
                    # SORTE
                    elif self.botao_selecionado == 2:
                        if self.sorte:
                            self.botoes_opcoes[2].mudar_texto("SORTE OFF")
                            self.freq_poder = FREQUENCIA_PODER
                        else:
                            self.botoes_opcoes[2].mudar_texto("SORTE ON")
                            self.freq_poder = 100
                        self.sorte = 0 if self.sorte else 1

                elif event.key == pg.K_ESCAPE:
                    self.opcoes = False
                    self.botao_selecionado = 1  # but why?


    def tela_saida(self):

        pg.mixer.fadeout(1000)
        self.canal_musica.play(self.audio_gameover, loops = -1)
        self.decidindo = True
        self.botao_selecionado = 0
        self.botao_tentar_novamente = Botao(self, 350, "NOVAMENTE", True)
        self.botao_menu = Botao(self, 415, "MENU", False)
        self.botoes = [self.botao_tentar_novamente, self.botao_menu]

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

        while self.decidindo:

            self.BG_COR = [0, 155, 155]
            self.tela.fill(self.BG_COR)

            for botao in self.botoes:
                botao.update()

            if self.recorde < self.pontos:
                self.recorde = self.pontos
                texto_recorde = "Novo recorde: " + str(self.recorde) + "!"
                self.draw_texto(texto_recorde, 40, WHITE, CENTRO_WIDTH, HEIGHT/4+20)
                with open(path.join(self.dir, RECORDE_FILE), 'w') as f:
                    f.write(str(self.pontos))
            else:
                texto_pontucao = 'Pontuação: ' + str(self.pontos)
                texto_recorde = "Recorde: " + str(self.recorde)
                self.draw_texto(texto_pontucao, 30, WHITE, CENTRO_WIDTH, HEIGHT/4 - 20)
                self.draw_texto(texto_recorde, 20, WHITE, CENTRO_WIDTH, HEIGHT/4 + 25)

            self.draw_texto('Não foi dessa vez! :(', 20, BLACK, CENTRO_WIDTH, HEIGHT/2 - 40)
            self.draw_texto('Mas não se procupe, não será uma', 18, BLACK, CENTRO_WIDTH, HEIGHT/2 + 0)
            self.draw_texto('"quedinha" que desmotivará Pipipopo.', 18, BLACK, CENTRO_WIDTH, HEIGHT/2 + 20)
            self.draw_texto('Ele passa bem e está pronto para', 18, BLACK, CENTRO_WIDTH, HEIGHT/2 + 40)
            self.draw_texto('tentar outra vez!', 18, BLACK, CENTRO_WIDTH, HEIGHT/2 + 60)

            self.tela_saida_eventos()

            pg.display.flip()

        self.audio_gameover.fadeout(1000)


    def tela_saida_eventos(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.decidindo = False
                self.jogando = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN or event.key == pg.K_UP:
                    self.botoes[self.botao_selecionado].deselecionar()
                    self.botao_selecionado = 0 if self.botao_selecionado else 1
                    self.botoes[self.botao_selecionado].selecionar()
                elif event.key == pg.K_RETURN:
                    self.decidindo = False
                    if self.botao_selecionado:
                        self.menu = True
                    else:
                        self.menu = False


    def esperando_comando(self):
        esperar = True
        while esperar:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.jogando = False
                    esperar = False
                elif event.type == pg.KEYDOWN:
                    esperar = False


    def verificar_colisoes(self):
        # plataforma
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
                    self.jogador.pos.x += self.velocidade_plat
                elif hit in self.plataformas_movendo_esquerda:
                    self.jogador.pos.x -= self.velocidade_plat
        # poderes
        hits = pg.sprite.spritecollide(self.jogador, self.poderes, True)
        for hit in hits:
            if hit.tipo == 'impulso':
                self.canal_efeito.play(self.audio_moeda)
                self.jogador.vel.y = -IMPULSO_POTENCIA
                self.jogador.pulando = False
        # mobs - GAME OVER
        hits = pg.sprite.spritecollide(self.jogador, self.mobs, False)
        if hits:
            self.game_over = True
            self.partida = False


    def verificar_game_over(self):

        if self.jogador.rect.top > HEIGHT:
            for sprite in self.sprites_geral:
                sprite.rect.y -= self.jogador.vel.y # limitar velocidade com max (..., 10)?
                if sprite.rect.bottom < 0:
                    sprite.kill()
            if not len(self.plataformas): # só quando some todas plataformas, novo jogo se inicia
                self.partida = False
                self.game_over = True
                return True
        else:
            return False


    def subir_tela(self):

        if self.jogador.rect.top <= HEIGHT / 4:
            self.jogador.pos.y += abs(self.jogador.vel.y)
            for mob in self.mobs:  # mover mob junto com a tela
                mob.rect.y += abs(self.jogador.vel.y)
            for pltfrms in self.plataformas:  # mover plataformas junto com a tela
                pltfrms.rect.y += abs(self.jogador.vel.y) # usar -= no lugar de abs?
                if pltfrms.rect.top >= HEIGHT:
                    pltfrms.kill()
                    self.pontos += 10
                    if self.BG_COR[1] > 3:
                        self.BG_COR[1] -= 1.5
                        self.BG_COR[2] -= 1.5


    def movimentar_plataformas(self):
        # direita
        for plat in self.plataformas_movendo_direita:
            plat.rect.right += self.velocidade_plat
            if plat.rect.left > WIDTH:
                plat.rect.right = 0
                if plat.rect.colliderect(self.jogador.rect):  # por que nunca entra?
                    print('hm')
                    self.jogador.pos.x = plat.rect.left + posicao_jogador_plataforma #ENTROOOOOU MAS DEU ERRO, ESTAVA CAINDO
            else:
                posicao_jogador_plataforma = plat.rect.left - self.jogador.pos.x
        # esquerda
        for plat in self.plataformas_movendo_esquerda:
            plat.rect.left -= self.velocidade_plat
            if plat.rect.left < plat.rect.size[0] * -1:
                plat.rect.right = WIDTH + plat.rect.size[0]


    def configurar_fases(self):
        if self.pontos == 800:
            self.fase = 4
            self.velocidade_plat = 3
            self.soundtrack.fadeout(3000)
            self.canal_musica.play(self.soundtrack_final, loops = -1)
            self.jogador.gravidade = 0.6
            self.prob_plat_movimento = 0.5
        elif self.pontos == 500:
            self.fase = 3
            self.velocidade_plat = 2
            self.prob_plat_movimento = 0.3
        elif self.pontos == 200:
            self.fase = 2
            self.velocidade_plat = 0


    def spawnar(self):
        # spawnando mobs
        agora = pg.time.get_ticks()
        if agora - self.tempo_mob > FREQUENCIA_MOB:
            self.tempo_mob = agora
            if random.random() < PROBABILICADE_MOB:
                Mob(self)

        # spawnando plataformas
        while len(self.plataformas) < 5:

            mais_alto = HEIGHT
            for pltfrms in self.plataformas:
                if mais_alto > pltfrms.rect.top:
                    mais_alto = pltfrms.rect.top

            if self.fase == 1:
                self.mais_alto = mais_alto - HEIGHT//4.1
                self.mais_baixo = mais_alto - HEIGHT//4.5
            elif self.fase == 2:
                self.mais_alto = mais_alto - HEIGHT//3.2
                self.mais_baixo = mais_alto - HEIGHT//3.9
            elif self.fase == 3:
                self.mais_alto = mais_alto - HEIGHT//2.8
                self.mais_baixo = mais_alto - HEIGHT//3.1
            elif self.fase == 4:
                self.mais_alto = mais_alto - HEIGHT//2.2
                self.mais_baixo = mais_alto - HEIGHT//2.6

            p = Plataforma(self, random.randrange(0, WIDTH - 50),
                        random.randrange(self.mais_alto, self.mais_baixo), self.fase)
            if self.fase >= 3:
                r = random.random()
                if r < self.prob_plat_movimento:
                    self.plataformas_movendo_direita.add(p)
                elif r < self.prob_plat_movimento * 2:
                    self.plataformas_movendo_esquerda.add(p)


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
        self.soundtrack = pg.mixer.Sound(path.join(self.sound_dir, MAIN_TRACK))
        self.soundtrack.set_volume(0.15) #0.15

        self.soundtrack_final = pg.mixer.Sound(path.join(self.sound_dir, MAIN_TRACK_FINAL))
        self.soundtrack_final.set_volume(0.05) #0.05

        self.audio_pulo = pg.mixer.Sound(path.join(self.sound_dir, PULO_AUDIO))
        self.audio_pulo.set_volume(0.04) #0.04

        self.audio_gameover = pg.mixer.Sound(path.join(self.sound_dir, GAME_OVER_AUDIO))
        self.audio_gameover.set_volume(0.1) #0.1

        self.audio_moeda = pg.mixer.Sound(path.join(self.sound_dir, COIN_AUDIO))
        self.audio_moeda.set_volume(0.2) #0.2

        self.audio_click = pg.mixer.Sound(path.join(self.sound_dir, CLICK))
        self.audio_click.set_volume(1)
