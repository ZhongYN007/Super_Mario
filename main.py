from source import tools, setup
import pygame
from source.states import main_menu,load_screen,level


def main():
    # 游戏的每个阶段
    dic = {
        'main_menu': main_menu.MainMenu(),
        'load_screen': load_screen.LoadScreen(),
        'level': level.Level(),
        'game_over': load_screen.Gameover()
    }
    game = tools.Game(dic, 'main_menu')
    game.run()


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
   main()

