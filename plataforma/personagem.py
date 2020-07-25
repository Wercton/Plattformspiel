import pygame

class Personagem(pygame.sprite.Sprite):

	tamanhoSprite = (50, 50)

	def __init__(self, imagem):

		pygame.sprite.Sprite.__init__(self)
		self.imagem = pygame.transform.scale(pygame.image.load(imagem), self.tamanhoSprite)
		self.posicao = [50, 50]
		self.pos_vertical = 0
		self.rect = pygame.Rect((self.posicao), (self.tamanhoSprite))
		self.direita = False
		self.esquerda = False


	def setDireita(self, direita):
		self.direita = direita


