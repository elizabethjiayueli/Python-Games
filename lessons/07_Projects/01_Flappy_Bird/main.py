import pygame
pygame.init

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
    # Gravity
    gravity = 0.5
    flap_y_velocity = 1.9
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
        self.y_vel = 2
        self.score = 0
        self.frames = 0
        #self.rect = pygame.draw.rect(Settings.screen, 144, 250, (self.image.get_width, self.image.get_height))
        
    def update(self): 
        #self.frames += 1

        # Animation
        self.image_num = (self.image_num +1) % 3
        self.image = self.images[self.image_num]

        # Jumping
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.y_vel -= Settings.flap_y_velocity
        # Gravity 
        self.rect.y += self.y_vel
        #self.rect.y += self.y_vel
        
        # Keep the player on screen
        if self.rect.top < 0: 
            self.rect.top = 0
        if self.rect.bottom > Settings.screen_height:
            self.rect.bottom = Settings.screen_height


class Pipes(pygame.sprite.Sprite):
    def __init__(self):
        self.gap = 150
        self.original_image = pygame.image.load(assets/'pipe-green.png')
        self.image = pygame.transform.scale(self.original_image, (Settings.pipe_width, Settings.pipe_height))
        

class Game():
    clock = pygame.time.Clock()
    game_over = False
    last_obstacle_time = pygame.time.get_ticks()

    # Group for obstacles
    obstacles = pygame.sprite.Group()
    obstacle_count = 0
    player = Flappy()
    player_group = pygame.sprite.GroupSingle(player)
    

    def make_tiled_bg(screen, background):
        # Scale background to match the screen height
        
        bg_tile = pygame.image.load(background).convert()
        
        background_height = screen.get_height()
        bg_tile = pygame.transform.scale(bg_tile, (bg_tile.get_width(), screen.get_height()))
        # Get the dimensions of the background after scaling
        background_width = bg_tile.get_width()
        return bg_tile
    
    

    full_background = make_tiled_bg(Settings.screen, assets/'background.png')
    # player.blit(Settings.screen)
    # obstacles.draw(Settings.screen)
# Main loop
running = True
while running:
    Game.player.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    Settings.screen.blit(Game.full_background,(0,0))
    Game.player_group.draw(Settings.screen)
    # Update the display
    pygame.display.flip()