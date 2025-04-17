import pygame
import colorDimentions
from platforms import MovingPlatform
from spritesheet_functions import SpriteSheet
import collectable

class Entity(pygame.sprite.Sprite):
    def __init__ (self): 
        super().__init__() # Box is a child class calling its parent pygame.sprite.Sprite

        self.dx = 0
        self.dy = 0
        # x pos, y pos, x velocity, y velocity

        # This holds all the images for the animated walk left/right
        # of our player
        self.walking_frames_l = []
        self.walking_frames_r = []

        # What direction is the player facing?
        self.direction = "R"

        # list of sprites we can collide with
        self.level = None

        # make a new sprite sheet for enemies 
        sprite_sheet = SpriteSheet("p1_walk.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(0, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        self.walking_frames_r.append(image)
 
        # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(0, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
 
        # Set the image the player starts with
        self.image = self.walking_frames_r[0]
 
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        

    def __str__(self):
        return f"({self.rect.x}, {self.rect.y})   <{self.dx}, {self.dy}>"
    
    def horzBlock(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.dx>0:
                # when moving right and hitting something. our right side hits the left side of the barrier
                self.rect.right = block.rect.left
            elif self.dx<0:
                self.rect.left = block.rect.right
            
            self.dx = -self.dx

    def vertBlock(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            if self.dy>0:
                # going down
                self.rect.bottom = block.rect.top
            elif self.dy<0:
                self.rect.top = block.rect.bottom
            
            # stop moving down because we hit a block 
            self.dy=0

            if isinstance(block, MovingPlatform):
                # checks if what we hit is a moving platform
                self.rect.x+=block.dx

    def vertEnemy(self): # need something to bounce off the player
        enemys_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        for enemy in enemys_hit_list:
            if enemy != self:
                if self.dy>0:
                    self.rect.bottom = enemy.rect.top
                elif self.dy<0:
                    self.rect.top = enemy.rect.bottom
                
                self.dy = 0
    
    def horzEnemy(self):
        enemys_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        for enemy in enemys_hit_list:
            if enemy != self:
                if self.dx>0:
                    # when moving right and hitting something. our right side hits the left side of the enemy
                    #self.rect.right = enemy.rect.left
                    self.dx = -self.dx
                elif self.dx<0:
                    #self.rect.left = enemy.rect.right
                    self.dx = -self.dx

    def horzPlayer(self):
        hit = pygame.sprite.collide_rect(self, self.level.player)
        if hit:
            if ((self.dx >=0 and self.level.player.dx>=0) or (self.dx <=0 and self.level.player.dx<=0)):
                self.dx = -self.dx
                
    def update(self):

        # gravity
        self.calc_grav()

        # move left and right
        self.rect.x+=self.dx
        # animation
        pos = int(self.rect.x + self.level.world_shift)
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

        # check collision
        self.horzBlock()

        # move up and down
        self.rect.y+=self.dy

        self.vertBlock()
        
        self.vertEnemy()

        self.horzEnemy()

        self.horzPlayer()

        if self.dx<0:
            self.direction = "L"
        elif self.dx>0:
            self.direction = "R"

    def calc_grav(self):
        
        # checking if we are on the Moon for low gravity
        if self.level.level_type == "Moon":
            if self.dy == 0:
                self.dy = 0.5
            else:
                self.dy+=0.2
        else:
            if self.dy==0:
                self.dy=1
            else:
                self.dy+=0.5

        # check if we are grounded
        if self.rect.y >= colorDimentions.screen_height - self.rect.height and self.dy>=0:
            self.dy=0
            self.rect.y = colorDimentions.screen_height - self.rect.height
    
    def die(self):
        self.kill()



class Player(Entity):
    hp = 10
    maxSpeed = 8
    score = 0
    def update(self):
        super().calc_grav()
        self.calc_friction()
        self.rect.x+=self.dx
        # animation
        pos = int(self.rect.x + self.level.world_shift)

        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]
        self.horzBlock() 
        self.rect.y+=self.dy
        super().vertBlock()
        
        self.collect()
        self.vertEnemy()
        self.horzEnemy()


        if self.dx<0:
            self.direction = "L"
        elif self.dx>0:
            self.direction = "R"

    def __str__(self):
        return f"({self.rect.x}, {self.rect.y})   <{self.dx}, {self.dy}>, HP: {self.hp}"
        
    def collect(self):
        collectable_hit_list = pygame.sprite.spritecollide(self, self.level.collectable_list, True)
        for item in collectable_hit_list:
            self.score += 1
            print(self.score)

    def vertEnemy(self):
        enemys_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        for enemy in enemys_hit_list:
            if enemy != self:
                if self.dy>0:
                    enemy.kill()
                    self.dy = -self.dy

    def horzEnemy(self):
        enemys_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        for enemy in enemys_hit_list:
            if enemy != self:
                if self.dx>0:
                    # when moving right and hitting something. our right side hits the left side of the enemy
                    #self.rect.right = enemy.rect.left
                    self.dx = -self.dx * 1.1 - 5
                elif self.dx<0:
                    #self.rect.left = enemy.rect.right
                    self.dx = -self.dx * 1.1 + 5
                self.hp-=1
                # TODO make the sprite change when hit
                print(self.hp)

    def horzBlock(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.dx>0:
                # when moving right and hitting something. our right side hits the left side of the barrier
                self.rect.right = block.rect.left
            elif self.dx<0:
                self.rect.left = block.rect.right
            
            self.dx = 0


    def jump(self):
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list)>0 or self.rect.bottom >= colorDimentions.screen_height:
            self.dy = -11

    def calc_friction(self):
        if self.level.level_type == "Ice":
            #print("ice")
            pass
        else:
            if self.dx<0.5 and self.dx > -0.5:
                self.dx = 0
            elif self.dx>=0.5:
                self.dx/=1.1
            elif self.dx<=-0.5:
                self.dx/=1.1