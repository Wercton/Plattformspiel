import pygame, sys
from pygame.locals import *
import personagem
import objeto_de_colisao

tamanhoTela = (400, 400)
clock = pygame.time.Clock()


def configurando_tela():

	pygame.init()

	tela = pygame.display.set_mode(tamanhoTela, 0, 32)
	pygame.display.set_caption("Jogo de Plataforma")

	return tela


def fabrica_de_objeto():

	teste = objeto_de_colisao.Objeto_colisao()
	
	return teste


def jogo_loop():

	while 1:

		tela.fill((0, 0, 0))
		tela.blit(delta.imagem, delta.posicao)

		movimento_jogador_jogo_loop()

		verificar_colisao_jogo_loop()

		evento_jogo_loop()

		pygame.display.update()
		clock.tick(60)  # forçando o fps para 60


def verificar_colisao_jogo_loop():

	if delta.rect.colliderect(teste.rect):
		pygame.draw.rect(tela, (250, 0, 0), teste.rect)
	else:
		pygame.draw.rect(tela, (0, 250, 0), teste.rect)


def movimento_jogador_jogo_loop():

	if delta.posicao[1] > tamanhoTela[1] - delta.imagem.get_height():
		delta.pos_vertical = -delta.pos_vertical
	else:
		delta.pos_vertical += 0.2
	delta.posicao[1] += delta.pos_vertical

	if delta.direita:
		delta.posicao[0] += 4
	if delta.esquerda:
		delta.posicao[0] -= 4

	delta.rect.x = delta.posicao[0]
	delta.rect.y = delta.posicao[1]


def evento_jogo_loop():

	for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_RIGHT:
					delta.direita = True
				if event.key == K_LEFT:
					delta.esquerda = True
			if event.type == KEYUP:
				if event.key == K_RIGHT:
					delta.direita = False
				if event.key == K_LEFT:
					delta.esquerda = False


if __name__ == '__main__':

	tela = configurando_tela()
	delta = personagem.Personagem("imagens/delta_roxo.png")
	teste = fabrica_de_objeto()
	jogo_loop()