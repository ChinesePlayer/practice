class Settings():
	'''本项目的所有设置'''
	def __init__(self):
		'''初始化游戏设置'''

		#屏幕设置
		self.screen_width=1200
		self.screen_height=750
		self.bg_color=(230,230,230)

		#飞船的设置
		self.ship_limit=4#最大飞船数量

		#子弹设置
		self.bullet_width=3
		self.bullet_height=15
		self.bullet_color=(194,22,234)
		self.bullets_allowed=4

		#外星人设置
		self.fleet_drop_speed=10

		#加快游戏节奏
		self.speedup_scale = 1.01
		self.pointup_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		'''初始化随游戏变化的属性'''
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 1
		self.alien_speed_factor = 1

		#1表示向右移动，-1表示向左移动
		self.fleet_direction=1

		#外星人点数
		self.alien_point = 10

	def increase_speed(self):
		'''提高速度设置'''
		self.ship_speed_factor*=self.speedup_scale
		self.bullet_speed_factor*=self.speedup_scale
		self.alien_speed_factor*=self.speedup_scale

		#提高外星人点数
		self.alien_point = int(self.alien_point*self.pointup_scale)