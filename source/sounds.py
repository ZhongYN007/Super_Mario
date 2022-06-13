import pygame							# 导入pygame资源包
file=r'resources/music/main_theme.ogg'		# 音乐的路径
pygame.mixer.init()						# 初始化
track = pygame.mixer.music.load(file)	# 加载音乐文件
pygame.mixer.music.play()
