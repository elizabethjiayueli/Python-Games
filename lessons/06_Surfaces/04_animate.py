import pygame
from jtlgames.spritesheet import SpriteSheet
from pathlib import Path
import math

images = Path(__file__).parent / 'images'

class Settings:
    """A class to store all settings for the game."""
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    PLAYER_SIZE = 20
    LINE_COLOR = (0, 255, 0)
    
    BACKGROUND_COLOR = (255, 255, 255)
    TEXT_COLOR = (0, 0, 0)
    FPS = 30
    ANGLE_CHANGE = 3
    LENGTH_CHANGE = 5
    INITIAL_LENGTH = 100
    FONT_SIZE = 24
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
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
    def __init__(self, x, y):
        """Initializes the Player with a position and direction vector.

        Args:
            x (int): The initial x-coordinate of the player.
            y (int): The initial y-coordinate of the player.
        """
        self.position = pygame.math.Vector2(x, y)
        self.direction_vector = pygame.math.Vector2(Settings.INITIAL_LENGTH, 0)  # Initial direction vector

    def draw(self, show_line=True):
        """Draws the player and the direction vector on the screen."""
        pygame.draw.rect(screen, Settings.PLAYER_COLOR, (self.position.x - Settings.PLAYER_SIZE // 2, self.position.y - Settings.PLAYER_SIZE // 2, Settings.PLAYER_SIZE, Settings.PLAYER_SIZE))
        
        # The end position of the direction vector is the player's position plus the direction vector
        end_position = self.position + self.direction_vector
        
        if show_line:
            pygame.draw.line(screen, Settings.LINE_COLOR, self.position, end_position, 2)

    def move(self):
        """Moves the player in the direction of the current angle."""
        
        
        init_position = self.position # Save the initial position for the animation
        
        # Calculate the final position after moving. Its just addition!
        final_position = self.position + self.direction_vector
        
        # The rest is just for animation
        length = self.direction_vector.length()
        N = int(length // 3)
        step = (final_position - self.position) / N
       
        for i in range(N):
            self.position += step
            screen.fill(Settings.BACKGROUND_COLOR)
            self.draw(show_line=False)
            pygame.draw.line(screen, Settings.LINE_COLOR, init_position, final_position, 2)
            pygame.display.flip()
            clock.tick(Settings.FPS)
def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Sprite Animation Test")

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
    player = frog_sprites[0].get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    pygame.math.Vector2(1, 0)
    def draw_alligator(alligator, index):
        """Creates a composed image of the alligator sprites.

        Args:
            alligator (list): List of alligator sprites.
            index (int): Index value to determine the right side sprite.

        Returns:
            pygame.Surface: Composed image of the alligator.
        """
        
        index = index % (len(alligator)-2)
        
        width = alligator[0].get_width()
        height = alligator[0].get_height()
        composed_image = pygame.Surface((width * 3, height), pygame.SRCALPHA)

        composed_image.blit(alligator[0], (0, 0))
        composed_image.blit(alligator[1], (width, 0))
        composed_image.blit(alligator[(index + 2) % len(alligator)], (width * 2, 0))

        return composed_image
    key_limit = 0
    while running:
        screen.fill((0,127,255))  # Clear screen with deep blue

        # Update animation every few frames
        frame_count += 1
        key_limit += 1
        
        
        
        keys = pygame.key.get_pressed()
        
        if key_limit%3 == 0: # Limit frequency of key presses so the user can set exact angles
            if keys[pygame.K_RIGHT]:
                player.direction_vector = player.direction_vector.rotate(-Settings.ANGLE_CHANGE)
            elif keys[pygame.K_LEFT]: 
                player.direction_vector = player.direction_vector.rotate(Settings.ANGLE_CHANGE)
                
        if keys[pygame.K_UP]:
            player.direction_vector.scale_to_length(player.direction_vector.length() + Settings.LENGTH_CHANGE)
        elif keys[pygame.K_DOWN]:
            player.direction_vector.scale_to_length(player.direction_vector.length() - Settings.LENGTH_CHANGE)
        elif keys[pygame.K_SPACE]:
            player.center += pygame.Vector2(0, -1)
        if frame_count % frames_per_image == 0: 
            frog_index = (frog_index + 1) % len(frog_sprites)
            allig_index = (allig_index + 1) % len(allig_sprites)
        
        # Get the current sprite and display it in the middle of the screen
        
        
        screen.blit(frog_sprites[frog_index], player)

        composed_alligator = draw_alligator(allig_sprites, allig_index)
        screen.blit(composed_alligator,  sprite_rect.move(0, 100))

        screen.blit(log,  sprite_rect.move(0, -100))


        # Update the display
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
