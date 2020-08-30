import pygame as pg
import jogo_classe


def gaming():

    game = jogo_classe.Game()
    game.tela_inicial()
    while game.jogando:
        game.novo()
        game.tela_saida()


if __name__ == '__main__':

    gaming()
