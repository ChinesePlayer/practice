from ship import Ship
from settings import Settings
import pygame
import sys
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
	pygame.init()
	ai_settings=Settings()
	screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")

	#创建play按钮
	play_button = Button(ai_settings, screen, 'Play')

	#储存游戏信息
	stats=GameStats(ai_settings)

	#创建记分牌
	sb = Scoreboard(ai_settings, screen, stats)
	
	#创建飞船
	ship=Ship(ai_settings,screen)

	#创建外星人群
	aliens=Group()
	gf.create_fleet(ai_settings,screen,aliens,ship)

	#创建子弹
	bullets=Group()

	#开始主循环
	while True:
		gf.check_events(ship, ai_settings, screen, bullets, stats, play_button, aliens)
		if stats.game_active:
			ship.update()
			gf.update_bullets(bullets,aliens,ai_settings,screen,ship, stats, sb)
			gf.update_aliens(ai_settings,aliens,ship,bullets,screen,stats)

		gf.update_screen(ai_settings,screen,ship,bullets,aliens,play_button,stats, sb)

run_game()
