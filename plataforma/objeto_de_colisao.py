import pygame

class Objeto_colisao:

	def __init__(self):
		self.posicao = (100, 100)
		self.tamanho = (100, 50)
		self.rect = pygame.Rect(self.posicao, self.tamanho)
