import pygame
from source import setup, tools
from source import constants as CONS

# 主界面金币
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        self.load_coin()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = 280
        self.rect.y = 58

    def load_coin(self):
        sheet = setup.GRAPHIC['item_objects']
        self.frames.append(tools.get_image(sheet, 1, 160, 5, 8, (0, 0, 0), CONS.magnify1))

