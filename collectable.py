import pygame
import colorDimentions
from spritesheet_functions import SpriteSheet


COLIMG            = (0, 0, 70, 70)
class Collectable(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_data):
        super().__init__()
        sprite_sheet = SpriteSheet("tiles_spritesheet.png")
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                                sprite_sheet_data[1],
                                                sprite_sheet_data[2],
                                                sprite_sheet_data[3])

        self.rect = self.image.get_rect()
        self.dx=0
        self.dy=0
    
    def update(self):
        self.rect.y+=self.dy
        self.rect.x+=self.dx