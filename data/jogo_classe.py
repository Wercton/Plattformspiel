import pygame as pg
import random
from data.configuracoes import *
from data.personagem import *
from os import path
from data.objetos import *


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
        self.pisou = False  # verifica se zerou o jogo

        self.sprites_geral = pg.sprite.LayeredUpdates()
        self.plataformas = pg.sprite.Group()
        self.plataformas_movendo_direita = pg.sprite.Group()
        self.plataformas_movendo_esquerda = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.poderes = pg.sprite.Group()
        self.nuvens = pg.sprite.Group()
        self.stars = pg.sprite.Group()
        self.cometa = pg.sprite.Group()

        self.pontos = 0
        self.fase = 1
        self.velocidade_plat = 0
        self.prob_plat_movimento = 0
        self.tempo_mob = 0
        self.ultima_mudanca = 0
        self.tem_cometa = 0
        self.tem_carro = 0
        self.final = 0

        self.jogador_spritesheet = random.choice(self.jogadores_spritesheets)
        self.jogador = Jogador(self)

        Plataforma(self, -20, HEIGHT - 15, -1)

        for _ in range(3):
            c = Nuvem(self, self.fase)
            c.rect.y += 400

        self.run()


    def run(self):
        # loop do jogo
        self.partida = True
        while self.partida:
            self.clock.tick(FPS)
            self.eventos()
            self.update()
            self.draw()
        self.BG_COR = [0, 155, 155]


    def update(self):

        self.sprites_geral.update()
        self.verificar_colisoes()

        if not self.verificar_game_over():

            self.subir_tela()  # muda as cores também
            self.movimentar_plataformas()  # aumentar precisão
            
            if not self.pontos % 100:
                self.configurar_fases()

            if not self.final:
                self.spawnar()
            else:
                self.jogador.vel.y -= 1
                if self.jogador.rect.y < -50:
                    self.pisou = 1
                    self.partida = 0


    def eventos(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.partida = False
                self.jogando = False
                self.menu = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if not self.final:
                        self.jogador.pular()
                elif event.key == pg.K_ESCAPE:
                    self.partida = False
                    self.menu = True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    if not self.final:
                        self.jogador.interromper_pulo()


    def draw(self):

        self.tela.fill(self.BG_COR)
        self.sprites_geral.draw(self.tela)
        self.draw_texto(str(self.pontos), 20, YELLOW, CENTRO_WIDTH, 10)

        pg.display.flip()


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
        if self.jogador.vel.y > -0.1:
            hits = pg.sprite.spritecollide(self.jogador, self.plataformas, False)
            for hit in hits:
                if self.jogador.pos.x < hit.rect.right + 15 and \
                self.jogador.rect.x > hit.rect.left - 35:  # cai quando as duas perninhas dele sai da plataforma
                    if self.jogador.pos.y - 5 <= hit.rect.bottom - 2:  # corrigindo bug de transportar para o topo sem alcançar
                        self.jogador.pos.y = hit.rect.top + 1
                        self.jogador.pulando = False
                        self.jogador.interromper_queda()
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
        hits = pg.sprite.spritecollide(self.jogador, self.mobs, False, pg.sprite.collide_mask)
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
            if self.fase < 4:
                if random.randrange(100) < 3:
                    Nuvem(self, self.fase)
            else:
                if random.randrange(100) < 2:
                    agora = pg.time.get_ticks()
                    if agora - self.ultima_mudanca > 6000:
                        self.ultima_mudanca = agora
                        Star(self)
            self.jogador.pos.y += abs(self.jogador.vel.y)
            for star in self.stars:
                star.rect.y += abs(self.jogador.vel.y / 6)
            for spaceObject in self.cometa:
                spaceObject.rect.y += abs(self.jogador.vel.y / 8)
            for nuvem in self.nuvens:
                if nuvem.frente:
                    nuvem.rect.y += abs(self.jogador.vel.y * 1.2)
                else:
                    nuvem.rect.y += abs(self.jogador.vel.y / 3)
            for mob in self.mobs:  # mover mob junto com a tela
                mob.rect.y += abs(self.jogador.vel.y)
            for pltfrms in self.plataformas:  # mover plataformas junto com a tela
                pltfrms.rect.y += abs(self.jogador.vel.y) # usar -= no lugar de abs?
                if pltfrms.rect.top >= HEIGHT:
                    pltfrms.kill()
                    self.pontos += 10
                    if self.BG_COR[1] > 3:
                        self.BG_COR[1] -= 1.5  # 1.5
                        self.BG_COR[2] -= 1.5
    

    def movimentar_plataformas(self):
        # direita
        for plat in self.plataformas_movendo_direita:
            plat.rect.right += self.velocidade_plat
            if plat.rect.left > WIDTH:
                if plat.rect.colliderect(self.jogador.rect):
                    posicao_jogador_plataforma =  self.jogador.pos.x - plat.rect.left
                    plat.rect.right = 0
                    self.jogador.pos.x = plat.rect.left + posicao_jogador_plataforma
                else:
                    plat.rect.right = 0
        # esquerda
        for plat in self.plataformas_movendo_esquerda:
            plat.rect.left -= self.velocidade_plat
            if plat.rect.left < plat.rect.size[0] * -1:
                if plat.rect.colliderect(self.jogador.rect):
                    posicao_jogador_plataforma =  self.jogador.pos.x - plat.rect.left
                    plat.rect.right = WIDTH + plat.rect.size[0]
                    self.jogador.pos.x = plat.rect.left + posicao_jogador_plataforma
                else:
                    plat.rect.right = WIDTH + plat.rect.size[0]


    def configurar_fases(self):
        
        if self.pontos == 1300:
            self.jogador.gravidade = 0
            self.jogador.pulando = 1
            self.final = 1
        elif self.pontos == 1200:
            if not self.tem_carro:
                Astronaut(self)
                self.tem_carro = 1
        elif self.pontos == 1000:
            if not self.tem_cometa:
                Cometa(self)
                self.tem_cometa = 1
        elif self.pontos == 800:  # 800
            self.fase = 4
            self.velocidade_plat = 3
            self.soundtrack.fadeout(3000)
            self.canal_musica.play(self.soundtrack_final, loops = -1)
            self.jogador.gravidade = 0.6
            self.prob_plat_movimento = 0.5
        elif self.pontos == 500:  # 500
            self.fase = 3
            self.velocidade_plat = 2
            self.prob_plat_movimento = 0.3
        elif self.pontos == 200:  # 200
            self.fase = 2
            self.velocidade_plat = 0


    def spawnar(self):
        # spawnando mobs
        agora = pg.time.get_ticks()
        if agora - self.tempo_mob > FREQUENCIA_MOB:
            self.tempo_mob = agora
            if random.random() < PROBABILICADE_MOB:
                Mob(self)
                pass

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

            p = Plataforma(self, random.randrange(0, WIDTH),
                        random.randrange(self.mais_alto, self.mais_baixo), self.fase)

            if p.rect.centerx > WIDTH - p.rect.width//2:
                p.rect.centerx = WIDTH - p.rect.width//2

            if self.fase >= 3:
                r = random.random()
                if r < self.prob_plat_movimento:
                    self.plataformas_movendo_direita.add(p)
                elif r < self.prob_plat_movimento * 2:
                    self.plataformas_movendo_esquerda.add(p)


    def carregar_dados(self):
        # pontuação
        try:
            with open(RECORDE_FILE, 'r+') as f:
                try:
                    self.recorde = int(f.read())
                except:
                    self.recorde = 0
        except:
            with open(RECORDE_FILE, 'w') as f:
                self.recorde = 0
        # música
        self.soundtrack = pg.mixer.Sound(MAIN_TRACK)
        self.soundtrack.set_volume(0.15) #0.15

        self.soundtrack_final = pg.mixer.Sound(MAIN_TRACK_FINAL)
        self.soundtrack_final.set_volume(0.12) #0.05

        self.audio_pulo = pg.mixer.Sound(PULO_AUDIO)
        self.audio_pulo.set_volume(0.04) #0.04

        self.audio_gameover = pg.mixer.Sound(GAME_OVER_AUDIO)
        self.audio_gameover.set_volume(0.1) #0.1

        self.audio_moeda = pg.mixer.Sound(COIN_AUDIO)
        self.audio_moeda.set_volume(0.2) #0.2

        self.audio_click = pg.mixer.Sound(CLICK)

        # spritesheet
        self.spritesheet = Spritesheet(NUVENS_SPRITESHEET)
        self.jogadores_spritesheets = [Spritesheet(JOGADOR_SPRITESHEET_GREEN),\
                                        Spritesheet(JOGADOR_SPRITESHEET_BLUE),\
                                        Spritesheet(JOGADOR_SPRITESHEET_GRAY),\
                                        Spritesheet(JOGADOR_SPRITESHEET_PINK)]
