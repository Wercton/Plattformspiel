import pygame as pg
from src.game.jogo_classe import Game
from src.configuracoes import *
from src.game.objetos import Botao
from os import path
import random


class Interface_Game(Game):

    def play(self):
        self.tela_inicial()
        while self.jogando:
            self.novo()
            if self.game_over:
                self.tela_saida()
            if self.pisou:
                self.animacao_final()
            if self.menu:
                self.tela_inicial()

    def draw_texto(self, texto, tamanho, cor, x, y):

        fonte = pg.font.Font(self.fonte_texto, tamanho)
        texto_surface = fonte.render(texto, True, cor)  # True para anti-alising
        texto_rect = texto_surface.get_rect()
        texto_rect.midtop = (x, y)
        self.tela.blit(texto_surface, texto_rect)

    def draw_titulo_moderno(self, texto, x, y):
        fonte = pg.font.Font(self.fonte_texto, 34)
        # Sombra
        sombra_surface = fonte.render(texto, True, (40, 40, 60))
        sombra_rect = sombra_surface.get_rect(center=(x + 4, y + 4))
        self.tela.blit(sombra_surface, sombra_rect)
        # Título principal
        titulo_surface = fonte.render(texto, True, (138, 43, 226))
        titulo_rect = titulo_surface.get_rect(center=(x, y))
        self.tela.blit(titulo_surface, titulo_rect)
        # Borda branca leve (deslocada, sem blend)
        borda_surface = fonte.render(texto, True, (255, 255, 255))
        borda_rect = borda_surface.get_rect(center=(x - 2, y - 2))
        self.tela.blit(borda_surface, borda_rect)

    def tela_inicial(self):
        pg.mixer.fadeout(1000)
        self.decidindo = True
        self.botao_selecionado = 0

        # Parâmetros para centralização
        num_botoes = 3
        altura_botao = 50
        espacamento = 30
        bloco_altura = num_botoes * altura_botao + (num_botoes - 1) * espacamento
        bloco_topo = (HEIGHT // 2) - (bloco_altura // 2) + 40  # +40 para dar espaço ao título

        # Criação dos botões centralizados verticalmente
        self.botao_jogar = Botao(self, bloco_topo, "JOGAR", True)
        self.botao_opcoes = Botao(self, bloco_topo + altura_botao + espacamento, "OPÇÕES")
        self.botao_sair = Botao(self, bloco_topo + 2 * (altura_botao + espacamento), "SAIR")
        self.botoes = [self.botao_jogar, self.botao_opcoes, self.botao_sair]
        self.opcoes = False

        flocos = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(2, 4)] for _ in range(5)]

        while self.decidindo:
            self.tela.fill(BG_COR)
            self.animar_neve(flocos)
            self.draw_titulo_moderno(TITLE, CENTRO_WIDTH, 60)

            for botao in self.botoes:
                botao.update()

            self.tela_inicial_eventos()

            if self.opcoes:
                self.tela_opcoes(flocos)

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

    def tela_opcoes(self, flocos=None):
        self.botao_selecionado = 0

        num_botoes = 4
        altura_botao = 50
        espacamento = 30
        bloco_altura = num_botoes * altura_botao + (num_botoes - 1) * espacamento
        bloco_topo = (HEIGHT // 2) - (bloco_altura // 2) + 40  # +40 para dar espaço ao título

        # Criação dos botões centralizados verticalmente
        self.botao_audio = Botao(self, bloco_topo, "AUDIO ON" if self.audio else "AUDIO OFF", True)
        self.botao_efeitos = Botao(self, bloco_topo + altura_botao + espacamento, "EFEITOS ON" if self.audio_efeitos else "EFEITOS OFF")
        self.botao_sorte = Botao(self, bloco_topo + 2 * (altura_botao + espacamento), "SORTE ON" if self.sorte else "SORTE OFF")
        self.botao_retornar = Botao(self, bloco_topo + 3 * (altura_botao + espacamento), "RETORNAR")
        self.botoes_opcoes = [
            self.botao_audio,
            self.botao_efeitos,
            self.botao_sorte,
            self.botao_retornar,
        ]

        while self.opcoes:
            self.tela.fill(BG_COR)
            if flocos:
                self.animar_neve(flocos)

            self.draw_titulo_moderno("OPÇÕES", CENTRO_WIDTH, 60)

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
        self.canal_musica.play(self.audio_gameover, loops=-1)
        self.decidindo = True
        self.botao_selecionado = 0

        altura_botao = 50
        espacamento = 30
        num_botoes = 2

        caixa_largura = 300
        caixa_altura = 130
        caixa_x = (WIDTH - caixa_largura) // 2
        caixa_y = (HEIGHT - caixa_altura - 54 - (num_botoes * altura_botao + espacamento)) // 2 + 54

        bloco_topo = caixa_y + caixa_altura + 32

        self.botao_tentar_novamente = Botao(self, bloco_topo, "NOVAMENTE", True)
        self.botao_menu = Botao(self, bloco_topo + altura_botao + espacamento, "MENU", False)
        self.botoes = [self.botao_tentar_novamente, self.botao_menu]

        flocos = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(2, 4)] for _ in range(5)]

        texto_gameover = "GAME OVER"
        texto_motiva = "Continue tentando!\nPipipopo acredita em você."
        if self.recorde < self.pontos:
            self.recorde = self.pontos
            texto_recorde = f"Novo recorde: {self.recorde}!"
            with open(RECORDE_FILE, "w") as f:
                f.write(str(self.pontos))
        else:
            texto_recorde = f"Recorde: {self.recorde}"
        texto_pontuacao = f"Pontuação: {self.pontos}"

        while self.decidindo:
            self.tela.fill(BG_COR)
            self.animar_neve(flocos)

            self.draw_titulo_moderno(texto_gameover, CENTRO_WIDTH, 38)

            caixa_rect = pg.Rect(caixa_x, caixa_y, caixa_largura, caixa_altura)
            sombra_rect = caixa_rect.copy()
            sombra_rect.y += 8
            pg.draw.rect(self.tela, (30, 30, 50), sombra_rect, border_radius=22)
            pg.draw.rect(self.tela, (50, 60, 100), caixa_rect, border_radius=22)
            pg.draw.rect(self.tela, (200, 200, 255), caixa_rect, width=2, border_radius=22)

            padding_top = 18
            padding_bottom = 18
            linha_y = caixa_y + padding_top

            fonte = pg.font.Font(self.fonte_texto, 22)
            pont_surface = fonte.render(texto_pontuacao, True, (255, 255, 255))
            pont_rect = pont_surface.get_rect(center=(CENTRO_WIDTH, linha_y))
            self.tela.blit(pont_surface, pont_rect)

            linha_y += 28
            rec_surface = fonte.render(texto_recorde, True, (255, 223, 0))
            rec_rect = rec_surface.get_rect(center=(CENTRO_WIDTH, linha_y))
            self.tela.blit(rec_surface, rec_rect)

            linha_y += 28
            fonte_menor = pg.font.Font(self.fonte_texto, 16)
            for i, linha in enumerate(texto_motiva.split('\n')):
                msg_surface = fonte_menor.render(linha, True, (220, 220, 255))
                msg_rect = msg_surface.get_rect(center=(CENTRO_WIDTH, linha_y + i * 22))
                self.tela.blit(msg_surface, msg_rect)

            for botao in self.botoes:
                botao.update()

            self.tela_saida_eventos()
            pg.display.flip()

        self.audio_gameover.fadeout(1000)

    def animacao_final(self):
        self.decidindo = True
        self.botao_selecionado = 0
        self.botao_jogar_novamente = Botao(self, 350, "NOVAMENTE", True)
        self.botao_menu = Botao(self, 415, "MENU", False)
        self.botoes = [self.botao_jogar_novamente, self.botao_menu]

        if self.recorde < self.pontos:
            with open(RECORDE_FILE, "w") as f:
                f.write(str(self.pontos))

        while self.decidindo:

            self.tela.fill(BLACK)

            for botao in self.botoes:
                botao.update()

            self.draw_texto("PARABÉNS!", 20, WHITE, CENTRO_WIDTH, HEIGHT / 2 - 40)
            self.draw_texto(
                "Graças a você, Pipipopo realizou",
                18,
                WHITE,
                CENTRO_WIDTH,
                HEIGHT / 2 + 0,
            )
            self.draw_texto(
                "seu sonho de acender no Cosmos.",
                18,
                WHITE,
                CENTRO_WIDTH,
                HEIGHT / 2 + 20,
            )
            self.draw_texto(
                "See you in space, cowboy ;)", 18, WHITE, CENTRO_WIDTH, HEIGHT / 2 + 40
            )

            self.tela_saida_eventos()

            pg.display.flip()

    def tela_saida_eventos(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.decidindo = False
                self.jogando = False
                self.menu = False
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

    def animar_neve(self, flocos):
        for floco in flocos:
            pg.draw.circle(self.tela, (255, 255, 255), (floco[0], floco[1]), floco[2])
            floco[1] += floco[2]  # velocidade proporcional ao tamanho
            if floco[1] > HEIGHT:
                floco[0] = random.randint(0, WIDTH)
                floco[1] = 0
