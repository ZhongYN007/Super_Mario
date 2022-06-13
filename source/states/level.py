from source.components import information
from source import tools, setup
from source import constants as CONS
from source.components import player,stuff,brick,box,emeny
import json,os
import pygame

 # 关卡一
class Level:
    def start(self,game_info):
        self.game_info = game_info
        self.finished = False
        self.next = 'game_over'
        self.info = information.Info('level',self.game_info)
        self.load_map_data()
        self.setup_background()
        self.setup_start_positions()
        self.setup_player()
        self.setup_ground_items()
        self.setup_bricks_boxes()
        self.setup_emenies()
        # 载入图片
    def load_map_data(self):
        file_name = 'level_1.json'
        file_path = os.path.join('source/data/maps', file_name)
        with open(file_path)as f:
            self.map_data = json.load(f)
       #载入背景
    def setup_background(self):
        self.image_name = self.map_data['image_name']
        self.background = setup.GRAPHIC[self.image_name]
        #self.background = setup.GRAPHIC['level_1']
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width*CONS.magnify1),
                                                                   int(rect.height*CONS.magnify1)))
        self.background_rect = self.background.get_rect()
        self.game_window  = setup.SCREEN.get_rect()
        self.game_ground = pygame.Surface((self.background_rect.width,self.background_rect.height))
     #马里奥的初始位置
    def setup_start_positions(self):
        self.positions = []
        for data in self.map_data['maps']:
            self.positions.append((data['start_x'], data['end_x'], data['player_x'], data['player_y']))
            self.start_x, self.end_x, self.player_x, self.player_y = self.positions[0]

     # 载入玩家对象
    def setup_player(self):
       self.player = player.Player('mario')
       self.player.rect.x = self.game_window.x + self.player_x
       self.player.rect.bottom = self.player_y
     # 载入碰撞数据
    def setup_ground_items(self):
       self.ground_items_group = pygame.sprite.Group() # 存放多个精灵
       for name in ['ground', 'pipe', 'step']:
            for item in self.map_data[name]:
                self.ground_items_group.add(stuff.Item(item['x'], item['y'], item['width'], item['height'], name))
                # print(item['x'])
   # 载入箱子，盒子
    def setup_bricks_boxes(self):

        self.brick_group = pygame.sprite.Group()
        self.box_group = pygame.sprite.Group()
        if 'brick' in self.map_data:
            for data in self.map_data['brick']:
                x, y = data['x'], data['y']
                brick_type = data['type']
                if 'brick_num' in data:
                   pass
                else:
                    self.brick_group.add(brick.Brick(x, y, brick_type))
        if 'box' in self.map_data:
            for data in self.map_data['box']:
                x, y = data['x'], data['y']
                box_type = data['type']
                self.box_group.add(box.Box(x, y, box_type))
    #载入敌人
    def setup_emenies(self):
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group_dict = {}
        for enemy_group_data in self.map_data['enemy']:
            group = pygame.sprite.Group()
            for enemy_group_id,enemy_list in enemy_group_data.items():
                for enemy_data in enemy_list:
                   group.add(emeny.create_enemy(enemy_data))
                   self.enemy_group.add(emeny.create_enemy(enemy_data))

                self.enemy_group_dict[enemy_group_id] = group
   # 更新
    def update(self, surface, keys):
        self.current_time = pygame.time.get_ticks()
        self.player.update(keys)

        if self.player.dead:
            if self.current_time - self.player.death_timer > 3000:
                self.finished = True
                self.update_game_info()
        else:

          self.update_player_position()
          self.check_if_die()
          self.update_game_window()
          self.info.update()
          self.brick_group.update()
          self.box_group.update()
        self.draw(surface)
   # 速度
    def adjust_player_x(self, sprite):
        if self.player.rect.x < sprite.rect.x:
            self.player.rect.right = sprite.rect.left
        else:
            self.player.rect.left = sprite.rect.right
        self.player.x_v = 0
   # x方向碰撞
    def check_x_collisions(self):
        check_group = pygame.sprite.Group(self.ground_items_group,self.brick_group,self.box_group)
        collided_sprite = pygame.sprite.spritecollideany(self.player, check_group)
        if collided_sprite:
            self.adjust_player_x(collided_sprite)
        enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)
        if enemy:
            self.player.dying()

  # y方向
    def adjust_player_y(self, sprite):
        if self.player.rect.bottom < sprite.rect.bottom:
            self.player.y_v = 0
            self.player.rect.bottom = sprite.rect.top
            self.player.state = 'walk'
        else:
            self.player.y_v = 7
            self.player.rect.top = sprite.rect.bottom
            self.player.state = 'fall'

    def check_y_collisions(self):
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group, self.box_group)
        collided_sprite = pygame.sprite.spritecollideany(self.player, check_group)
        # print(ground_item)
        if collided_sprite:
            self.adjust_player_y(collided_sprite )
        enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)
        if enemy:
            self.player.dying()
        self.check_will_fail(self.player)
  # 边界判断
    def update_player_position(self):
        self.player.rect.x += self.player.x_v
        if self.player.rect.x < self.start_x:
            self.player.rect.x = self.start_x
        elif self.player.rect.right > self.end_x:
            self.player.rect.right = self.end_x
        self.check_x_collisions()

        self.player.rect.y += self.player.y_v
        self.check_y_collisions()

    # 这里很重要，检查是否掉落
    def check_will_fail(self, sprite):
        sprite.rect.y += 1
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group, self.box_group)
        collided = pygame.sprite.spritecollideany(sprite,check_group)
        if not collided and sprite.state != 'jump':
            sprite.state = 'fall'
        sprite.rect.y -= 1


    def update_game_window(self):
        third = self.game_window.x + self.game_window.width / 3
        if self.player.x_v > 0 and self.player.rect.centerx > third and self.game_window.right < self.end_x:
            self.game_window.x += self.player.x_v
            self.start_x = self.game_window.x
     #载入画布
    def draw(self, surface):
        self.game_ground.blit(self.background,  self.game_window, self.game_window)
        self.game_ground.blit(self.player.image, self.player.rect)
        self.brick_group.draw(self.game_ground)
        self.box_group.draw(self.game_ground)
        for enemy in self.enemy_group_dict.values():
            enemy.draw(self.game_ground)
        surface.blit(self.game_ground, (0, 0), self.game_window)
        self.info.draw(surface)

   # 检查是否死亡
    def check_if_die(self):
        if self.player.rect.y > CONS.HEIGHT:
            self.player.dying()

   # 游戏生命信息
    def update_game_info(self):
        if self.player.dead:
            self. game_info['lives'] -= 1
        if self.game_info['lives'] == 0:
            self.next = 'game_over'
        else:
            self.next = 'load_screen'

