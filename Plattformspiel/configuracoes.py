# opções de jogo
TITLE = 'Plattformspiel'
WIDTH = 580
HEIGHT = 360
FPS = 30

# cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# propriedades do Jogador
ACC_JOGADOR = 0.5
FRICCAO_JOGADOR = -0.12
GRAVIDADE_JOGADOR = 0.8

# sprites - Jogador
TAMANHO_JOGADOR = (50, 50)
JOGADOR_SPRITE = "./imagens/delta_roxo.png"
POSICAO_INICIAL = (WIDTH/2 - TAMANHO_JOGADOR[0]/2, HEIGHT/2 - TAMANHO_JOGADOR[1]/2)

# plataformas
PLATAFORMAS_LISTA = [(0, HEIGHT - 25, WIDTH, 25),
                    (WIDTH/3, HEIGHT - (HEIGHT/3), WIDTH/3, 25),
                    (WIDTH/7, HEIGHT/3, 100, 25),
                    (WIDTH - WIDTH/4, 100, 80, 25)]
