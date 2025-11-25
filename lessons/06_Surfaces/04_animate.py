import pygame
from jtlgames.spritesheet import SpriteSheet
from pathlib import Path
import math
import random
import time
import pygame
 
from pygame.math import Vector2

from pathlib import Path
images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"
pygame.init()
images = Path(__file__).parent / 'images' 

class Settings:
    """A class to store all settings for the game."""
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    PLAYER_SIZE = 20
    LINE_COLOR = (255,192,203)
    PLAYER_COLOR = (0, 255, 0)
    
    BACKGROUND_COLOR = (209, 246, 255)
    TEXT_COLOR = (0, 0, 0)
    FPS = 30
    ANGLE_CHANGE = 3
    LENGTH_CHANGE = 5
    INITIAL_LENGTH = 100
    FONT_SIZE = 24
    CROC_SPEED = 1
    score = 0 
    
    number = random.randint(0, 0)
    white = (255, 255, 255)
    font = pygame.font.SysFont("Tahoma", 26)
    death_messages = ["Game Over"]
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
clock = pygame.time.Clock()

def scale_sprites(sprites, scale):
    """Scale a list of sprites by a given factor.

    Args:
        sprites (list): List of pygame.Surface objects.
        scale (int): Scale factor.

    Returns:
        list: List of scaled pygame.Surface objects.
    """
    return [pygame.transform.scale(sprite, (sprite.get_width() * scale, sprite.get_height() * scale)) for sprite in sprites]
