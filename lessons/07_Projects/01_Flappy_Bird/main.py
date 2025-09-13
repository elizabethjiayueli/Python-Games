import pygame
import time
import random
pygame.init()
clock = pygame.time.Clock()

from pathlib import Path
assets = Path(__file__).parent / 'images'
background = pygame.image.load(assets/'background.png')
class Settings:
    # Screen
    screen_width = 288
    screen_height = 500
    pipe_width = 80
    pipe_height = 500
    position = (100, 100)   
    #pipe_speed = 
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Flappy Birb')  
    FPS = 30
    # Gravity
    gravity = -1
    flap_y_velocity = 12  
    player_y_velocity = 0

class Flappy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_num = 0
        self.image = pygame.image.load(assets/'bluebird-upflap.png')
        self.images =  [pygame.image.load(assets/'bluebird-upflap.png'),
                        pygame.image.load(assets/'bluebird-midflap.png'),
                        pygame.image.load(assets/'bluebird-downflap.png')]
        self.rect = self.images[1].get_rect(center = Settings.position)
        self.y_vel = -1
        self.score = 0
        self.frames = 0
        self.pressed = False
        #self.rect = pygame.draw.rect(Settings.screen, 144, 250, (self.image.get_width, self.image.get_height))
        
    def update(self): 
        #self.frames += 1

        # Animation
        self.image_num = (self.image_num +1) % 3
        self.image = self.images[self.image_num]

        # Jumping
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.pressed == False:
            self.y_vel = -Settings.flap_y_velocity
            self.pressed = True
        elif keys[pygame.K_SPACE] == False and keys[pygame.K_UP] == False:
            self.pressed = False

        # Gravity 
        self.rect.y += self.y_vel
        self.y_vel -= Settings.gravity
        #self.rect.y += self.y_vel
        
        # Keep the player on screen
        if self.rect.top < 0: 
            self.rect.top = 0
        if self.rect.bottom > Settings.screen_height:
            self.rect.bottom = Settings.screen_height

class Pipe(pygame.sprite.Sprite):
    def __init__(self, flipped):
        super().__init__()
        self.original_image = pygame.image.load(assets/'pipe-green.png')
        self.image = pygame.transform.scale(self.original_image, (Settings.pipe_width, Settings.pipe_height))
        if flipped == True:
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()
        #Settings.screen.blit(self.image, Settings.screen)
        self.rect[0] = Settings.screen_width
    def update(self):
        self.rect[0] -= 5
        
class Pipes():
    def __init__(self):
        self.lower_pipe = Pipe(False)
        self.upper_pipe = Pipe(True)
        self.gap = 150
        self.lower_pipe.rect[1] = random.randint(200, 500)
        self.upper_pipe.rect[1] = self.lower_pipe.rect[1] - self.gap- self.upper_pipe.rect[3]
    
    def update(self):

        self.lower_pipe.update()
        self.upper_pipe.update()
        

        
        # if self.lower_pipe.rect[0] <= -Settings.pipe_width: # Original
        if self.lower_pipe.rect.right <= 0: 
            self.lower_pipe.rect.x = Settings.screen_width 
            self.upper_pipe.rect.x = Settings.screen_width  
            self.lower_pipe.rect.y = random.randint(200, 400) 
            self.upper_pipe.rect.y = self.lower_pipe.rect.y - self.gap - self.upper_pipe.rect.height # Reset y using .y and .height
            Game.score += 1
            
            print(Game.score)
        
class Game():
    
    game_over = False
    last_obstacle_time = pygame.time.get_ticks()
    pygame.key.set_repeat(2000)
    # Group for obstacles
    obstacles = pygame.sprite.Group()
    score = 0
    player = Flappy()
    pipes = Pipes()
    obstacles.add(pipes.lower_pipe, pipes.upper_pipe)
    player_group = pygame.sprite.GroupSingle(player)
    
    
   
    def make_tiled_bg(screen, background):
        "Scale background to match the screen height"
        
        bg_tile = pygame.image.load(background).convert()
        
        background_height = screen.get_height()
        bg_tile = pygame.transform.scale(bg_tile, (bg_tile.get_width(), screen.get_height()))
        # Get the dimensions of the background after scaling
        background_width = bg_tile.get_width()
        return bg_tile
    
    

    full_background = make_tiled_bg(Settings.screen, assets/'background.png')
    # player.blit(Settings.screen)
    # obstacles.draw(Settings.screen)
pygame.font.init()
game_active = False 
countdown_start_time = pygame.time.get_ticks()
countdown_duration = 3000 
countdown_font = pygame.font.SysFont(None, 100) 
font = pygame.font.SysFont(None, 40) 
text = Game.score
game = Game()


running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    if not game_active:
        
        current_time = pygame.time.get_ticks()
        time_left = countdown_duration - (current_time - countdown_start_time)
        
        if time_left <= 0:
            game_active = True
            pygame.display.flip()
            pygame.time.delay(500)
            # game.player.rect.center = Settings.position 
            # game.obstacles.empty() 
        else:
            countdown_seconds = int(time_left / 1000) + 1 
            text_to_display = str(countdown_seconds)
            
            
    else: 
        game.player.update()
        game.pipes.update()
        #game.player.draw()
         
        
        # Collision detection
        collider = pygame.sprite.spritecollide(game.player, game.obstacles, dokill=False)
        if collider:
            print("Your score was:", game.score)
            running = False 

       

    
    Settings.screen.blit(game.full_background, (0, 0))

    if not game_active:
        countdown_text_surface = countdown_font.render(text_to_display, True, (255, 255, 255))
        text_rect = countdown_text_surface.get_rect(center=(Settings.screen_width / 2, Settings.screen_height / 2))
        Settings.screen.blit(countdown_text_surface, text_rect)
    else:
        score_text = font.render(str(game.score), True, (0, 0, 0)) 
        Settings.screen.blit(score_text, (32, 48)) 
        game.player_group.draw(Settings.screen)
        game.obstacles.draw(Settings.screen)

    
    pygame.display.flip() 

    
    clock.tick(Settings.FPS) 

pygame.quit()                
        

