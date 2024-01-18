import pygame as pg
import random
from data.configuracoes import LAYER_NUVENS, SHINY_STAR1, SHINY_STAR2, BLACK, WIDTH, HEIGHT


class Star(pg.sprite.Sprite):
    
    def __init__(self, game):
        
        self._layer = LAYER_NUVENS
        self.grupos = game.sprites_geral, game.stars
        pg.sprite.Sprite.__init__(self, self.grupos)
        self.game = game
        
        self.size = 20
        self.imagens = [pg.transform.scale(pg.image.load(SHINY_STAR1), (self.size, self.size)), pg.transform.scale(pg.image.load(SHINY_STAR2), (self.size, self.size))]
        self.image = self.imagens[0]
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-500, -50)
        
        self.ultima_mudanca = 0
        self.frame_atual = 0
        
    def update(self):
        
        agora = pg.time.get_ticks()
        if agora - self.ultima_mudanca > 100:
            self.ultima_mudanca = agora
            self.frame_atual = not self.frame_atual
            self.image = self.imagens[self.frame_atual]
        if self.rect.top > HEIGHT:
            self.kill()
