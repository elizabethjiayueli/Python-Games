import pygame
pygame.init

from pathlib import Path
assets = Path(__file__).parent / 'images'
background = pygame.image.load(assets/'background.png')
class Settings:
    # Screen
    screen_width = 288
    screen_height = 500
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Flappy Birb')
    # Gravity
    gravity: int = 1
    flap_y_velocity: int = 16
    
    
    player_y_velocity = 0

class Flappy():
    def __init__(self):
        self.images = [pygame.image.load(assets/'bluebird-upflap.png'),
        pygame.image.load(assets/'bluebird-midflap.png'),
        pygame.image.load(assets/'bluebird-downflap.png')]
        self.image_num = 0
        self.image = pygame.image.load(assets/'bluebird-upflap.png')
        self.hitbox = self.images[1].get_rect
        self.y_vel = 0
        self.score = 0
        self.frames = 0
    def update(self): 
        self.frames += 1
        self.image_num = (self.image_num +1) % 3
        # Animation
        self.image = self.images[self.current_image]
        ## Jumping detection
        keys = pygame.key.get_pressed()  
        if self.rect.bottom == Settings.HEIGHT:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.y_vel = -Settings.flap_y_velocity
        # Gravity 
        self.y_vel += Settings.gravity
        self.rect.y += self.y_vel
        
        # Keep the player on screen
        if self.rect.top < 0: 
            self.rect.top = 0
        if self.rect.bottom > Settings.HEIGHT:
            self.rect.bottom = Settings.HEIGHT

        Settings.screen.blit()

class Game():
    clock = pygame.time.Clock()
    game_over = False
    last_obstacle_time = pygame.time.get_ticks()

    # Group for obstacles
    obstacles = pygame.sprite.Group()
    obstacle_count = 0
    player = Flappy()
    

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    Settings.screen.blit(Game.full_background,(0,0))

    # Update the display
    pygame.display.flip()