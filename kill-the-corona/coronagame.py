import pygame, sys, random


def update_position(match=False):
	global corona_pos, coronarect, size, speed, score
	# atualiza a posição no eixo horizontal
	corona_pos[0] -= speed

	# verifica se imagem saiu da tela
	if (corona_pos[0] + coronarect.size[0]) <= 0 or match:
		corona_pos[0] = size[0]
		corona_pos[1] = random.randint(coronarect.size[0], size[1] - coronarect.size[0])

		if speed < 50:
			speed += 2.5

		if not match:
			if score > 0:
				score -= 1



def score_text(score, speed):
	font = pygame.font.Font(None, 30)
	text = font.render('Pontuação: ' + str(score) + ' - Velocidade: ' + str(speed) + 'x', 1, WHITE)
	return text


if __name__ == "__main__":

	# inicializa a pygame
	pygame.init()

	# define cores no formato RGB
	WHITE = (255, 255, 255)
	BLACK = (0, 0, 0)

	# janela
	size = 800, 600
	window = pygame.display.set_mode(size)
	pygame.display.set_caption("Corona Game")

	# imagem
	img_corona = pygame.image.load('corona_mask.png')
	img_corona = pygame.transform.scale(img_corona, (60, 60))
	corona_pos = [size[0], random.randint(0, size[1])]
	coronarect = img_corona.get_rect()

	speed = 5
	score = 0

	done = True  # flag para o loop principal da aplicação
	corona = None  # serve para verificar colisão

	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if corona.collidepoint(event.pos):
					score += 1
					update_position(True)
				else:
					if score != 0:
						score -= 1
		
		window.fill(BLACK)  # preenche o fundo
		corona = window.blit(img_corona, corona_pos) # desenha a imagem
		window.blit(score_text(score, speed), (0, 0))  # desenha o texto
		pygame.display.update()  # atualiza a tela
		pygame.time.delay(100)
		update_position()  # atualiza posição / por que necessário?

	pygame.quit()
