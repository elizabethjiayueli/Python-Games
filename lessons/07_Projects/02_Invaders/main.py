import pygame
import random
import time
from pathlib import Path
assets = Path(__file__).parent / 'images'
background = pygame.image.load(assets/'space.png')

# Initialize Pygame
pygame.init()

clock = pygame.time.Clock()



class Settings:
    # Screen
    screen_width = 288
    screen_height = 420
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('SPACE INVADERS')  
    FPS = 30

    projectile_speed = 50    

class Player():
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(assets/'rocket.png')
        self.rect = self.image.get_rect()
    def update(self): 
        keys = pygame.key.get_pressed()
        if keys[pygame.LEFT]:
            
class Alien():
    super().__init__()
    
class Projectile():
    super().__init__()
    
class Game():
    def make_tiled_bg(screen, background):
        # Scale background to match the screen height
        
        bg_tile = pygame.image.load(background).convert()
        
        background_height = Settings.screen.get_height()
        bg_tile = pygame.transform.scale(bg_tile, (bg_tile.get_width(), Settings.screen.get_height()))
        # Get the dimensions of the background after scaling
        background_width = bg_tile.get_width()
        return bg_tile
    
    

    full_background = make_tiled_bg(Settings.screen, assets/'space.png')
    Settings.screen.blit(full_background, (0, 0))
    pygame.display.flip()

     
game = Game()

running = False
run = True
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip() 

        
clock.tick(Settings.FPS)