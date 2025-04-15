"""
Example of loading a background image that is not as wide as the screen, and
tiling it to fill the screen.

"""
import pygame

# Initialize Pygame
pygame.init()

from pathlib import Path
assets = Path(__file__).parent / 'images'

# Set up display
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tiled Background')

def make_tiled_bg(screen, bg_file):
    # Scale background to match the screen height
    
    bg_tile = pygame.image.load(bg_file).convert()
    
    background_height = screen.get_height()
    bg_tile = pygame.transform.scale(bg_tile, (bg_tile.get_width(), screen.get_height()))

    # Get the dimensions of the background after scaling
    background_width = bg_tile.get_width()

    # Make an image the is the same size as the screen
    image = pygame.Surface((screen.get_width(), screen.get_height()))
    stripes = pygame.Surface((300, screen.get_height()))
    
    #image = pygame.Surface.fill(original_image, (0,0,255))
    # Tile the background image in the x-direction
    
    red = pygame.draw.rect(stripes, (237,33,0), (0,0, 50, 600))
    orange = pygame.draw.rect(stripes, (255, 139, 0), (50,0, 50, 600))
    yellow = pygame.draw.rect(stripes, (255,239,0), (100,0, 50, 600))
    green = pygame.draw.rect(stripes, (11,218,81), (150,0, 50, 600))
    blue = pygame.draw.rect(stripes, (0,127,255), (200,0, 50, 600))
    purple = pygame.draw.rect(stripes, (148,0,211), (250,0, 50, 600))
    # # colors = [red, orange, yellow, green, blue, purple]
    n = 0
    for x in range(0, screen.get_width(), stripes.get_width()):
        image.blit(stripes, (x, 0))
        n +=1
        print(n)
        
        
    
    return image

background = make_tiled_bg(screen, assets/'background_tile.gif')

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background,(0,0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
