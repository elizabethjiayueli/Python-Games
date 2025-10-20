import pygame
import random
import time
import math
from jtlgames.spritesheet import SpriteSheet

# Initialize Pygame
pygame.init()
from pathlib import Path
assets = Path(__file__).parent / 'images'
background = pygame.image.load(assets/'frogger_road_bg.png')

clock = pygame.time.Clock()

class Settings: 
    # Screen
    screen_width = 550
    screen_height = 520
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('FROGGER')  
    FPS = 30
    obstacle_speed = 10
    width, height = 48, 56
    WIDTH, HEIGHT = 600, 300
    PLAYER_SIZE = 25
    position = (100, 1000)
screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
def scale_sprites(sprites, scale):
    """Scale a list of sprites by a given factor.

    Args:
        sprites (list): List of pygame.Surface objects.
        scale (int): Scale factor.

    Returns:
        list: List of scaled pygame.Surface objects.
    """
    return [pygame.transform.scale(sprite, (sprite.get_width() * scale, sprite.get_height() * scale)) for sprite in sprites]

class Player(pygame.sprite.Sprite):

    def __init__(self, rect, frog_sprites):
        """Initializes the Player with a position and direction vector.

        Args:
            x (int): The initial x-coordinate of the player.
            y (int): The initial y-coordinate of the player.
        """
        super().__init__()
        self.frog_sprites = frog_sprites
        self.rect = rect
        self.rect.height = rect.height/2
        self.rect.width = rect.width/2
        self.position = pygame.math.Vector2(rect.center)  
        self.N = 0
        self.step = 0
        self.init_position, self.final_position = 0,0


    def draw(self, frog_index, show_line=True):
        """Draws the player and the direction vector on the screen."""
        x, y = self.rect.center
        #pygame.draw.rect(screen, Settings.PLAYER_COLOR, (self.position.x - Settings.PLAYER_SIZE // 2, self.position.y - Settings.PLAYER_SIZE // 2, Settings.PLAYER_SIZE, Settings.PLAYER_SIZE))
        
        width, height = self.rect[2], self.rect[3]
        y -= height//2
        # The end position of the direction vector is the player's position plus the direction vector
        
        
        if self.N > 0:
            self.rect.center += self.step
            #pygame.draw.line(screen, Settings.LINE_COLOR, self.rect.center, self.final_position, 2)
            
            
            self.N -= 1
        

        # elif show_line:
            #pygame.draw.line(screen, Settings.LINE_COLOR, self.rect.center, end_position, 2)
        

class Car(pygame.sprite.Sprite):
    def __init__(self, game, direction):
        super().__init__()
        pass

class Log(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        pass

class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.logs = pygame.sprite.Group()
        
        self.create_obstacles()
        self.full_background = self.make_tiled_bg(Settings.screen, assets/'frogger_road_bg.png')

    def create_obstacles(self):
        # Create cars and logs and add them to their respective groups
        pass
    def make_tiled_bg(self, screen, background):
        # Scale background to match the screen height
        bg_tile = pygame.image.load(background).convert()
        background_height = Settings.screen.get_height()
        bg_tile = pygame.transform.scale(bg_tile, (bg_tile.get_width(), 300))
        # Get the dimensions of the background after scaling
        background_width = bg_tile.get_width()
        return bg_tile
    def handle_events(self):
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("space pressed")
            if event.type == pygame.QUIT:
                self.running = False
    filename = assets / 'spritesheet.png'  # Replace with your actual file path
    cellsize = (16, 16)  # Replace with the size of your sprites
    spritesheet = SpriteSheet(filename, cellsize)


    # Load a strip sprites
    frog_sprites = scale_sprites(spritesheet.load_strip(0, 4, colorkey=-1) , 4)

    # Compose an image
    log = spritesheet.compose_horiz([24, 25, 26], colorkey=-1)
    log = pygame.transform.scale(log, (log.get_width() * 4, log.get_height() * 4))

    # Variables for animation
    frog_index = 0
    frames_per_image = 6
    frame_count = 0

    # Main game loop
    running = True
    
    sprite_rect = frog_sprites[0].get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    player = Player(sprite_rect, frog_sprites)
    player_group = pygame.sprite.GroupSingle(player)
    
    pygame.math.Vector2(1, 0)
    
    key_limit = 0
    while running:
        

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
            
        
    
        
        # Get the current sprite and display it in the middle of the screen
        
        
        #pygame.draw.rect(screen, Settings.LINE_COLOR, player.rect)
        player.draw(frog_index)

            
         
game = Game()


run = True
running = True
while running:
    Settings.screen.blit(game.full_background, (0,0))
    game.handle_events()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip() 

        
    

    
    clock.tick(Settings.FPS)