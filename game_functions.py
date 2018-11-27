import sys

import pygame

from time import sleep 

from bullet import Bullet
from alien import Alien

def check_events(screen, ai_settings, ship, bullets, play_button, stats,
                    aliens, sb):
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, screen, ai_settings, ship, bullets)
                
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(play_button, mouse_x, mouse_y, stats, screen,
                ai_settings, aliens, ship, bullets, sb)
            
def check_play_button(play_button, mouse_x, mouse_y, stats, screen,
        ai_settings, aliens, ship, bullets, sb):
            
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        aliens.empty()
        bullets.empty()
        
        ai_settings.initialize_dynamic_settings()
        
        create_fleet(screen, ai_settings, aliens, ship)
        ship.center_ship()
        
        pygame.mouse.set_visible(False)
        
def check_keydown_events(event, screen, ai_settings, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets, ai_settings, screen, ship)
    elif event.key == pygame.K_q:
        sys.exit()
     
def fire_bullet(bullets, ai_settings, screen, ship):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(screen, ai_settings, ship)
        bullets.add(new_bullet)
        
def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
        
def update_screen(ai_settings, screen, ship, bullets, aliens, 
        play_button, stats, sb):
    
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    
    sb.show_score()
    
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def update_bullets(bullets, aliens, screen, ai_settings, ship, stats, sb):
    bullets.update()
    
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            
    check_bullet_alien_collisions(bullets, aliens, screen, ai_settings, ship,
                                    stats, sb)

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_bullet_alien_collisions(bullets, aliens, screen, ai_settings, ship,
                                    stats, sb):            
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
    check_high_score(stats, sb)
    
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increased_speed()
        create_fleet(screen, ai_settings, aliens, ship)
        stats.level += 1
        sb.prep_level()
            
def check_fleet_edges(aliens, ai_settings):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(aliens, ai_settings)
            break
            
def change_fleet_direction(aliens, ai_settings):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(stats, aliens, bullets, screen, ai_settings, ship, sb):
    if stats.ship_left > 0:
        stats.ship_left -= 1
        
        sb.prep_ships()
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        
    aliens.empty()
    bullets.empty()
    
    create_fleet(screen, ai_settings, aliens, ship)
    ship.center_ship()
    
    sleep(0.5)

def check_aliens_bottom(screen, aliens, stats, bullets, ai_settings, ship, sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(stats, aliens, bullets, screen, ai_settings, ship, sb)
            break
            
def update_aliens(aliens, ai_settings, ship, stats, bullets, screen, sb):
    check_fleet_edges(aliens, ai_settings)
    aliens.update()
    
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(stats, aliens, bullets, screen, ai_settings, ship, sb)
    
    check_aliens_bottom(screen, aliens, stats, bullets, ai_settings, ship, sb)
    
    
def get_number_aliens_x(alien_width, ai_settings):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x           
  
def get_number_rows(ai_settings, alien_height, ship_height):
    available_space_y = (ai_settings.screen_height -
                            (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    
def create_alien(screen, ai_settings, alien_number, row_number, aliens):
    alien = Alien(screen, ai_settings)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
def create_fleet(screen, ai_settings, aliens, ship):
    alien = Alien(screen, ai_settings)
    number_aliens_x = get_number_aliens_x(alien.rect.width, ai_settings)
    number_rows = get_number_rows(ai_settings, alien.rect.height, 
        ship.rect.height)
    
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(screen, ai_settings, alien_number, 
                row_number, aliens)


            
            
            
            
            
            
            
            
            
            
            
            
            
