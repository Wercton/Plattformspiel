# opções de jogo
TITLE = 'Plattformspiel'
WIDTH = 360
HEIGHT = 480
CENTRO_WIDTH = WIDTH/2
FPS = 30
FONTE_TEXTO = 'ubuntumono' # freemono, arial, freeserif, ubuntumono
RECORDE_FILE = '.recorde.txt'

# cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BG_COR = (0, 155, 155)

# propriedades do Jogador
ACC_JOGADOR = 0.7
FRICCAO_JOGADOR = -0.12
GRAVIDADE_JOGADOR = 0.8

# sprites - Jogador
TAMANHO_JOGADOR = (40, 40)
POSICAO_INICIAL = (WIDTH/2 - TAMANHO_JOGADOR[0]/2, HEIGHT/2 - TAMANHO_JOGADOR[1]/2)
PULO_JOGADOR = 15

JOGADOR_SPRITE = "imagens/Pipipopo.png"
JOGADOR_SPRITE2 = "imagens/Pipipopo2.png"
ANDAR1_SPRITE = "imagens/Pipipopo_andar1.png"
ANDAR2_SPRITE = "imagens/Pipipopo_andar2.png"
PULO_SPRITE = "imagens/Pipipopo_pular.png"
CAIR_SPRITE = "imagens/Pipipopo_cair.png"

# plataformas
WIDTH_PLAT = 15
PLATAFORMAS_LISTA = [(0, HEIGHT - WIDTH_PLAT, WIDTH, WIDTH_PLAT),
                    (WIDTH/3, HEIGHT - (HEIGHT/3), WIDTH/3, WIDTH_PLAT),
                    (10, HEIGHT/2 - 30, 100, WIDTH_PLAT),
                    (WIDTH - WIDTH/4, 100, 80, WIDTH_PLAT),
                    (WIDTH/3, 10, WIDTH/3, WIDTH_PLAT)]
