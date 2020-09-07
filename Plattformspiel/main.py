import pygame as pg
import jogo_classe


def gaming():

    game = jogo_classe.Game()

    game.tela_inicial()
    while game.jogando:
        game.novo()
        if game.game_over:
            game.tela_saida()
        if game.menu:
            game.tela_inicial()


if __name__ == '__main__':

    gaming()
