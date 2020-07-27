import os, sys, random
import pkg_resources.py2_warn
import pygame
from pygame.locals import *

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)



dirpath = os.getcwd()
if getattr(sys, "frozen", False):
	os.chdir(sys._MEIPASS)

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')


class Punho(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)  # chama o iniciador do Sprite
		self.image, self.rect = carregar_imagem('data/fist.png', (60, 60), -1)
		self.soco = 0

	def update(self):
		# movendo o punho
		pos = pygame.mouse.get_pos()
		self.rect.midtop = pos
		if self.soco:
			self.rect.move_ip(5, 10)

	def socão(self, alvo):
		# retorna true se o alvo foi socado
		if not self.soco:
			self.soco = 1
			area_do_alvo = self.rect.inflate(-5, -5)
			return area_do_alvo.colliderect(alvo.rect)

	def errou_socão(self):
		self.soco = 0


class Algum_Babaca(pygame.sprite.Sprite):
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = carregar_imagem('data/palhaco.png', (200, 200), -1)
		tela = pygame.display.get_surface()  # pega o tamnho da tela e o aplica logo em seguida
		self.area = tela.get_rect()
		self.rect.topleft = 10, 10
		self.movimento = -1
		self.tonto = 0

	def update(self):
		# should i run or should i spin
		if self.tonto:
			self._roda_roda()
		else:
			self._corre_mlk()

	def _corre_mlk(self):
		nova_pos = self.rect.move((self.movimento, 0))
		if not self.area.contains(nova_pos):
			if self.rect.left < self.area.left or self.rect.right > self.area.right:
				self.movimento = -self.movimento
				nova_pos = self.rect.move((self.movimento, 0))
				self.image = pygame.transform.flip(self.image, 1, 0)
			self.rect = nova_pos

	def _roda_roda(self):
		centro = self.rect.center
		self.tonto += 12
		if self.tonto >= 360:
			self.tonto = 0
			self.image = self.original
		else:
			rotacionar = pygame.transform.rotate
			self.image = rotacionar(self.original, self.tonto)
		self.rect = self.image.get_rect(center=centro)  # garante que a imagem nunca saia do lugar enquanto rotaciona

	def socado(self):
		if self.movimento >= 0:
			self.movimento += 1
		else:
			self.movimento -= 1

		if not self.tonto:
			self.tonto = 1
			self.original = self.image  # salva a img original pois na rotação ela fica maior


def carregar_imagem(imagem, tamanho, colorkey=None):
	caminho_imagem = os.path.join('.', imagem)
	try:
		imagem = pygame.image.load(caminho_imagem)
		imagem = pygame.transform.scale(imagem, tamanho)
	except pygame.error as message:
		print('Imagem não encontrada:', imagem)
		raise SystemExit(message)
	imagem = imagem.convert()
	if colorkey is not None:
		if colorkey == -1:
			colorkey = imagem.get_at((0, 0))
		imagem.set_colorkey(colorkey, RLEACCEL)
	return imagem, imagem.get_rect()


def carregar_som(som):
	class NoneSound:
		def play(self): pass
	if not pygame.mixer:
		return NoneSound()
	caminho_som = os.path.join('.', som)
	try:
		som = pygame.mixer.Sound(caminho_som)
	except pygame.error as message:
		print('Som não encontrado:', som)
		raise SystemExit(message)
	return som


def criando_fundão(cor):
	imagem_de_fundo = pygame.Surface(tela.get_size())
	imagem_de_fundo = imagem_de_fundo.convert()
	imagem_de_fundo.fill(cor)
	return imagem_de_fundo


def criando_tela(tamanho, nome):
	tela = pygame.display.set_mode(tamanho)
	pygame.display.set_caption(nome)
	pygame.mouse.set_visible(0)
	return tela


def exibindo_pontuacao(pontuacao):
	fonte = pygame.font.Font(None, 26)
	texto_pontuacao = fonte.render("{0} socão".format(pontuacao), 1, (0, 0, 0))
	return texto_pontuacao


def desenhar_texto(texto, cor, tela, x, y):
	fonte = pygame.font.Font(None, 26)
	texto_objeto = fonte.render(texto, 1, cor)
	texto_rect = texto_objeto.get_rect()
	texto_rect.topleft = (x, y)
	return texto_objeto, texto_rect


def menu_principal():

	som_inicio.set_volume(0.07)
	som_inicio.play()

	fundo_menu = pygame.image.load("data/gado.jpg")
	fundo_menu = pygame.transform.scale(fundo_menu, tamanho_tela)

	botao = pygame.image.load('data/botao.png')
	botao = pygame.transform.scale(botao, (135, 100))

	tela.blit(fundo_menu, (0, 0))

	botao_jogar = pygame.Rect(230, 50, 135, 100)

	click = False
	while 1:

		mx, my = pygame.mouse.get_pos()
		pygame.draw.rect(tela, (250, 0, 0), botao_jogar)

		if botao_jogar.collidepoint((mx, my)):
			if click:
				game()

		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.type == K_ESCAPE:
					pygame.quit()
					sys.quit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button:
					click = True

		texto, texto_rect = desenhar_texto("Jogar", (250, 250, 250), tela, 275, 90)

		tela.blit(fundo_menu, (0, 0))
		tela.blit(botao, (230, 50))
		tela.blit(texto, texto_rect)
		todos_sprites.draw(tela)

		pygame.display.update()
		todos_sprites.update()

		tempo.tick(60)


