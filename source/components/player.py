import pygame
from source import tools, setup
from source import constants as CONS
import json
import os


# 玩家信息
class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.load_data()
        self.setup_states()
        self.setup_velocities()
        self.setup_timers()
        self.load_images()

        '''
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        '''
    def load_data(self):
        file_name = self.name + '.json'
        file_path = os.path.join('source/data/player', file_name)
        with open(file_path) as f:
            self.player_data = json.load(f) #字典


    def setup_states(self):  # 主角状态
        self.state = 'stand'
        self.face_right = True
        self.dead = False
        self.big = False
        self.can_jump = True

    def setup_velocities(self):
        speed = self.player_data['speed']
        self.x_v = 0
        self.y_v = 0

        self.max_walk_v = speed['max_walk_speed']
        self.max_run_v = speed['max_run_speed']
        self.max_y_v = speed['max_y_velocity']
        self.jump_v = speed['jump_velocity']
        self.walk_a = speed['walk_accel']
        self.run_accel  = speed['run_accel']
        self.turn_accel = speed['turn_accel'] # 转身加速度
        self.gravity = CONS.GRAVITY
        self.anti_gravity = CONS.ANTI_GRAVITY
        self.max_x_v = self.max_walk_v
        self.x_a = self.walk_a

    def setup_timers(self):
        self.walking_timer = 0
        self.transtion_timer = 0
        self.death_timer = 0

    def load_images(self):
        sheet = setup.GRAPHIC['mario_bros']
        frame_rects = self.player_data['image_frames']
        # 上下左右移动
        self.right_small_frames = []
        self.right_big_frames = []
        self.left_small_frames = []
        self.left_big_frames = []

        self.small_frames = [self.right_small_frames, self.left_small_frames]
        self.big_frames = [self.right_big_frames, self.left_big_frames]

        self.all_frames = [self.right_small_frames, self.right_big_frames, self.left_small_frames, self.left_big_frames]
        self.right_frames = self.right_small_frames
        self.left_frames = self.left_small_frames
        '''
        frame_rects = self.player_data
        self.frames.append(tools.get_image(sheet, 178, 32, 12, 16, (0, 0, 0), CONS.magnify2))
        '''
        for group, group_frame_rects in frame_rects.items():
             for frame_rect in group_frame_rects:
                 right_image = tools.get_image(sheet, frame_rect['x'], frame_rect['y'], frame_rect['width'],
                                               frame_rect['height'],  (0, 0, 0), CONS.magnify2)
                 left_image = pygame.transform.flip(right_image, True, False) # 图片的反转
                 if group =='right_small_normal':
                     self.right_small_frames.append(right_image)
                     self.left_small_frames.append(left_image)
                 if group == 'right_big_normal':
                    self.right_big_frames.append(right_image)
                    self.left_big_frames.append(left_image)

        self.frame_index = 0  # 运用了几帧
        self.frames = self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
   # 计算速度
    def calc_v(self, vel, accel, max_vel, face_right=True):
           if face_right:
               return min(vel+accel, max_vel)
           else:
               return max(vel-accel, -max_vel)

    def update(self, keys):
        self.current_time = pygame.time.get_ticks()
        self.handle_states(keys)
   #是否能够跳
    def can_jump_or_not(self,keys):
        if not keys[pygame.K_SPACE]:
            self.can_jump = True
    #游戏信息
    def handle_states(self, keys):
        self.can_jump_or_not(keys)


        if self.state == 'stand':
            self.stand(keys)
        elif self.state == 'walk':
            self.walk(keys)
        elif self.state == 'jump':
            self.jump(keys)
        elif self.state == 'fall':
            self.fall(keys)
        elif self.state == 'die':
            self.die(keys)

        if self.face_right:
            self.image = self.right_frames[self.frame_index]
        else:
            self.image = self.left_frames[self.frame_index]

   # 站立
    def stand(self, keys):
        self.frame_index = 0
        self.x_v = 0
        self.y_v = 0
        if keys[pygame.K_LEFT]:
            self.face_right = False
            self.state = 'walk'
        elif keys[pygame.K_RIGHT]:
            self.face_right = True
            self.state = 'walk'
        elif keys[pygame.K_SPACE] and self.can_jump:
            self.state = 'jump'
            self.y_v = self.jump_v

   # 走路
    def walk(self, keys):
        self.max_x_v = self.max_walk_v
        self.x_a = self.walk_a
        if keys[pygame.K_SPACE]:
            self.state = 'jump'
            self.y_v = self.jump_v

        if self.current_time - self.walking_timer >100:
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 1
            self.walking_timer = self.current_time
        elif keys[pygame.K_RIGHT]:
           self.face_right =True
           if self.x_v < 0:
               self.frame_index = 5
               self.x_a = self.turn_accel
           self.x_v = self.calc_v(self.x_v,self.x_a,self.max_x_v,True)
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            if self.x_v >0:
                self.frame_index = 5
                self.x_a = self.turn_accel
            self.x_v = self.calc_v(self.x_v,self.x_a,self.max_x_v,False)
        else:
            if self.face_right:
                self.x_v -= self.x_a
                if self.x_v < 0:
                    self.x_v = 0
                    self.state = 'stand'
            else:
                self.x_v += self.x_a
                if self.x_v > 0:
                    self.x_v = 0
                    self.state = 'stand'
  # 跳跃
    def jump(self, keys):
        self.frame_index = 4
        self.y_v += self.anti_gravity
        self.can_jump   = False

        if self.y_v >= 0:
            self.state = 'fall'

        if keys[pygame.K_RIGHT]:
            self.x_v = self.calc_v(self.x_v, self.x_a, self.max_x_v, True)
        if keys[pygame.K_LEFT]:
            self.x_v = self.calc_v(self.x_v, self.x_a, self.max_x_v, False)
        if not keys[pygame.K_SPACE]:
            self.state = 'fall'

    # 掉落
    def fall(self, keys):
        self.y_v = self.calc_v(self.y_v, self.gravity, self.max_y_v)


        if keys[pygame.K_RIGHT]:
            self.x_v = self.calc_v(self.x_v, self.x_a, self.max_x_v, True)
        if keys[pygame.K_LEFT]:
            self.x_v = self.calc_v(self.x_v, self.x_a, self.max_x_v, False)


        '''
        if self.face_right:
            self.image = self.right_frames[self.frame_index]
        else:
        elf.image = self.left_frames[self.frame_index]
        '''
    def die(self, keys):
        self.rect.y += self.y_v
        self.y_v += self.anti_gravity

    def dying(self):
       self.dead = True
       self.y_v = self.jump_v
       self.frame_index = 6
       self.state = 'die'
       self.death_timer = self.current_time





