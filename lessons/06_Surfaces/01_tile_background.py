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
    # image = pygame.Surface.fill(original_image, (0,0,255))
    # Tile the background image in the x-direction
    
    red = pygame.draw.rect(image, (237,33,0), (0,0, 100, 600))
    orange = pygame.draw.rect(image, (255, 139, 0), (100,0, 100, 600))
    yellow = pygame.draw.rect(image, (255,239,0), (200,0, 100, 600))
    green = pygame.draw.rect(image, (11,218,81), (300,0, 100, 600))
    blue = pygame.draw.rect(image, (0,127,255), (400,0, 100, 600))
    purple = pygame.draw.rect(image, (148,0,211), (500,0, 100, 600))
    # colors = [red, orange, yellow, green, blue, purple]
    # counter = 0
    # for x in range(0, screen.get_width(), background_width):
    #     image.blit(red, (2*x, 0))
    #     image.blit(orange, (2*x, 0))
        # counter +=1
        # if counter == 5:
        #     break
        
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
