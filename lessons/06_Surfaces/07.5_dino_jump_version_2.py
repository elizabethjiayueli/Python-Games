"""
Dino Jump

Use the arrow keys to move the blue square up and down to avoid the Settings.
obstacles. The game should end when the player collides with an obstacle ...
but it does not. It's a work in progress, and you'll have to finish it. 

## = MY COMMENTS
"""
from pathlib import Path
#assets = Path(__file__).parent / "images"
assets = Path("/workspaces/Python-Games/lessons/05_Collisions/images")
import pygame
import random
from pathlib import Path
import time

# Initialize Pygame 
pygame.init()

images_dir = assets if assets.exists() else Path(__file__).parent / "assets"

class Settings:
    WIDTH, HEIGHT = 600, 300
    
    width, height = 48, 56
    # Colors
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Settings.FPS
    FPS = 60

    # Player attributes
    PLAYER_SIZE = 25
    high_score = -101
    player_speed = 5

    # Obstacle attributes
    OBSTACLE_WIDTH = 20
    OBSTACLE_HEIGHT = 20
    obstacle_speed = 5

    # Font
    font = pygame.font.SysFont(None, 36)
    #Gravity stuff
    
    gravity: int = 1
    jump_y_velocity: int = 16
    jump_x_velocity: int = 1
    player_x_velocity = 0
    player_y_velocity = 0
screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
pygame.display.set_caption("Dino Jump")
# Define an obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(assets/'cactus_9.png')
        
        self.image = pygame.transform.scale(self.original_image, (40, 70))
        self.rect = self.image.get_rect()
        self.rect.x = Settings.WIDTH
        self.rect.y = Settings.HEIGHT - Settings.OBSTACLE_HEIGHT - 45
        

        
        self.explosion = pygame.image.load(images_dir / "explosion1.gif")

    def update(self):
        self.rect.x -= Settings.obstacle_speed
        # Remove the obstacle if it goes off screen
        if self.rect.right < 0:
            self.kill()

    def explode(self):
        """Replace the image with an explosition image."""
        
        # Load the explosion image
        self.image = self.explosion
        self.image = pygame.transform.scale(self.image, (Settings.OBSTACLE_WIDTH, Settings.OBSTACLE_HEIGHT))
        self.rect = self.image.get_rect(center=self.rect.center)


# Define a player class
class Player(pygame.sprite.Sprite):
    def __init__(self): 
        super().__init__()
        self.original_image = pygame.image.load(assets/'dino_0.png')
        
        
        self.image = pygame.transform.scale(self.original_image, (Settings.width, Settings.height))
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = Settings.HEIGHT - Settings.PLAYER_SIZE -7
        
        self.speed = Settings.player_speed
        self.y_vel = 0
        self.score = 0
        self.frames = 0
        ## Different images for squashing
        self.image_reg = pygame.transform.scale(self.original_image, (Settings.width, Settings.height))
        self.rect_reg = self.image.get_rect()
        self.image_squash = pygame.transform.scale(self.original_image, (Settings.width, Settings.height/2))
        self.rect_squash = self.image_squash.get_rect()
        self.is_squashing = False
        self.original_height = Settings.height
        self.squashed_height = 56
    def update(self): 
        # self.frames += 1

        ## Jumping detection
        keys = pygame.key.get_pressed()  
        if self.rect.bottom == Settings.HEIGHT:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.y_vel = -Settings.jump_y_velocity
            
             
            
        self.y_vel += Settings.gravity
        self.rect.y += self.y_vel
        
        # Keep the player on screen
        if self.rect.top < 0: 
            self.rect.top = 0
        if self.rect.bottom <= Settings.HEIGHT:
            self.image = self.image_reg
            self.rect = self.rect_reg
        if self.y_vel == 0:
            self.image = self.image_reg
        if self.rect.bottom > Settings.HEIGHT:
            #pass                   
            self.rect.bottom = Settings.HEIGHT
            self.image = self.image_squash
            self.rect = self.rect_squash
        
        #.if self.rect.bottom >= Settings.HEIGHT and self.y_vel > 0:   
        ## Sqaush timing
        if self.rect.bottom >= Settings.HEIGHT and self.y_vel > 0 and self.is_squashing == False:
            print("...")
            self.is_squashing = True
            self.image = self.image_squash
            self.rect = self.rect_squash
        if self.is_squashing == True:
            self.frames += 1
            self.score = self.frames//5
            Settings.height = self.squashed_height
        # if self.frames %30 == 0:
        #     self.image = self.image_reg
        #     self.is_squashing = False
        #     self.frames = 0 
        #     self.rect = self.rect_reg
        # elif self.rect.    
        #     #screen.blit(self.image, (self.rect.x, self.rect.y))

# Create a player object
player = Player()
player_group = pygame.sprite.GroupSingle(player)
 
# Add obstacles periodically
def add_obstacle(obstacles):
    # random.random() returns a random float between 0 and 1, so a value
    # of 0.25 means that there is a 25% chance of adding an obstacle. Since
    # add_obstacle() is called every 100ms, this means that on average, an
    # obstacle will be added every 400ms.
    # The combination of the randomness and the time allows for random
    # obstacles, but not too close together. 
    
    if random.random() < 0.4 :
        obstacle = Obstacle()
        obstacles.add(obstacle)
        return 1
    return 0


# Main game loop
def Game():
    
    clock = pygame.time.Clock()
    game_over = False
    last_obstacle_time = pygame.time.get_ticks()

    # Group for obstacles
    obstacles = pygame.sprite.Group()
    obstacle_count = 0
    player = Player()
    
    player_group = pygame.sprite.GroupSingle(player)
    

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Update player
        player.update()

        # Add obstacles and update
        if pygame.time.get_ticks() - last_obstacle_time > 500:
            last_obstacle_time = pygame.time.get_ticks()
            obstacle_count += add_obstacle(obstacles)

        obstacles.update()

        # Check for collisions
        collider = pygame.sprite.spritecollide(player, obstacles, dokill=False)
        if collider:
            collider[0].explode()
            player = Player()
            game_over = True
            #player.image = player.image2
            #player.rect = player.rect2
            #player.rect.x = player.rect.x2
            #player.rect.y = player.rect.y2
            
       
        # Draw everything
        screen.fill(Settings.WHITE)
        player_group.draw(screen)
        obstacles.draw(screen)

        # Display obstacle count
        obstacle_text = Settings.font.render(f"Score: {player.score}", True, Settings.HEIGHT)
        screen.blit(obstacle_text, (10, 10))
        saved_score = player.score
        pygame.display.update()
        clock.tick(Settings.FPS)
        #return obstacle_count

    # Game over screen
    
    while not pygame.key.get_pressed()[pygame.K_RETURN]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        player.score = saved_score
        run = pygame.key.get_pressed()
        end_text = Settings.font.render("Press Enter to Start Over", True, Settings.HEIGHT)
        screen.blit(end_text, (150, 100))
        erase_score = pygame.Rect(0,0,200,50)
        pygame.draw.rect(screen, Settings.WHITE, erase_score)
        obstacle_text = Settings.font.render(f"High score: {Settings.high_score}", True, Settings.HEIGHT)
        if player.score >= Settings.high_score:
            obstacle_text = Settings.font.render(f"High score: {player.score}", True, Settings.HEIGHT)
        
        
        screen.blit(obstacle_text, (210, 125))
        player.image = player.image_reg
        pygame.display.update()
    
    Game()
if __name__ == "__main__":
    Game()
