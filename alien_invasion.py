# -*- coding:utf-8 -*-

import sys

import pygame

from setting import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf
from pygame.sprite import Group

def run_game():
    #初始化
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    play_button = Button(ai_settings, screen, "Play")
    
    stats = GameStats(ai_settings)
    
    sb = Scoreboard(screen, ai_settings, stats)
    
    ship = Ship(ai_settings, screen)
    
    bullets = Group()
    
    aliens = Group()
    
    gf.create_fleet(screen, ai_settings, aliens, ship)
    #主循环
    while True:
        
        #监视事件
        gf.check_events(screen, ai_settings, ship, bullets, play_button, stats,
            aliens, sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, aliens, screen, ai_settings, ship,
                                stats, sb)
            gf.update_aliens(aliens, ai_settings, ship, stats, bullets, 
                screen, sb)
        #更新屏幕
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, 
            play_button, stats, sb)
        
            
        
run_game()
