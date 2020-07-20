import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

imagem = 'corona_mask.png'
som = 'laser1.wav'

class Punho(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)  # chama o iniciador do Sprite
		self.image, self.rect = carregar_imagem('fist.png', -1)
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
		self.image, self.rect = carregar_imagem('palhaco.png', -1)
		#pygame.transform.scale(self.image, (20, 20))
		tela = pygame.display.get_surface()  # pega o tamnho da tela e o aplica logo em seguida
		self.area = tela.get_rect()
		self.rect.topleft = 10, 10
		self.movimento = 9
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
		if not self.tonto:
			self.tonto = 1
			self.original = self.image  # salva a img original pois na rotação ela fica maior


def carregar_imagem(imagem, colorkey=None):
	caminho_imagem = os.path.join('C:\\Users\\Wercton\\Desktop\\Profissional\\python aleatorio\\pygame', imagem)
	try:
		imagem = pygame.image.load(caminho_imagem)
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
	caminho_som = os.path.join('C:\\Users\\Wercton\\Desktop\\Profissional\\python aleatorio\\pygame\\sound', som)
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


if __name__ == '__main__':
	
	pygame.init()

	tela = criando_tela(tamanho=(768, 560), nome='Socão no Bozo')

	imagem_de_fundo = criando_fundão(cor=(250, 250, 250))
	criando_font()

	tela.blit(imagem_de_fundo, (0, 0))
	pygame.display.flip()

	som_erro = None  # encontrar um
	som_acerto = carregar_som('laser1.wav')
	babaca = Algum_Babaca()
	punho = Punho()
	todos_sprites = pygame.sprite.RenderPlain((babaca, punho))
	tempo = pygame.time.Clock()

	while 1:
		tempo.tick(60)

		for event in pygame.event.get():
			if event.type == QUIT: sys.exit()
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				pass
			elif event.type == MOUSEBUTTONDOWN:
				if punho.socão(babaca):
					som_acerto.play()
					babaca.socado()
				else:
					print('missed!')
			elif event.type == MOUSEBUTTONUP:
				punho.errou_socão()

		todos_sprites.update()
		tela.blit(imagem_de_fundo, (0, 0))
		todos_sprites.draw(tela)
		pygame.display.flip()
