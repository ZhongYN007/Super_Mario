import pygame
from source import setup
from source import tools
from source import constants as CONS
from source.components import information
from source import sounds

# 主菜单界面
class MainMenu:
    def __init__(self):
        game_info = {
            'score': 0,
            'score': 0,
            'lives': 3
        }
        self.start(game_info)

    def start(self,game_info):
        self.game_info = game_info # 用于接受上一个阶段传送过来的关键信息
        self.setup_background()
        self.setup_player()
        self.setup_cursor()  # 设置光标
        self.info = information.Info('main_menu', self.game_info)
        self.finished = False
        self.next = 'load_screen' #下一阶段
        sounds.pygame.mixer.music.play()
    def setup_background(self):
        self.background = setup.GRAPHIC['level_1']
        self.background_rect = self.background.get_rect()  # 获得图片的矩形
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width*CONS.magnify1),int(self.background_rect.height*CONS.magnify1)))
        self.viewport = setup.SCREEN.get_rect()  # 获取背景图
        self.caption = tools.get_image(setup.GRAPHIC['title_screen'], 1, 60, 176, 88, (255, 0, 220), CONS.magnify1)
    # 载入马里奥图片
    def setup_player(self):
        self.player = tools.get_image(setup.GRAPHIC['mario_bros'], 178, 32, 12, 16, (0, 0, 0), CONS.magnify2)

   # 游戏的开始
    def setup_cursor(self):
        self.cursor = pygame.sprite.Sprite()
        self.cursor.image = tools.get_image(setup.GRAPHIC['item_objects'], 24, 160, 8, 8, (0, 0, 0), CONS.magnify2)  # 光标
        self.cursor.state = 'Start'

    def update_cursor(self, keys):
      if keys[pygame.K_RETURN]:
          self.recovery()  #重置游戏信息
          if self.cursor.state == 'Start':
              self.finished = True

    def update(self, surface, keys):

        self.update_cursor(keys)

        surface.blit(self.background, self.viewport)
        surface.blit(self.caption, (170, 100))
        surface.blit(self.player, (110, 490))
        #surface.blit(self.cursor, (220,360))

        #  self.info.update()
        self.info.draw(surface)

    def recovery(self):
        self.game_info.update({
            'score': 0,
            'coin': 0,
            'lives':3
        })