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
BG_COR_SAVE = [0, 155, 155]

# propriedades do Jogador
ACC_JOGADOR = 0.7
FRICCAO_JOGADOR = -0.12
GRAVIDADE_JOGADOR = 0.8

# propriedades do jogo
IMPULSO_POTENCIA = 30
FREQUENCIA_PODER = 5
FREQUENCIA_MOB = 5000
PROBABILICADE_MOB = 0.3

# layers
LAYER_PLATAFORMA = 1
LAYER_JOGADOR = 2
LAYER_MOB = 2
LAYER_PODER = 1
LAYER_NUVENS = 0
LAYER_NUVENS_FRENTE = 3
LAYER_SISTEMA = 5

# sprites - Jogador
TAMANHO_JOGADOR = (40, 40)
POSICAO_INICIAL = (TAMANHO_JOGADOR[0], HEIGHT - TAMANHO_JOGADOR[1]/2)
PULO_JOGADOR = 17

JOGADOR_SPRITE = "imagens/Pipipopo.png"
JOGADOR_SPRITE2 = "imagens/Pipipopo2.png"
ANDAR1_SPRITE = "imagens/Pipipopo_andar1.png"
ANDAR2_SPRITE = "imagens/Pipipopo_andar2.png"
PULO_SPRITE = "imagens/Pipipopo_pular.png"
CAIR_SPRITE = "imagens/Pipipopo_cair.png"

# plataformas
WIDTH_PLAT = 15
PLATAFORMA_INICIAL = "imagens/Primeira_plataforma.png"

PLATAFORMA_FASE1 = ["imagens/Plataforma_100.png",
                    "imagens/Plataforma_100_terra2.png",
                    "imagens/Plataforma_100_terra3.png",
                    "imagens/Plataforma_100_terra4.png",
                    "imagens/Plataforma_70_terra5.png"]

PLATAFORMA_FASE2 = ["imagens/Plataforma_80_fase2.png",
                    "imagens/Plataforma_80_fase2_2.png",
                    "imagens/Plataforma_60_fase2_3.png",
                    "imagens/Plataforma_60_fase2_4.png",
                    "imagens/Plataforma_70_fase2_5.png"]

PLATAFORMA_FASE3 = ["imagens/Plataforma_60_fase3_1.png",
                    "imagens/Plataforma_40_fase3_3.png",
                    "imagens/Plataforma_60_fase3_4.png",
                    "imagens/Plataforma_60_fase3_5.png"]

PLATAFORMA_FASE4 = ["imagens/Plataforma_45_fase4.png",
                    "imagens/Plataforma_30_fase4_2.png"]

PLATAFORMA_RARA = "imagens/Plataforma_60_fase3_2.png"

ASTEROIDES = ["imagens/Plataforma_50_asteroide.png",
            "imagens/Plataforma_50_asteroide_2.png",
            "imagens/Plataforma_50_asteroide_3.png"]

# outros sprites
FOGUETÃO = "imagens/coin.png"
NUVENS_SPRITESHEET = "imagens/clouds.png"
NYAH1 = "imagens/nyah.png"
NYAH2 = "imagens/nyah2.png"
BOTAO = "imagens/botao.png"
BOTAO_SELECIONADO = "imagens/botao_selecionado.png"

# audio
CLICK = "click.ogg"
MAIN_TRACK = 'loneliness.ogg'
MAIN_TRACK_FINAL = 'was_it_all_for_nothing.ogg'
MAIN_TRACK_SUSPENSE = "there_is_something_wrong.ogg"
PULO_AUDIO = 'cute_jump.ogg'
GAME_OVER_AUDIO = 'game_over_audio.ogg'
COIN_AUDIO = 'coin01.ogg'
IMPULSO_AUDIO = 'jump01.ogg'
