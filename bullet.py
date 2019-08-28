import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	'''管理发射的子弹'''

	def __init__(self,ai_settings,screen,ship):
		super().__init__()#等价于：super(Bullet,self).__init__()

		self.screen=screen

		#在(0,0)创建子弹，再移到正确位置
		self.rect=pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
		self.rect.centerx=ship.rect.centerx
		self.rect.top=ship.rect.top

		#用小数表示子弹的位置
		self.y=float(self.rect.y)

		self.color=ai_settings.bullet_color
		self.speed_factor=ai_settings.bullet_speed_factor

	def update(self):
		'''向上移动子弹'''
		self.y-=self.speed_factor
		#同步坐标
		self.rect.y=self.y

	def draw_bullet(self):
		pygame.draw.rect(self.screen,self.color,self.rect)