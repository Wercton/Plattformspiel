import pygame as pg
from .settings import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_SIZE, 0)
        self.clock = pg.time.Clock()
        pg.display.set_caption(TITLE)
        self.running = True
        self.playing = False

    def newGame(self):
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.draw()
            pg.display.update()

    def events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.playing = False
                self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        pg.draw.circle(self.screen, YELLOW, (WIDTH / 2, HEIGHT / 2), 50, 0)