class Player:

    def __init__(self, rect, frog_sprites):
        """Initializes the Player with a position and direction vector.

        Args:
            x (int): The initial x-coordinate of the player.
            y (int): The initial y-coordinate of the player.
        """
        self.frog_sprites = frog_sprites
        self.rect = rect
        self.rect.height = rect.height/2
        self.rect.width = rect.width/2
        self.position = pygame.math.Vector2(rect.center)  
        self.direction_vector = pygame.math.Vector2(Settings.INITIAL_LENGTH, 0)  # Initial direction vector
        self.N = 0
        self.step = 0
        self.init_position, self.final_position = 0,0


    def draw(self, frog_index, show_line=True):
        """Draws the player and the direction vector on the screen."""
        x, y = self.rect.center
        #pygame.draw.rect(screen, Settings.PLAYER_COLOR, (self.position.x - Settings.PLAYER_SIZE // 2, self.position.y - Settings.PLAYER_SIZE // 2, Settings.PLAYER_SIZE, Settings.PLAYER_SIZE))
        self.image = pygame.transform.rotate(self.frog_sprites[frog_index], 270-self.direction_vector.as_polar()[1])
        width, height = self.image.get_size()
        x -= width//2
        y -= height//2
        # The end position of the direction vector is the player's position plus the direction vector
        end_position = self.rect.center + self.direction_vector
        
        if self.N > 0:
            self.rect.center += self.step
            #pygame.draw.line(screen, Settings.LINE_COLOR, self.rect.center, self.final_position, 2)
            
            
            self.N -= 1
        

        # elif show_line:
            #pygame.draw.line(screen, Settings.LINE_COLOR, self.rect.center, end_position, 2)
        screen.blit(self.image, (x, y))
    def move(self):
        
        """Moves the player in the direction of the current angle."""
        # while self.N >= 0:
        #     self.position += self.step
        #     screen.fill(Settings.BACKGROUND_COLOR)
        #     pygame.draw.line(screen, Settings.LINE_COLOR, self.rect.center, self.final_position, 2)
        #     self.draw(show_line=False, frog_index= False)
        #     pygame.display.flip()
        #     clock.tick(Settings.FPS)
        #     self.N -=1/6
        if self.N>0:
            return
        self.init_position = self.rect.center # Save the initial position for the animation
        
        # Calculate the final position after moving. It's just addition!
        self.final_position = self.rect.center + self.direction_vector
        
        # The rest is just for animation
        length = self.direction_vector.length()
        self.N = int(length // 3)
        self.step = (self.final_position - self.rect.center) / self.N
        
class Alligator:
    def __init__(self, rect, player):
        self.player = player
        self.rect = rect
        self.rect.width = rect.width*3
        self.rect.height = rect.height/3
        self.movement_speed = Settings.CROC_SPEED
        self.position = pygame.math.Vector2(self.rect.center) 
        self.offset= pygame.math.Vector2(0, -self.rect.height)
    def chase(self):
        # self.init_position = self.position
        
        # self.final_position = self.player.position
        # if self.N>0:
        #     return
        
        self.prey = pygame.math.Vector2(self.player.rect.center)
        # The rest is just for animation
        # if self.prey - self.position < (0,0):
        #     self.length = -self.prey + self.position
        # self.length = self.prey - self.position

        self.length = self.prey - self.position + (3,1)
        self.step = self.length / self.length.magnitude() / 2 
        self.position += self.step
        self.rect.center = self.position
    def draw_alligator(self,alligator, index):
        """Creates a composed image of the alligator sprites.

        Args:
            alligator (list): List of alligator sprites.
            index (int): Index value to determine the right side sprite.

        Returns:
            pygame.Surface: Composed image of the alligator.
        """
        
        index = index % (len(alligator)-2)
        
        #pygame.draw.line(screen, (0,127,255), self.rect.center, self.player.rect.center, 2)
        width = alligator[0].get_width()
        height = alligator[0].get_height()
        composed_image = pygame.Surface((width * 3, height), pygame.SRCALPHA)

        composed_image.blit(alligator[0], (0, 0))
        composed_image.blit(alligator[1], (width, 0))
        composed_image.blit(alligator[(index + 2) % len(alligator)], (width * 2, 0))

        return composed_image
def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Ice-Skating Phorg")

    # Load the sprite sheet
    filename = images / 'spritesheet.png'  # Replace with your actual file path
    cellsize = (16, 16)  # Replace with the size of your sprites
    spritesheet = SpriteSheet(filename, cellsize)


    # Load a strip sprites
    frog_sprites = scale_sprites(spritesheet.load_strip(0, 4, colorkey=-1) , 4)
    allig_sprites = scale_sprites(spritesheet.load_strip( (0,4), 7, colorkey=-1), 4)

    # Compose an image
    log = spritesheet.compose_horiz([24, 25, 26], colorkey=-1)
    log = pygame.transform.scale(log, (log.get_width() * 4, log.get_height() * 4))

    # Variables for animation
    frog_index = 0 
    allig_index = 0
    frames_per_image = 6
    frame_count = 0

    # Main game loop
    running = True
    
    sprite_rect = frog_sprites[0].get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    player = Player(frog_sprites[0].get_rect(center=(screen.get_width() // 2, screen.get_height() // 2)), frog_sprites)
    croc = Alligator(allig_sprites[0].get_rect(center=(screen.get_width() // 1.5, screen.get_height() // 1.5)), player)
    pygame.math.Vector2(1, 0)
    
    key_limit = 0
    while running:
        Alligator.draw_alligator(croc, allig_sprites, allig_index)
        screen.fill(Settings.BACKGROUND_COLOR)  # Clear screen with deep blue

        # Update animation every few frames
        frame_count += 1
        key_limit += 1
        

        
        
        keys = pygame.key.get_pressed()
        
        if key_limit%2 == 0: # Limit frequency of key presses so the user can set exact angles
            if keys[pygame.K_RIGHT]:
                player.direction_vector = player.direction_vector.rotate(-Settings.ANGLE_CHANGE)
            elif keys[pygame.K_LEFT]: 
                player.direction_vector = player.direction_vector.rotate(Settings.ANGLE_CHANGE)
               
        if keys[pygame.K_UP]:
            player.direction_vector.scale_to_length(player.direction_vector.length() + Settings.LENGTH_CHANGE)
        elif keys[pygame.K_DOWN]:
            if player.direction_vector.length() > Settings.LENGTH_CHANGE:
                player.direction_vector.scale_to_length(player.direction_vector.length() - Settings.LENGTH_CHANGE)
            
        elif keys[pygame.K_SPACE] and key_limit%3 == 0:
            player.move()
            
        elif keys[pygame.K_w]:
            player.rect.center += pygame.Vector2(0, -1)
        elif keys[pygame.K_s]:
            player.rect.center += pygame.Vector2(0, 1)
        elif keys[pygame.K_a]:
            player.rect.center += pygame.Vector2(-1, 0)
        elif keys[pygame.K_d]:
            player.rect.center += pygame.Vector2(1, 0)
        if frame_count % frames_per_image == 0: 
            if player.N<=0:
                frog_index = (frog_index + 1) % len(frog_sprites)
            allig_index = (allig_index + 1) % len(allig_sprites)
        
    
        
        # Get the current sprite and display it in the middle of the screen
        
        
        #pygame.draw.rect(screen, Settings.LINE_COLOR, player.rect)
        player.draw(frog_index)
        #pygame.draw.rect(screen, Settings.LINE_COLOR, croc.rect)
        composed_alligator = Alligator.draw_alligator(croc, allig_sprites, allig_index)
        screen.blit(composed_alligator,  croc.rect.move(croc.offset))
        
        #screen.blit(log,  sprite_rect.move(0, -100))

        collider = pygame.sprite.collide_rect(player, croc)
        if collider:
            
            print(Settings.death_messages[Settings.number])
            #print("Score:", Settings.score)
            
            running = False
        # Update the display
        croc.chase()
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Cap the frame rate
        pygame.time.Clock().tick(60)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
