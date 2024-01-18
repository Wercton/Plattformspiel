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
YELLOW = (255, 255, 0)
BG_COR_SAVE = [0, 155, 155]

# propriedades do Jogador
ACC_JOGADOR = 0.7
FRICCAO_JOGADOR = -0.12
GRAVIDADE_JOGADOR = 0.8

# propriedades do jogo
IMPULSO_POTENCIA = 30
FREQUENCIA_PODER = 5
FREQUENCIA_MOB = 3000
PROBABILICADE_MOB = 0.4

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

JOGADOR_SPRITESHEET_BLUE = "data/imagens/PipipopoSpritesheet.png"
JOGADOR_SPRITESHEET_PINK = "data/imagens/PipipopoSpritesheet2.png"
JOGADOR_SPRITESHEET_GRAY = "data/imagens/PipipopoSpritesheet3.png"
JOGADOR_SPRITESHEET_GREEN = "data/imagens/PipipopoSpritesheet4.png"


# plataformas
WIDTH_PLAT = 15
PLATAFORMA_INICIAL = "data/imagens/Primeira_plataforma.png"

PLATAFORMA_FASE1 = ["data/imagens/Plataforma_100.png",
                    "data/imagens/Plataforma_100_terra2.png",
                    "data/imagens/Plataforma_100_terra3.png",
                    "data/imagens/Plataforma_100_terra4.png",
                    "data/imagens/Plataforma_70_terra5.png"]

PLATAFORMA_FASE2 = ["data/imagens/Plataforma_80_fase2.png",
                    "data/imagens/Plataforma_80_fase2_2.png",
                    "data/imagens/Plataforma_60_fase2_3.png",
                    "data/imagens/Plataforma_60_fase2_4.png",
                    "data/imagens/Plataforma_70_fase2_5.png"]

PLATAFORMA_FASE3 = ["data/imagens/Plataforma_60_fase3_1.png",
                    "data/imagens/Plataforma_40_fase3_3.png",
                    "data/imagens/Plataforma_60_fase3_4.png",
                    "data/imagens/Plataforma_60_fase3_5.png"]

PLATAFORMA_FASE4 = ["data/imagens/Plataforma_45_fase4.png",
                    "data/imagens/Plataforma_30_fase4_2.png"]

PLATAFORMA_RARA = "data/imagens/Plataforma_60_fase3_2.png"

ASTEROIDES = ["data/imagens/Plataforma_50_asteroide.png",
            "data/imagens/Plataforma_50_asteroide_2.png",
            "data/imagens/Plataforma_50_asteroide_3.png"]

# outros sprites
ATENCAO1 = "data/imagens/atencao_vermelho.png"
ATENCAO2 = "data/imagens/atencao_vermelho_claro.png"

FOGUETÃO = "data/imagens/coin.png"
NUVENS_SPRITESHEET = "data/imagens/clouds.png"
NYAH1 = "data/imagens/nyah.png"
NYAH2 = "data/imagens/nyah2.png"
BOTAO = "data/imagens/botao.png"
BOTAO_SELECIONADO = "data/imagens/botao_selecionado.png"
SHINY_STAR1 = "data/imagens/shiny_star_1.png"
SHINY_STAR2 = "data/imagens/shiny_star_2.png"
COMETA1 = "data/imagens/comet1.png"
COMETA2 = "data/imagens/comet2.png"
SPACEX_CARRO = "data/imagens/spacex_car.png"

# audio
CLICK = "data/audio/click.ogg"
MAIN_TRACK = 'data/audio/loneliness.ogg'
MAIN_TRACK_FINAL = 'data/audio/was_it_all_for_nothing.ogg'
MAIN_TRACK_SUSPENSE = 'data/audio/there_is_something_wrong.ogg'
PULO_AUDIO = 'data/audio/cute_jump.ogg'
GAME_OVER_AUDIO = 'data/audio/game_over_audio.ogg'
COIN_AUDIO = 'data/audio/coin01.ogg'
IMPULSO_AUDIO = 'data/audio/jump01.ogg'
