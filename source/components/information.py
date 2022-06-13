import pygame
from source import constants as CONS
from source.components import coin
from source import setup,tools
pygame.font.init()


class Info:

     def __init__(self, state,game_info):  # 传递不同阶段游戏文字信息
         self.state = state
         self.game_info = game_info
         self.create_state_labels()  # 某个阶段特有文字
         self.create_info_labels()  # 通用信息
         self.coin = coin.Coin()
     def create_state_labels(self):
         self.state_labels = []
         if self.state == 'main_menu':
             self.state_labels.append((self.create_label('Press Enter to Start!'), (265, 360)))
         elif self.state == 'load_screen':
             self.state_labels.append((self.create_label('WORLD'),(280,200)))
             self.state_labels.append((self.create_label('1 - 1'),(430,200)))
             self.state_labels.append((self.create_label('X   {}'.format(self.game_info['lives'])), (380, 280)))
             self.player_image = tools.get_image(setup.GRAPHIC['mario_bros'],178,32,12,16,(0,0,0),CONS.magnify2)
         elif self.state == 'game_over':
             self.state_labels.append((self.create_label('GAME OVER'), (280, 300)))
     def create_info_labels(self):
         self.labels2 = []
         self.labels2.append((self.create_label('MARIO'), (75,30)))
         self.labels2.append((self.create_label('WORLD'), (450,30)))
         self.labels2.append((self.create_label('TIME'), (625, 30)))
         self.labels2.append((self.create_label('000000'), (75,55)))
         self.labels2.append((self.create_label('x00'), (300, 55)))
         self.labels2.append((self.create_label('1 - 1'), (480, 55)))

     def create_label(self, label, size=40, width_scale=1.25, height_scale=1):  # 公共方法
         font = pygame.font.SysFont('Keyboard.ttf', size) #字体
         label_image = font.render(label, 1, (255, 255, 255))  # '1'代表是否抗锯齿，白色
         return label_image

     def update(self):
         pass

     def draw(self, surface):
         for writing in self.state_labels:
             surface.blit(writing[0], writing[1])
         for writing in self.labels2:
             surface.blit(writing[0], writing[1])
        # 金币
         surface.blit(self.coin.image, self.coin.rect)

         if self.state == 'load_screen':
             surface.blit(self.player_image,(300,270))
