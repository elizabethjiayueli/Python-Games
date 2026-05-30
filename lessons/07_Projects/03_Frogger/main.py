from tkinter import Tk, font, messagebox, simpledialog

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
    obstacle_speed = 0.25
    width, height = 48, 56
    WIDTH, HEIGHT = 600, 300
    PLAYER_SIZE = 25
    position = (100, 1000)
    LINE_COLOR = (255, 0, 0)
    red = LINE_COLOR
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
        self.rect.x +=self.rect.width//8
        self.rect.y +=self.rect.height//8
        self.rect.height -= rect.height*1/4
        self.rect.width -= rect.width//4
        #self.position = pygame.math.Vector2(rect[0], rect[1])  
        self.N = 0
        self.step = 0
        #self.init_position, self.final_position = 0,0
        self.image = self.frog_sprites[0]


    def draw(self, frog_index, show_line=True):
        """Draws the player and the direction vector on the screen."""
        self.rect.center= self.rect.x+20, self.rect.y+20 
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
        self.image = pygame.transform.scale(self.original_image, (65, 40))
        self.rect = self.image.get_rect()
        self.rect[1] = random.randint(0,3)*50+50
        self.direction = direction
        if direction == 0:
            self.move = -Settings.obstacle_speed
            
            self.rect.left = Settings.screen_width
        
        if direction == 1:
            self.move = Settings.obstacle_speed
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
        #self.rect.draw(Settings.screen)
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
        self.health = 5
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
sprite_rect = game.frog_sprites[0].get_rect(center=(Settings.screen.get_width() // 2, Settings.screen.get_height()))
player = Player(sprite_rect, game.frog_sprites)
player_group = pygame.sprite.GroupSingle(player)
lives = 5
font = pygame.font.SysFont(None, 40)
level=1
high_score = 0
score_text = font.render(f"Level {level}", True, (255, 255, 255))

hold=False
pygame.math.Vector2(1, 0)
key_limit = 0
running = True
tick_count = 10000
score = 0
while running:
    frog_sprites = scale_sprites(game.spritesheet.load_strip(0, 4, colorkey=-1) , 4)

    # Update animation every few frames
    game.frame_count += 1
    key_limit += 1
    if tick_count <= 0:
        tick_count = 0
    else:
        tick_count -=1
    
    ticks = int(tick_count)//100
    
    # Health bars
    
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
    collider = pygame.sprite.spritecollide(player, game.cars, False)
    if collider:
        print("collision")
        player.rect.center = (Settings.screen.get_width() // 2, Settings.screen.get_height())
        lives -= 1
        score -= 50
        if lives <=0:
            print("Game Over")
            Settings.obstacle_speed = 0.25
            level = 1
            score = 0
            lives = 5
            score_text = font.render(f"Level {level}", True, (255, 255, 255))
            Settings.screen.blit(score_text, (32, 48)) 
        if score > high_score:
            high_score = score
            print("New high score: ", high_score)
        print("lives remaining: ", lives)
    if player.rect.y <= 0:
        level+=1
        player.rect.y = Settings.screen_height
        Settings.obstacle_speed += 0.1
        print(ticks)
        score += ticks + 50
        tick_count = 10000

        
        print("Level up! Current level: ", level)
        if level > high_score:
            high_score = level
            print("New high score: ", high_score)
    
        player.rect.center = (Settings.screen.get_width() // 2, Settings.screen.get_height())
    score_text = font.render(f"Level {level}", True, (255, 255, 255))
    Settings.screen.blit(score_text, (16, 24))   
    Settings.screen.blit(game.full_background, (0,0))
    game.handle_events()
    # player_group.draw(Settings.screen)
    # pygame.display.flip()
    player.update()
    
    player_group.draw(Settings.screen)
    game.create_obstacles()
    for car in game.cars:
        car.update()
        #pygame.draw.rect(Settings.screen, Settings.LINE_COLOR, player.rect)
        #zpygame.draw.rect(Settings.screen, Settings.LINE_COLOR, car.rect)
    game.cars.draw(Settings.screen)
    Settings.screen.blit(score_text, (10, 24)) 
    tick_text = font.render(f"Score: {score}", True, (8, 17, 59))
    Settings.screen.blit(tick_text, (400, 270)) 
    if lives > 0:
        health_1 = pygame.draw.circle(Settings.screen, Settings.red, (29, 280), 5)
    if lives > 1:
        health_2 = pygame.draw.circle(Settings.screen, Settings.red, (44, 280), 5)
    if lives > 2:
        health_3 = pygame.draw.circle(Settings.screen, Settings.red, (59, 280), 5)
    if lives > 3:
        health_4 = pygame.draw.circle(Settings.screen, Settings.red, (74, 280), 5)
    if lives > 4:
        health_5 = pygame.draw.circle(Settings.screen, Settings.red, (89, 280), 5)
    pygame.display.flip()
    pygame.display.flip()
    
   
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

        
    

    
pygame.quit()