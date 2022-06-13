import pygame
import os

 # 游戏的运行
class Game:
    def __init__(self, state_dict, start_state):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()  # 跟踪游戏运行的时间
        self.keys = pygame.key.get_pressed()
        self.state_dict = state_dict
        self.state = self.state_dict[start_state]
    # 游戏主控类
    def update(self):
      if self.state.finished:
          game_info = self.state.game_info
          next_state = self.state.next
          self.state.finished = False
          self.state = self.state_dict[next_state]
          self.state.start(game_info)
      self.state.update(self.screen,self.keys)
        # 运行游戏
    def run(self):

       while True:
           for op in pygame.event.get():
               if op.type == pygame.QUIT:
                   pygame.display.quit()
                   quit()
               elif op.type == pygame.KEYDOWN:
                   self.keys = pygame.key.get_pressed()
               elif op.type == pygame.KEYUP:
                   self.keys = pygame.key.get_pressed()
           self.update()

           pygame.display.update()
           self.clock.tick(60)  # 控制帧速率


def load_graphics(path, accept=('.jpg', '.png', '.gif', '.bmp')):
    graphics = {}
    for pic in os.listdir(path):   # 遍历文件夹
        name, ext = os.path.splitext(pic)  # 拆分文件名和格式
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(path, pic))
            if img.get_alpha():  # 转换为带透明层的图片格式
                img = img. convert_alpha()
            else:
                img = img.convert()   # 转换为普通的图片格式
            graphics[name] = img
    return graphics


def get_image(sheet, x, y, width, height, colorkey, scale): # 快速抠图底色，放大倍数
    image = pygame.Surface((width, height))
    image.blit(sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(colorkey)
    image = pygame.transform.scale(image, (int(width*scale),int(height*scale)))   # 放大图片
    return image



