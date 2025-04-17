"""
Module for managing platforms.
"""
import pygame
 
from spritesheet_functions import SpriteSheet
 
# These constants define our platform types:
#   Name of file
#   X location of sprite
#   Y location of sprite
#   Width of sprite
#   Height of sprite
 
GRASS_LEFT            = (576, 720, 70, 70)
GRASS_RIGHT           = (576, 576, 70, 70)
GRASS_MIDDLE          = (504, 576, 70, 70)
STONE_PLATFORM_LEFT   = (432, 720, 70, 40)
STONE_PLATFORM_MIDDLE = (648, 648, 70, 40)
STONE_PLATFORM_RIGHT  = (792, 648, 70, 40)
 
class Platform(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_data):
            """ Platform constructor. Assumes constructed with user passing in
                an array of 5 numbers like what's defined at the top of this
                code. """  # we get parameter of width and height, and the code will set rect.x and rect.y, and player to the platform
            super().__init__()
    
            sprite_sheet = SpriteSheet("tiles_spritesheet.png")
            # Grab the image for this platform
            self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                                sprite_sheet_data[1],
                                                sprite_sheet_data[2],
                                                sprite_sheet_data[3])
    
            self.rect = self.image.get_rect()
 
 
class MovingPlatform(Platform):

    def __init__(self, sprite_sheet_data):
        super().__init__(sprite_sheet_data)
        self.dx = 0
        self.dy = 0

        self.boundary_top = 0
        self.boundary_bottom = 0
        self.boundary_left = 0
        self.boundary_right = 0

        self.player = None
        self.level = None

    def update(self):
        """ Move the platform.
            If the player is in the way, it will shove the player
            out of the way. This does NOT handle what happens if a
            platform shoves a player into another object. Make sure
            moving platforms have clearance to push the player around
            or add code to handle what happens if they don't. """


        # left right 
        self.rect.x+=self.dx

        # check collision with player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.dx<0:
                # platform moving left
                self.player.rect.right = self.rect.left
            else:
                self.player.rect.left = self.rect.right
        
        # up down
        self.rect.y+=self.dy

        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # we hit the player and are assuming we will not move the player into anything
            if self.dy<0:
                # moving up
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom
        
        # Check the boundaries and see if we need to reverse direction
        if (not self.dy == 0) and (self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top):
            self.dy *= -1
 
        cur_pos = self.rect.x - self.level.world_shift
        if (not self.dx == 0) and (cur_pos < self.boundary_left or cur_pos > self.boundary_right):
            self.dx *= -1