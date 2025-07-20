import pygame as pg
from src.game.jogo_classe import Game
from src.configuracoes import *
from src.game.objetos import Botao
from os import path


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

        self.botoes_opcoes = [
            self.botao_audio,
            self.botao_efeitos,
            self.botao_sorte,
            self.botao_retornar,
        ]

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
        self.canal_musica.play(self.audio_gameover, loops=-1)
        self.decidindo = True
        self.botao_selecionado = 0
        self.botao_tentar_novamente = Botao(self, 350, "NOVAMENTE", True)
        self.botao_menu = Botao(self, 415, "MENU", False)
        self.botoes = [self.botao_tentar_novamente, self.botao_menu]

        if self.recorde < self.pontos:
            self.recorde = self.pontos
            texto_recorde = "Novo recorde: " + str(self.recorde) + "!"
            self.draw_texto(texto_recorde, 40, WHITE, CENTRO_WIDTH, HEIGHT / 4 + 20)
            with open(RECORDE_FILE, "w") as f:
                f.write(str(self.pontos))
        else:
            texto_pontucao = "Pontuação: " + str(self.pontos)
            texto_recorde = "Recorde: " + str(self.recorde)
            self.draw_texto(texto_pontucao, 30, WHITE, CENTRO_WIDTH, HEIGHT / 4)
            self.draw_texto(texto_recorde, 20, WHITE, CENTRO_WIDTH, HEIGHT / 4 + 45)

        while self.decidindo:

            self.tela.fill(self.BG_COR)

            for botao in self.botoes:
                botao.update()

            if self.recorde < self.pontos:
                self.recorde = self.pontos
                texto_recorde = "Novo recorde: " + str(self.recorde) + "!"
                self.draw_texto(texto_recorde, 40, WHITE, CENTRO_WIDTH, HEIGHT / 4 + 20)
                with open(RECORDE_FILE, "w") as f:
                    f.write(str(self.pontos))
            else:
                texto_pontucao = "Pontuação: " + str(self.pontos)
                texto_recorde = "Recorde: " + str(self.recorde)
                self.draw_texto(
                    texto_pontucao, 30, WHITE, CENTRO_WIDTH, HEIGHT / 4 - 20
                )
                self.draw_texto(texto_recorde, 20, WHITE, CENTRO_WIDTH, HEIGHT / 4 + 25)

            self.draw_texto(
                "Não foi dessa vez! :(", 20, BLACK, CENTRO_WIDTH, HEIGHT / 2 - 40
            )
            self.draw_texto(
                "Mas não se procupe, não será uma",
                18,
                BLACK,
                CENTRO_WIDTH,
                HEIGHT / 2 + 0,
            )
            self.draw_texto(
                '"quedinha" que desmotivará Pipipopo.',
                18,
                BLACK,
                CENTRO_WIDTH,
                HEIGHT / 2 + 20,
            )
            self.draw_texto(
                "Ele passa bem e está pronto para",
                18,
                BLACK,
                CENTRO_WIDTH,
                HEIGHT / 2 + 40,
            )
            self.draw_texto(
                "tentar outra vez!", 18, BLACK, CENTRO_WIDTH, HEIGHT / 2 + 60
            )

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
