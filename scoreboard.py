import pygame

class Scoreboard():
	def __init__(self, ai_settings, screen, stats):
		'''初始化显示得分涉及的属性'''
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats

		#字体设置
		self.text_color = (0, 0, 0)
		self.font = pygame.font.SysFont(None, 48)

		#准备初始得分图像
		self.prep_score()

		#不重置最高分
		self.prep_high_score()

	def prep_score(self):
		'''将分数转化为图像'''
		rounded_score = int(round(self.stats.score, -1))
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color)
		self.score_image_rect = self.score_image.get_rect()

		#将得分放在右上角
		self.score_image_rect.right = self.screen_rect.right - 20
		self.score_image_rect.top = 20

	def prep_high_score(self):
		'''将最高得分转化为图像'''
		high_score = int(round(self.stats.high_score, -1))
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True, self.text_color)
		self.high_score_rect = self.high_score_image.get_rect()

		#将其放在屏幕右上角
		self.high_score_rect.top = 0
		self.high_score_rect.centerx = self.screen_rect.centerx

	def show_score(self):
		'''显示得分'''
		self.screen.blit(self.score_image, self.score_image_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)