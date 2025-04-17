import pygame
 
import colorDimentions
import platforms
import collectable
import entity

class Level(object):
    """ This is a generic super-class used to define a level.
    Create a child class for each level with level-specific
    info. """
    # big parent to all levels made

    # heat level idea: blocks move fast


    def __init__(self, player):
        # list of sprites for levels
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.collectable_list = pygame.sprite.Group()
        self.player = player

        # background image
        self.background = None
        # level size is 1100-level_limit

        # how far the world has shifted left and right
        self.world_shift = 0
        self.level_limit = -1000

        # adding level types to change things like friction and jump height for later
        self.level_type_list = ["Normal", "Ice", "Moon"]
        self.level_type = None

    def update(self):
        # update everything in this level
        self.platform_list.update()
        self.enemy_list.update()
        self.collectable_list.update()
    
    def draw(self, screen):

        # Draw the background
        # We don't shift the background as much as the sprites are shifted
        # to give a feeling of depth.
        screen.fill(colorDimentions.BLUE)
        screen.blit(self.background,(self.world_shift // 3, 0))
        screen.blit(self.background,(self.world_shift // 3-self.background.get_width(), 0))
        screen.blit(self.background,(self.world_shift // 3+self.background.get_width(), 0))
        # when > 0, the background image does not fit the screen
        # TODO add screen rap
        # print(self.background.get_width())

        #draw all sprite lists part of the level (not player or stuff not just on this level)
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.collectable_list.draw(screen)
    
    def shift_world(self, shift_x):
        # moving left and right moves the world

        self.world_shift += shift_x

        # go though all the sprite groups and shift them
        for platform in self.platform_list:
            platform.rect.x += shift_x
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
        for collectable in self.collectable_list:
            collectable.rect.x += shift_x

class Level_00(Level):
    """ Testing. """

    def __init__(self, player):
        """ Create level 0. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("background_02.png").convert()
        self.background.set_colorkey(colorDimentions.WHITE)
        self.level_limit = -1000
        self.level_type = self.level_type_list[0]
        


        # level is 800x600
        # player starts at x=240
        # Array with image, x, and y of platform

        level = [ 
                  [platforms.GRASS_MIDDLE, 2100, 0], # level limit
                  ]


        # img, x, y
        collectables = [[collectable.COLIMG,600,400]]
        

        # Array with image, x, y, left boundry, right boundry, top boundry, bottom boundry, dx, dy
        # if not moving vertically, set dy to 0
        # if not moving horizontally, set dx to 0
        # bounds will not matter
        movingplatforms = [[platforms.STONE_PLATFORM_MIDDLE, 200, 300, 200, 500, None, None, 1, 0]]
        
        enemys = [[0, 100, 1], [150, 100, -1], [500, 100, 0]]
        
        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)
        
        
        for moving in movingplatforms:
            block = platforms.MovingPlatform(moving[0])
            block.rect.x = moving[1]
            block.rect.y = moving[2]
            block.boundary_left = moving[3]
            block.boundary_right = moving[4]
            block.boundary_top = moving[5]
            block.boundary_bottom = moving[6]
            block.dx = moving[7]
            block.dy = moving[8]
            block.player = self.player
            block.level = self
            self.platform_list.add(block)
        

        for item in collectables:
            obj = collectable.Collectable(item[0])
            obj.rect.x = item[1]
            obj.rect.y = item[2]
            self.collectable_list.add(obj)
        
        '''
        for enemy in enemys:
            dude = entity.Entity()
            dude.rect.x = enemy[0]
            dude.rect.y = enemy[1]
            dude.dx =enemy[2]
            dude.level = self
            self.enemy_list.add(dude)

        '''


class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("background_01.png").convert()
        self.background.set_colorkey(colorDimentions.WHITE)
        self.level_limit = -2500
        self.level_type = self.level_type_list[0]


        # level is 800x600
        # player starts at x=240
        # Array with image, x, and y of platform
        level = [ [platforms.GRASS_LEFT, 500, 500],
                  [platforms.GRASS_MIDDLE, 570, 500],
                  [platforms.GRASS_RIGHT, 640, 500],
                  [platforms.GRASS_LEFT, 800, 400],
                  [platforms.GRASS_MIDDLE, 870, 400],
                  [platforms.GRASS_RIGHT, 940, 400],
                  [platforms.GRASS_LEFT, 1000, 500],
                  [platforms.GRASS_MIDDLE, 1070, 500],
                  [platforms.GRASS_RIGHT, 1140, 500],
                  [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                  [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                  [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
                  [platforms.GRASS_MIDDLE, 3600, 0], # level limit
                  ]


        # img, x, y
        collectables = [[collectable.COLIMG,0,0]]
        

        # Array with image, x, y, left boundry, right boundry, top boundry, bottom boundry, dx, dy
        # if not moving vertically, set dy to 0
        # if not moving horizontally, set dx to 0
        # bounds will not matter
        movingplatforms = [[platforms.STONE_PLATFORM_MIDDLE, 200, 300, 200, 500, None, None, 1, 0]]
        
        enemys = [[0, 100, 1], [150, 100, -1], [500, 100, 0]]

        # Go through the array above and add platforms
        
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)
        
        
        for moving in movingplatforms:
            block = platforms.MovingPlatform(moving[0])
            block.rect.x = moving[1]
            block.rect.y = moving[2]
            block.boundary_left = moving[3]
            block.boundary_right = moving[4]
            block.boundary_top = moving[5]
            block.boundary_bottom = moving[6]
            block.dx = moving[7]
            block.dy = moving[8]
            block.player = self.player
            block.level = self
            self.platform_list.add(block)
        

        for item in collectables:
            obj = collectable.Collectable(item[0])
            obj.rect.x = item[1]
            obj.rect.y = item[2]
            self.collectable_list.add(obj)
        
        for enemy in enemys:
            dude = entity.Entity()
            dude.rect.x = enemy[0]
            dude.rect.y = enemy[1]
            dude.dx =enemy[2]
            dude.level = self
            self.enemy_list.add(dude)

class Level_02(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("background_02.png").convert()
        self.background.set_colorkey(colorDimentions.WHITE)
        self.level_limit = -1000
        self.level_type = self.level_type_list[1]


        # level is 800x600
        # player starts at x=240
        # Array with image, x, and y of platform
        level = [ [platforms.GRASS_LEFT, 500, 500],
                  [platforms.GRASS_MIDDLE, 570, 500],
                  [platforms.GRASS_RIGHT, 640, 500],
                  [platforms.GRASS_LEFT, 800, 400],
                  [platforms.GRASS_MIDDLE, 870, 400],
                  [platforms.GRASS_RIGHT, 940, 400],
                  [platforms.GRASS_LEFT, 1000, 500],
                  [platforms.GRASS_MIDDLE, 1070, 500],
                  [platforms.GRASS_RIGHT, 1140, 500],
                  [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                  [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                  [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
                  [platforms.GRASS_MIDDLE, 2100, 0], # level limit
                  ]


        # img, x, y
        collectables = [[collectable.COLIMG,0,0]]
        

        # Array with image, x, y, left boundry, right boundry, top boundry, bottom boundry, dx, dy
        # if not moving vertically, set dy to 0
        # if not moving horizontally, set dx to 0
        # bounds will not matter
        movingplatforms = [[platforms.STONE_PLATFORM_MIDDLE, 200, 300, 200, 500, None, None, 1, 0]]
        
        enemys = [[0, 100, 1], [150, 100, -1], [500, 100, 0]]

        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)
        
        
        for moving in movingplatforms:
            block = platforms.MovingPlatform(moving[0])
            block.rect.x = moving[1]
            block.rect.y = moving[2]
            block.boundary_left = moving[3]
            block.boundary_right = moving[4]
            block.boundary_top = moving[5]
            block.boundary_bottom = moving[6]
            block.dx = moving[7]
            block.dy = moving[8]
            block.player = self.player
            block.level = self
            self.platform_list.add(block)
        

        for item in collectables:
            obj = collectable.Collectable(item[0])
            obj.rect.x = item[1]
            obj.rect.y = item[2]
            self.collectable_list.add(obj)
        
        for enemy in enemys:
            dude = entity.Entity()
            dude.rect.x = enemy[0]
            dude.rect.y = enemy[1]
            dude.dx =enemy[2]
            dude.level = self
            self.enemy_list.add(dude)