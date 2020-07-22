import os, sys, random
import pygame
from pygame.locals import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')


class Punho(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)  # chama o iniciador do Sprite
		self.image, self.rect = carregar_imagem('fist.png', (60, 60), -1)
		#pygame.transform.scale(self.image, (20, 20))
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
		self.image, self.rect = carregar_imagem('palhaco.png', (200, 200), -1)
		#pygame.transform.scale(self.image, (20, 20))
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
				self.movimento = -self.movimento  # multiplicar por -1 depois?
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
			rotacionar = pygame.transform.rotate  # ()?
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
	caminho_imagem = os.path.join('.\\imagens', imagem)
	try:
		imagem = pygame.image.load(caminho_imagem)
		imagem = pygame.transform.scale(imagem, tamanho)
	except pygame.error as message:
		print('Imagem não encontrada:', imagem)
		raise SystemExit(message)
	imagem = imagem.convert()  # permanece?
	if colorkey is not None:
		if colorkey is -1:
			colorkey = imagem.get_at((0, 0))
		imagem.set_colorkey(colorkey, RLEACCEL)
	return imagem, imagem.get_rect()


def carregar_som(som):
	class NoneSound:
		def play(self): pass
	if not pygame.mixer:
		return NoneSound()
	caminho_som = os.path.join('.\\sons', som)
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


def criando_font():
	fonte = pygame.font.Font(None, 26)
	texto = fonte.render("METE O SOCÃO NESSE GENOCIDA DE MERDA", 1, (10, 10, 10))
	texto_pos = texto.get_rect(centerx=imagem_de_fundo.get_width()//2)
	imagem_de_fundo.blit(texto, texto_pos)


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
	#tela.blit(texto_objeto, texto_rect)


def menu_principal():

	caminho_imagem = os.path.join('.\\imagens', 'gado.jpg')
	fundo_menu = pygame.image.load(caminho_imagem)
	fundo_menu = pygame.transform.scale(fundo_menu, tamanho_tela)

	caminho_imagem = os.path.join('.\\imagens', 'botao.png')
	botao = pygame.image.load(caminho_imagem)
	botao = pygame.transform.scale(botao, (135, 100))

	tela.blit(fundo_menu, (0, 0))

	botao_1 = pygame.Rect(230, 50, 135, 100)

	click = False
	while 1:

		mx, my = pygame.mouse.get_pos()
		pygame.draw.rect(tela, (250, 0, 0), botao_1)

		if botao_1.collidepoint((mx, my)):
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


def game():

	tela.blit(imagem_de_fundo, (0, 0))
	pygame.display.flip()

	caminho_imagem = os.path.join('.\\imagens', 'primeira_fase.jpg')
	primeira_fase = pygame.image.load(caminho_imagem)
	primeira_fase = pygame.transform.scale(primeira_fase, tamanho_tela)

	caminho_imagem = os.path.join('.\\imagens', 'segunda_fase.jpg')
	segunda_fase = pygame.image.load(caminho_imagem)
	segunda_fase = pygame.transform.scale(segunda_fase, tamanho_tela)

	caminho_imagem = os.path.join('.\\imagens', 'terceira_fase.jpg')
	terceira_fase = pygame.image.load(caminho_imagem)
	terceira_fase = pygame.transform.scale(terceira_fase, tamanho_tela)

	todos_sprites = pygame.sprite.RenderPlain((babaca, punho))
	pontuacao = 0

	fase_atual = primeira_fase

	while 1:
		tempo.tick(60)

		for event in pygame.event.get():
			if event.type == QUIT: sys.exit()
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				pass
			elif event.type == MOUSEBUTTONDOWN:
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
					else:
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
		else:
			fase_atual = terceira_fase

		tela.fill((250, 250, 250))
		tela.blit(fase_atual, (0, 0))
		criando_font()
		todos_sprites.update()
		tela.blit(exibindo_pontuacao(pontuacao), (0, 0))
		todos_sprites.draw(tela)
		pygame.display.update()  # necessário?
		pygame.display.flip()


if __name__ == '__main__':
	
	pygame.init()

	tamanho_tela = (650, 200)
	tela = criando_tela(tamanho_tela, nome='Socão no Bozo')
	
	imagem_de_fundo = criando_fundão(cor=(250, 250, 250))
	criando_font()

	som_erro = carregar_som('risada.ogg')  # encontrar um
	som_acerto = carregar_som('PUNCH.wav')
	som_vagabundo = carregar_som('vagabundo.ogg')
	som_queimar = carregar_som('queimar.ogg')
	som_porra = carregar_som('porra.ogg')

	babaca = Algum_Babaca()
	punho = Punho()
	todos_sprites = pygame.sprite.RenderPlain((punho))
	tempo = pygame.time.Clock()

	menu_principal()

	pygame.quit()
