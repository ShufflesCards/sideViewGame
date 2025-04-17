# Benjamin Kellman
# 3/18/25
# 4/14/25
'''
http://programarcadegames.com/python_examples/en/sprite_sheets/
'''
# side view game
# I will finish this then topDownGame


import pygame
import colorDimentions
import levels
import entity

# spikes in a seperate class
# have that offset from a platform
# function update: rect.x rect.y offset from moving platform rect.x rect.y


pygame.init()

                   
screen = pygame.display.set_mode([colorDimentions.screen_width, colorDimentions.screen_height]) 
pygame.display.set_caption('Window Caption') 


player = entity.Player()

# Create all the levels
level_list = []
level_list.append(levels.Level_00(player))
level_list.append(levels.Level_01(player))
level_list.append(levels.Level_02(player))

# Set the current level 
current_level_no = 0
current_level = level_list[current_level_no]

active_sprite_list = pygame.sprite.Group()
player.level = current_level

player.rect.x=240
player.rect.y=colorDimentions.screen_height-player.rect.height
active_sprite_list.add(player)

clock = pygame.time.Clock()
pygame.key.set_repeat(1, 20)







isFirstClick = True
pygame.time.set_timer(pygame.USEREVENT, 1000)
while True: 
    # Figure out if it was an arrow key. If so
    # adjust speed.
    keys = pygame.key.get_pressed()


    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if player.dx >= -player.maxSpeed:
            player.dx-=1
        
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if player.dx <= player.maxSpeed:
            player.dx+=1
        
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.jump()

    # for loop through the event queue   
    for event in pygame.event.get(): 
        
        # Check for QUIT event       
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()
        # if event.type == pygame.USEREVENT: 
        #     print(player)

        
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            pos = pygame.mouse.get_pos()
            mousex = int(pos[0]-current_level.world_shift)
            mousey = int(pos[1])
            if isFirstClick:
                isFirstClick = False
                blockAdd = [mousex, mousey]
            else:
                # adds height
                blockAdd.insert(0, mousey-blockAdd[1])
                blockAdd.insert(0, mousex-blockAdd[1])

                print(blockAdd)
                isFirstClick = True
            

            # block format: width, height, x, y


    # update the player
    active_sprite_list.update()

    # update items in level
    current_level.update()
    
    # If the player gets near the right side, shift the world left (-x)
    if player.rect.right >= colorDimentions.screen_width//1.4:
        diff = player.rect.right - colorDimentions.screen_width//1.4
        player.rect.right = colorDimentions.screen_width//1.4
        current_level.shift_world(-diff)

    # If the player gets near the left side, shift the world right (+x)
    if player.rect.left <= colorDimentions.screen_width//3.5:
        diff = colorDimentions.screen_width//3.5 - player.rect.left
        player.rect.left = colorDimentions.screen_width//3.5
        current_level.shift_world(diff)


    # If we reach the end of the level, go to the next one
    current_positioin = player.rect.x + current_level.world_shift

    if current_positioin < current_level.level_limit:
        player.rect.x = colorDimentions.screen_width//3.5
        if current_level_no < len(level_list)-1:
            current_level_no+=1
            current_level = level_list[current_level_no]
            player.level = current_level
        else:
            print("Game over") # add something better
    







    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
    current_level.draw(screen)
    active_sprite_list.draw(screen)

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Limit to 60 frames per second
    clock.tick(60)
    pygame.display.flip()
