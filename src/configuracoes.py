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

JOGADOR_SPRITESHEET_BLUE = "assets/imagens/PipipopoSpritesheet.png"
JOGADOR_SPRITESHEET_PINK = "assets/imagens/PipipopoSpritesheet2.png"
JOGADOR_SPRITESHEET_GRAY = "assets/imagens/PipipopoSpritesheet3.png"
JOGADOR_SPRITESHEET_GREEN = "assets/imagens/PipipopoSpritesheet4.png"


# plataformas
WIDTH_PLAT = 15
PLATAFORMA_INICIAL = "assets/imagens/Primeira_plataforma.png"

PLATAFORMA_FASE1 = [
    "assets/imagens/Plataforma_100.png",
    "assets/imagens/Plataforma_100_terra2.png",
    "assets/imagens/Plataforma_100_terra3.png",
    "assets/imagens/Plataforma_100_terra4.png",
    "assets/imagens/Plataforma_70_terra5.png"
]

PLATAFORMA_FASE2 = [
    "assets/imagens/Plataforma_80_fase2.png",
    "assets/imagens/Plataforma_80_fase2_2.png",
    "assets/imagens/Plataforma_60_fase2_3.png",
    "assets/imagens/Plataforma_60_fase2_4.png",
    "assets/imagens/Plataforma_70_fase2_5.png"
]

PLATAFORMA_FASE3 = [
    "assets/imagens/Plataforma_60_fase3_1.png",
    "assets/imagens/Plataforma_40_fase3_3.png",
    "assets/imagens/Plataforma_60_fase3_4.png",
    "assets/imagens/Plataforma_60_fase3_5.png"
]

PLATAFORMA_FASE4 = [
    "assets/imagens/Plataforma_45_fase4.png",
    "assets/imagens/Plataforma_30_fase4_2.png"
]

PLATAFORMA_RARA = "assets/imagens/Plataforma_60_fase3_2.png"

ASTEROIDES = [
    "assets/imagens/Plataforma_50_asteroide.png",
    "assets/imagens/Plataforma_50_asteroide_2.png",
    "assets/imagens/Plataforma_50_asteroide_3.png"
]

# outros sprites
ATENCAO1 = "assets/imagens/atencao_vermelho.png"
ATENCAO2 = "assets/imagens/atencao_vermelho_claro.png"
FOGUETÃO = "assets/imagens/coin.png"
NUVENS_SPRITESHEET = "assets/imagens/clouds.png"
NYAH1 = "assets/imagens/nyah.png"
NYAH2 = "assets/imagens/nyah2.png"
BOTAO = "assets/imagens/botao.png"
BOTAO_SELECIONADO = "assets/imagens/botao_selecionado.png"
SHINY_STAR1 = "assets/imagens/shiny_star_1.png"
SHINY_STAR2 = "assets/imagens/shiny_star_2.png"
COMETA1 = "assets/imagens/comet1.png"
COMETA2 = "assets/imagens/comet2.png"
SPACEX_CARRO = "assets/imagens/spacex_car.png"

# audio
CLICK = "assets/audio/click.ogg"
MAIN_TRACK = "assets/audio/loneliness.ogg"
MAIN_TRACK_FINAL = "assets/audio/was_it_all_for_nothing.ogg"
MAIN_TRACK_SUSPENSE = "assets/audio/there_is_something_wrong.ogg"
PULO_AUDIO = "assets/audio/cute_jump.ogg"
GAME_OVER_AUDIO = "assets/audio/game_over_audio.ogg"
COIN_AUDIO = "assets/audio/coin01.ogg"
IMPULSO_AUDIO = "assets/audio/jump01.ogg"
