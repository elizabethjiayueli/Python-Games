"""
Example of a scrolling background 

This example creates a background sprite twice the width of the screen so that it can 
be smoothly scrolled and updated from the Sprite groups. 

"""
import pygame
import random
from pathlib import Path

d = Path(__file__).parent # The directory that holds the script

# Initialize Pygame
pygame.init()

class Settings:
    """A class to store all settings for the game."""
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    BACKGROUND_SCROLL_SPEED = 2
    FPS = 50

# Initialize screen
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption("Background Scroll")

# Define background class
class Background(pygame.sprite.Sprite):
    """Represents the scrolling background in the game."""
    def __init__(self):
        super().__init__()
        
        # The Sprite image is 2x as wide as the screen
        self.image = pygame.Surface((Settings.SCREEN_WIDTH * 2, Settings.SCREEN_HEIGHT))
        
        # Load the background image and scale it to the screen size. Note the convert() call. 
        # This converts the form of the image to be more efficient. 
        
        stripes = pygame.Surface((300, screen.get_height()))
        #image = pygame.Surface.fill(original_image, (0,0,255))
        # Tile the background image in the x-direction
        
        red = pygame.draw.rect(stripes, (237,33,0), (0,0, 50, 600))
        orange = pygame.draw.rect(stripes, (255, 139, 0), (50,0, 50, 600))
        yellow = pygame.draw.rect(stripes, (255,239,0), (100,0, 50, 600))
        green = pygame.draw.rect(stripes, (11,218,81), (150,0, 50, 600))
        blue = pygame.draw.rect(stripes, (0,127,255), (200,0, 50, 600))
        purple = pygame.draw.rect(stripes, (148,0,211), (250,0, 50, 600))
        
        
        # Then, copy it into the self.image surface twice
        n = 0
        for x in range(0, self.image.get_width(), stripes.get_width()):
            self.image.blit(stripes, (x, 0))
            n +=1
            print(n)
            
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        """Update the position of the background."""
        
        self.rect.x -= Settings.BACKGROUND_SCROLL_SPEED
        
        if self.rect.right <= Settings.SCREEN_WIDTH:
            self.rect.x = 0
        # elif self.rect.left <= Settings.SCREEN_WIDTH:
        #     self.rect.x = Settings.SCREEN_WIDTH



def main():
    """Run the main game loop."""
    running = True


    bg = Background()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(bg)

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        
        clock.tick(Settings.FPS)

    pygame.quit()





if __name__ == "__main__":
    main()