def vitoria():

	som_final = carregar_som('data/vitoria.ogg')
	som_final.play()

	fundo_vitoria = pygame.image.load('data/vitoria.jpg')
	fundo_vitoria = pygame.transform.scale(fundo_vitoria, (tamanho_tela[0]//2,tamanho_tela[1]))

	botao_voltar = pygame.Rect(230, 50, 135, 100)

	click = False
	while 1:

		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.type == K_ESCAPE:
					pygame.quit()
					sys.quit()

		tela.fill((0, 0, 0))
		tela.blit(fundo_vitoria, (0, 0))
		
		fonte_vitoria = pygame.font.SysFont(None, 26)
		texto_vitoria = fonte_vitoria.render("Parabéns, você nocateou o Bolsonaro", False, (255, 0, 0))
		texto_vitoria2 = fonte_vitoria.render("antes dele assumir a presidência.", False, (255, 100, 0))
		texto_vitoria3 = fonte_vitoria.render("E com isso você salvou a vida das", False, (255, 250, 0))
		texto_vitoria4 = fonte_vitoria.render("mais de 100 mil vidas perdidas que", False, (0, 130, 0))
		texto_vitoria5 = fonte_vitoria.render("morreriam devido sua péssima gestão.", False, (0, 0, 200))
		texto_vitoria6 = fonte_vitoria.render("Viva a liberdade de expressão!", False, (210, 0, 170))

		tela.blit(texto_vitoria, (330, 5))
		tela.blit(texto_vitoria2, (330, 25))
		tela.blit(texto_vitoria3, (330, 45))
		tela.blit(texto_vitoria4, (330, 65))
		tela.blit(texto_vitoria5, (330, 85))
		tela.blit(texto_vitoria6, (360, 135))


		pygame.display.update()
		pygame.display.flip()


def game():

	tela.blit(imagem_de_fundo, (0, 0))
	pygame.display.flip()

	botao_voltar = pygame.Rect(500, 0, 135, 20)
	botao = pygame.image.load("data/botao.png")
	botao = pygame.transform.scale(botao, (235, 100))

	primeira_fase = pygame.image.load("data/primeira_fase.jpg")
	primeira_fase = pygame.transform.scale(primeira_fase, tamanho_tela)

	segunda_fase = pygame.image.load("data/segunda_fase.jpg")
	segunda_fase = pygame.transform.scale(segunda_fase, tamanho_tela)

	terceira_fase = pygame.image.load("data/terceira_fase.jpg")
	terceira_fase = pygame.transform.scale(terceira_fase, tamanho_tela)

	quarta_fase = pygame.image.load("data/democracia.jpg")
	quarta_fase = pygame.transform.scale(quarta_fase, tamanho_tela)

	todos_sprites = pygame.sprite.RenderPlain((babaca, punho))
	pontuacao = 0

	fase_atual = primeira_fase

	click = False

	while 1:
		tempo.tick(60)

		mx, my = pygame.mouse.get_pos()
		pygame.draw.rect(tela, (250, 0, 0), botao_voltar)

		for event in pygame.event.get():
			if event.type == QUIT: sys.exit()
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				pass
			elif event.type == MOUSEBUTTONDOWN:
				click = True
				if babaca.tonto == 0:  # consertando bug de murros infinitos
					if punho.socão(babaca):
						som_erro.stop()
						som_queimar.stop()
						som_acerto.play()

						escolher_som_aleatoriamente = random.randint(0, 5)
						if escolher_som_aleatoriamente == 0: som_vagabundo.play()
						elif escolher_som_aleatoriamente == 1: som_queimar.play()
						elif escolher_som_aleatoriamente == 2: som_porra.play()
						
						babaca.socado()
						pontuacao += 1

						if pontuacao == 40:
							som_inicio.stop()
							som_erro.stop()
							som_queimar.stop()
							som_porra.stop()
							som_vagabundo.stop()
							vitoria()

					else:
						som_erro.stop()
						som_erro.play()
						if babaca.movimento >= 0:
							babaca.movimento = 1
						else:
							babaca.movimento = -1
						pontuacao = 0
			elif event.type == MOUSEBUTTONUP:
				punho.errou_socão()

		if pontuacao < 10:
			fase_atual = primeira_fase
		elif pontuacao < 20:
			fase_atual = segunda_fase
		elif pontuacao < 30:
			fase_atual = terceira_fase
		else:
			fase_atual = quarta_fase

		if botao_voltar.collidepoint((mx, my)):
			if click:
				som_erro.stop()
				som_queimar.stop()
				som_inicio.stop()
				menu_principal()

		click = False

		tela.fill((250, 250, 250))
		tela.blit(fase_atual, (0, 0))
		todos_sprites.update()

		texto, texto_rect = desenhar_texto("Voltar", (250, 250, 250), tela, 540, 10)

		tela.blit(fase_atual, (0, 0))
		tela.blit(exibindo_pontuacao(pontuacao), (0, 0))
		tela.blit(botao, (450, -30))
		tela.blit(texto, texto_rect)
		todos_sprites.draw(tela)
		pygame.display.update()  # necessário?
		pygame.display.flip()


if __name__ == '__main__':
	
	pygame.init()

	tamanho_tela = (650, 200)
	tela = criando_tela(tamanho_tela, nome='Socão no Bozo')
	
	imagem_de_fundo = criando_fundão(cor=(250, 250, 250))

	#som_erro = carregar_som('risada.ogg')
	#caminho_som = os.path.join('.\\sons', som)
	som_erro = pygame.mixer.Sound('data/risada.ogg')
	som_acerto = carregar_som('data/PUNCH.wav')
	som_vagabundo = carregar_som('data/vagabundo.ogg')
	som_queimar = carregar_som('data/queimar.ogg')
	som_porra = carregar_som('data/porra.ogg')
	som_inicio = carregar_som('data/bella-ciao.wav')



	babaca = Algum_Babaca()
	punho = Punho()
	todos_sprites = pygame.sprite.RenderPlain((punho))
	tempo = pygame.time.Clock()

	menu_principal()

	pygame.quit()
