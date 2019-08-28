class GameStats():
	'''追踪游戏统计信息'''
	def __init__(self,ai_settings):
		self.ai_settings=ai_settings
		self.reset_stats()
		#游戏刚启动时处于活动状态
		self.game_active=False

		#在任何情况下都不重置最高分
		self.high_score = 0

	def reset_stats(self):
		'''初始化在游戏运行期间可能会变化的数据'''
		self.ship_left=self.ai_settings.ship_limit
		self.score = 0