
class mainwindow(pygame.sprite.Sprite):
    def __init__(self):
        countdown=3
        last_count = pygame.time.get_ticks()
        last_Enemy_shot = pygame.time.get_ticks()
        game_over = 0#0 is no game over, 1 means player has won, -1 means player has lost
        #Game Loop
        run=True
        while run:
            clock.tick(fps)
            #background
            draw_bg()
            #bg_fx.play()
            if countdown == 0:
                #create random alien bullets
                #record current time
                time_now = pygame.time.get_ticks()
                #shoot
                if time_now - last_Enemy_shot > Enemy_cooldown and len(Enemy_bullet_group) < 5 and len(Enemy_group) > 0:
                    attacking_Enemy = random.choice(Enemy_group.sprites())
                    Enemy_bullet = Enemy_Bullets(attacking_Enemy.rect.centerx, attacking_Enemy.rect.bottom)
                    Enemy_bullet_group.add(Enemy_bullet)
                    last_Enemy_shot = time_now
                #check if all the aliens have been killed
                if len(Enemy_group) == 0:
                    game_over = 1
                if game_over == 0:
                    #update spaceship
                    game_over = spaceship.update()
                    #update sprite groups
                    bullet_group.update()
                    Enemy_group.update()
                    Enemy_bullet_group.update()
                else:
                    if game_over == -1:
                        draw_text('GAME OVER! ', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
                        #draw restart Icon
                        draw_exibtn()
                        #draw Exit Icon
                        #draw_rsbtn()
                    if game_over == 1:
                        draw_text('YOU WIN!', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
                        #draw restart Icon
                        draw_exibtn()
                        #draw Exit Icon
                        #draw_rsbtn()
            if countdown > 0:
                draw_text('GET READY!', font40, white, int(screen_width / 2 - 110), int(screen_height / 2 + 50))
                draw_text(str(countdown), font40, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
                count_timer = pygame.time.get_ticks()
                if count_timer - last_count > 1000:
                    countdown -= 1
                    last_count = count_timer
            #update explosion group
            explosion_group.update()
            #draw sprite groups
            spaceship_group.draw(screen)
            bullet_group.draw(screen)
            Enemy_group.draw(screen)
            Enemy_bullet_group.draw(screen)
            explosion_group.draw(screen)
            score.show_score(screen)
            #event handlers
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # press r to restart
                        run=False
                        break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # press Q to quit
                        run= False
                        break
            pygame.display.update()
        pygame.quit()
        

if __name__== "__main__":
    app= mainwindow()
    

