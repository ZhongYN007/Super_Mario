import pygame
from source import setup,tools
from source import constants as CONS

def create_enemy(enemy_data):
    enemy_type = enemy_data['type']
    x = enemy_data['x']
    y_bottom = enemy_data['y']
    direction = enemy_data['direction']
    color = enemy_data['color']
    if enemy_type == 0:
        enemy = Goomba(x,y_bottom,direction,'goomba',color)
    elif enemy_type == 1:
        enemy = Koopa(x,y_bottom,direction,'koopa',color)
    return enemy

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y_bottom, direction, name, frame_rects):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.name = name
        self.frame_index = 0
        self.left_frames = []
        self.right_frames = []

        self.load_frames(frame_rects)
        self.frames = self.left_frames if self.direction == 0 else self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y_bottom


    def load_frames(self, frame_rects):
        for frame_rect in frame_rects:
            left_frame = tools.get_image(setup.GRAPHIC['enemies'],*frame_rect,(0,0,0),CONS.magnify1)
            right_frame = pygame.transform.flip(left_frame,True,False)
            self.left_frames.append(left_frame)
            self.right_frames.append(right_frame)


class Goomba(Enemy):
    def __init__(self,x,y,direction,name,color):
        bright_frames_rect = [(0, 16, 16, 16),(16,16,16,16) ,(32, 16, 16, 16)]
        dark_frames_rect = [(0, 48, 16, 16), (16, 48, 16, 16),(32,48,16,16)]

        if not color:
            frame_rects = bright_frames_rect
        else:
            frame_rects = dark_frames_rect

        Enemy.__init__(self,x, y, direction, name,  frame_rects)

class Koopa(Enemy):
    def __init__(self, x, y, direction, name, color):
        bright_frames_rect = [(96, 9, 16, 22), (112, 9, 16, 22), (160, 9, 16, 22)]
        dark_frames_rect = [(96, 72, 16, 22), (112, 72, 16, 22), (160, 72, 16, 22)]

        if not color:
            self.frame_rects = bright_frames_rect
        else:
            self.frame_rects = dark_frames_rect

        Enemy.__init__(self,x, y, direction, name, self.frame_rects)
