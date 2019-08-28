import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep



def get_number_rows(ai_settings,ship_height,alien_height):
	available_space_y=ai_settings.screen_height-ship_height-3*alien_height
	number_rows=int(available_space_y/(2*alien_height))
	number_rows=3
	return number_rows


def get_aliens_number(ai_settings,alien):
	alien_width=alien.rect.width
	available_space_x=ai_settings.screen_width-2*alien_width
	number_aliens=int(available_space_x/(2*alien_width))
	return number_aliens


def create_alien(ai_settings,screen,alien_number,aliens,row_number):
	'''创建一个外星人并放在当前行'''
	alien=Alien(ai_settings,screen)
	alien_width=alien.rect.width
	alien.x=alien_width+2*alien_width*alien_number
	alien.rect.x=alien.x
	alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
	aliens.add(alien)


def create_fleet(ai_settings,screen,aliens,ship):
	'''创建外星人群'''
	#创建一个外星人，并计算一行可以容纳多少个外星人
	#外星人的间距为外星人的宽度
	alien=Alien(ai_settings,screen)
	number_aliens_x=get_aliens_number(ai_settings,alien)
	number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
	#创建第一行外星人
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,alien_number,aliens,row_number)


def fire_bullet(ai_settings,screen,ship,bullets):
	if len(bullets)<ai_settings.bullets_allowed:
		new_bullet=Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)


def check_keydown(event,ai_settings,screen,ship,bullets):

	#飞船：
	if event.key==pygame.K_RIGHT:
		#向右移动飞船
		ship.moving_right=True

	elif event.key==pygame.K_LEFT:
		#向左移动飞船
		ship.moving_left=True

	elif event.key==pygame.K_UP:
		#向上移动飞船
		ship.moving_up=True

	elif event.key==pygame.K_DOWN:
		#向下移动飞船
		ship.moving_down=True

	elif event.key==pygame.K_q:
		sys.exit()

	
	#子弹：
	elif event.key==pygame.K_SPACE:
		#创建子弹并加入
		fire_bullet(ai_settings,screen,ship,bullets)


def check_keyup(event,ship):
	if event.key==pygame.K_RIGHT:
		ship.moving_right=False

	elif event.key==pygame.K_LEFT:
		ship.moving_left=False

	elif event.key==pygame.K_UP:
		ship.moving_up=False

	elif event.key==pygame.K_DOWN:
		ship.moving_down=False

def check_events(ship, ai_settings, screen, bullets, stats, play_button, aliens):
	'''响应鼠标和按键事件'''
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()

		elif event.type==pygame.KEYDOWN:
			check_keydown(event,ai_settings,screen,ship,bullets)

		elif event.type==pygame.KEYUP:
			check_keyup(event,ship)

		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, stats, play_button, mouse_x, mouse_y, ship, screen, aliens, bullets)

def check_play_button(ai_settings, stats, play_button, mouse_x, mouse_y, ship, screen, aliens, bullets):
	'''在玩家单击play按钮时开始新游戏'''
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		#重置游戏设置
		ai_settings.initialize_dynamic_settings()

		#隐藏光标
		pygame.mouse.set_visible(False)

		#重置游戏统计信息
		stats.reset_stats()
		stats.game_active = True

		#清空外星人和子弹列表
		aliens.empty()
		bullets.empty()

		#创建一群外星人并让飞船居中
		create_fleet(ai_settings,screen,aliens,ship)
		ship.center_ship()

def update_bullets(bullets,aliens,ai_settings,screen,ship, stats, sb):
	#更新子弹位置
	bullets.update()

	#删除已消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom<=0:
			bullets.remove(bullet)

	#碰撞检测,删除被打中的外星人和击中外星人子弹
	check_bullet_alien_collisions(bullets,aliens,ai_settings,screen,ship,stats, sb)

def check_bullet_alien_collisions(bullets,aliens,ai_settings,screen,ship,stats, sb):
	collisions=pygame.sprite.groupcollide(bullets,aliens,False,True)
	if len(aliens)==0:
		'''删除现有子弹，加快游戏节奏，并创建一群新的外星人'''
		#bullets.empty()
		ai_settings.increase_speed()
		create_fleet(ai_settings,screen,aliens,ship)

	if collisions:
		for aliens in collisions.values():
			stats.score+= ai_settings.alien_point*len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)

def change_fleet_direction(ai_settings,aliens):
	'''让整群外星人向下移并改变他们的方向'''
	for alien in aliens.sprites():
		alien.rect.y+=ai_settings.fleet_drop_speed
	ai_settings.fleet_direction*=-1


def check_fleet_edges(ai_settings,aliens):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
	'''响应被撞到的飞船'''
	if stats.ship_left>0:
		#将ship的数量减一
		stats.ship_left-=1

		#清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()

		#创建一群新的外星人，并将飞船放到屏幕低端中央
		create_fleet(ai_settings,screen,aliens,ship)
		ship.center_ship()

		#暂停
		sleep(0.5)

	else:
		stats.game_active=False
		pygame.mouse.set_visible(True)

def check_alien_bottom(ai_settings,stats,screen,ship,aliens,bullets):
	'''检查是否有外星人碰到了屏幕底端'''
	screen_rect=screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#像飞船被撞到了一样处理
			ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
			break

def check_high_score(stats, sb):
	'''检查是否出现了新的最高分'''
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()

def update_aliens(ai_settings,aliens,ship,bullets,screen,stats):
	'''检查是否有外星人位于屏幕边缘，并更新整群外星人位置'''
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,screen,ship,aliens,bullets)

	#检查是否有外星人到达了屏幕底端
	check_alien_bottom(ai_settings,stats,screen,ship,aliens,bullets)

def update_screen(ai_settings,screen,ship,bullets,aliens,play_button,stats, sb):
	'''更新屏幕并切换到新屏幕'''
	#每次循环都重绘屏幕
	screen.fill(ai_settings.bg_color)
	for bullet in bullets.sprites():
		bullet.draw_bullet()

	ship.blitme()
	aliens.draw(screen)
	sb.show_score()

	#如果游戏处于非活动状态，就绘制按钮
	if stats.game_active == False:
		play_button.draw_button()

	#让最近绘制的屏幕可见
	pygame.display.flip()