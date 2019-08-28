import pygame

class Ship():
	def __init__(self,ai_settings,screen):
		'''初始化飞船并设置其初始位置'''
		self.screen=screen
		self.ai_settings=ai_settings

		#加载飞船图像并获取其外接矩形
		self.image=pygame.image.load(r'images\ship.bmp')
		self.rect=self.image.get_rect()
		self.screen_rect=screen.get_rect()

		#将每艘飞船都放在屏幕的正下方
		self.rect.centerx=self.screen_rect.centerx
		self.rect.bottom=self.screen_rect.bottom

		#在飞船的属性center中储存小数值
		self.center={'x':float(self.rect.centerx) ,'y':float(self.rect.centery)}

		#移动标志
		self.moving_right=False
		self.moving_left=False
		self.moving_up=False
		self.moving_down=False

	def blitme(self):
		self.screen.blit(self.image,self.rect)

	def update(self):
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center['x']+=self.ai_settings.ship_speed_factor

		if self.moving_left and self.rect.left > self.screen_rect.left:
			self.center['x']-=self.ai_settings.ship_speed_factor

		if self.moving_up and self.rect.top > self.screen_rect.top:
			self.center['y']-=self.ai_settings.ship_speed_factor

		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.center['y']+=self.ai_settings.ship_speed_factor

		#同步坐标
		self.rect.centerx=self.center['x']
		self.rect.centery=self.center['y']

	def center_ship(self):
		'''让飞船在屏幕中间的下面'''
		self.center['y']=float(self.screen_rect.bottom)-float(self.rect.height/2)
		self.center['x']=self.screen_rect.centerx