import pygame
from source import constants as CONS
from source import tools
pygame.init()
SCREEN = pygame.display.set_mode((CONS.WEIGHT,  CONS.HEIGHT))
GRAPHIC = tools.load_graphics('resources/graphics') #所有用到的图片载入到列表中