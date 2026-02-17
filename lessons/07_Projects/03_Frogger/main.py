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
    screen_height = 300
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('FROGGER')  
    FPS = 30
    obstacle_speed = 10
    width, height = 48, 56
    WIDTH, HEIGHT = 600, 300
    PLAYER_SIZE = 25
    position = (100, 1000)
#screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
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
        self.position = pygame.math.Vector2(3)  
        self.N = 0
        self.step = 0
        self.init_position, self.final_position = 0,0
        self.image = self.frog_sprites[0]


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
    def update(self):
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > Settings.screen_height - self.rect.height:
            self.rect.y = Settings.screen_height - self.rect.height
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > Settings.screen_width - self.rect.width:
            self.rect.x = Settings.screen_width - self.rect.width
        if self.rect.y >=Settings.screen_height:
            self.rect.y = 0

class Car(pygame.sprite.Sprite):
    def __init__(self, game, direction):
        super().__init__()
        self.original_image = pygame.image.load(assets/'carLeft.png')
        self.rect = self.original_image.get_rect()
        self.rect[1] = random.randint(0,3)*50+50
        print (self.rect[1])
        self.image = pygame.transform.scale(self.original_image, (65, 40))
        self.direction = direction
        if direction == 0:
            self.move = -0.5
            
            self.rect.left = Settings.screen_width
        
        if direction == 1:
            self.move = 0.5
            self.largeimage = pygame.transform.flip(pygame.image.load(assets/'carLeft.png'), True, False)
            self.image = pygame.transform.scale(self.largeimage, (65, 40))
            self.rect.right = 0
          
    def update(self):
        #print(self.rect[0], "before move")
        if self.direction == 0:
            self.rect[0] += self.move 
        if self.direction == 1:
            self.rect.right += self.move
        # print(self.rect[0], "after move")
        # print(self.direction, "direction")
        # print(self.rect.right, self.rect.left, "positions")
        if self.direction == 0 and self.rect.left <= 0:
            
            self.kill()
            #print("kill")
            
        if self.direction == 1 and self.rect.left >= Settings.screen_width:
            self.kill()
            #print("kill")
        if self.rect.y <= 50 or self.rect.y >= Settings.screen_height-80:
            self.kill()
            #print("remove offscreen")
class Log(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        pass

class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.logs = pygame.sprite.Group()
        self.filename = assets / 'spritesheet.png'  # Replace with your actual file path
        self.cellsize = (16, 16)  # Replace with the size of your sprites
        self.spritesheet = SpriteSheet(self.filename, self.cellsize)
        self.frog_sprites = scale_sprites(self.spritesheet.load_strip(0, 4, colorkey=-1) , 4)
        
    # Compose an image
        log = self.spritesheet.compose_horiz([24, 25, 26], colorkey=-1)
        log = pygame.transform.scale(log, (log.get_width() * 4, log.get_height() * 4))

        # Variables for animation
        self.frog_index = 0
        self.frames_per_image = 6
        self.frame_count = 0
        self.create_obstacles()
        self.full_background = self.make_tiled_bg(Settings.screen, assets/'frogger_road_bg.png')

    def create_obstacles(self):
        # Create cars and logs and add them to their respective groups
        if self.frame_count % 150 == 0:
            direction = random.choice([0, 1])
            car = Car(self, direction)
            # car.rect.y = random.randint(1,5)*100+50
            #print(car.rect.y)
            self.cars.add(car)
            self.all_sprites.add(car)
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
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         #print("space pressed")
            if event.type == pygame.QUIT:
                self.running = False
    
        
    
    


    # Load a strip sprites
    

    # Main game loop
running = True
game = Game()
sprite_rect = game.frog_sprites[0].get_rect(center=(Settings.screen.get_width() // 2, Settings.screen.get_height() // 2))
player = Player(sprite_rect, game.frog_sprites)
player_group = pygame.sprite.GroupSingle(player)


hold=False
pygame.math.Vector2(1, 0)
key_limit = 0
running = True
while running:
    frog_sprites = scale_sprites(game.spritesheet.load_strip(0, 4, colorkey=-1) , 4)

    # Update animation every few frames
    game.frame_count += 1
    key_limit += 1

    # Create cars
    

    keys = pygame.key.get_pressed()
    
    if hold == False:
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.rect.x += 50
            hold = True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: 
            player.rect.x -= 50  
            hold = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.rect.y -= 50
            hold = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            
            player.rect.y += 50
            hold = True
    if not any(keys):
        hold = False

    Settings.screen.blit(game.full_background, (0,0))
    game.handle_events()
    # player_group.draw(Settings.screen)
    # pygame.display.flip()
    player.update()
    player_group.draw(Settings.screen)
    game.create_obstacles()
    for car in game.cars:
        car.update()
    game.cars.draw(Settings.screen)
    pygame.display.flip() 
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

        
    

    
pygame.quit()