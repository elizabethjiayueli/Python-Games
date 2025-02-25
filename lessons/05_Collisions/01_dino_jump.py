"""
Dino Jump

Use the arrow keys to move the blue square up and down to avoid the Settings.
obstacles. The game should end when the player collides with an obstacle ...
but it does not. It's a work in progress, and you'll have to finish it. 

"""
from pathlib import Path
assets = Path(__file__).parent / "images"
import pygame
import random
from pathlib import Path

# Initialize Pygame 
pygame.init()

images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"

class Settings:
    WIDTH, HEIGHT = 600, 300
    

    # Colors
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Settings.FPS
    FPS = 60

    # Player attributes
    PLAYER_SIZE = 25
    high_score = 0
    player_speed = 5

    # Obstacle attributes
    OBSTACLE_WIDTH = 20
    OBSTACLE_HEIGHT = 20
    obstacle_speed = 5

    # Font
    font = pygame.font.SysFont(None, 36)
    #Gravity stuff
    
    gravity: int = 1
    jump_y_velocity: int = 100 
    jump_x_velocity: int = 10
    player_x_velocity = 0
    player_y_velocity = 0
screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
pygame.display.set_caption("Dino Jump")
# Define an obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(assets/'cactus_9.png')
        
        self.image = pygame.transform.scale(self.original_image, (100, 200))
        self.rect = self.image.get_rect()
        self.rect.x = Settings.WIDTH
        self.rect.y = Settings.HEIGHT - Settings.OBSTACLE_HEIGHT - 180

        
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
        
        
        self.image = pygame.transform.scale(self.original_image, (30, 35))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = Settings.HEIGHT - Settings.PLAYER_SIZE - 10 
        self.speed = Settings.player_speed
        self.y_vel = 0
        self.score = 0
    def update(self): 
         

        keys = pygame.key.get_pressed()  
        if self.rect.bottom == Settings.HEIGHT:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.y_vel = -Settings.jump_y_velocity
            
             
            
        self.y_vel += Settings.gravity
        self.rect.y += self.y_vel
        
        # Keep the player on screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > Settings.HEIGHT:
            self.rect.bottom = Settings.HEIGHT

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
            game_over = True
       
        # Draw everything
        screen.fill(Settings.WHITE)
        player_group.draw(screen)
        obstacles.draw(screen)

        # Display obstacle count
        obstacle_text = Settings.font.render(f"Score: {obstacle_count}", True, Settings.HEIGHT)
        screen.blit(obstacle_text, (10, 10))

        pygame.display.update()
        clock.tick(Settings.FPS)
        #return obstacle_count

    # Game over screen
    
    while not pygame.key.get_pressed()[pygame.K_RETURN]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        run = pygame.key.get_pressed()
        end_text = Settings.font.render("Press Enter to Start Over", True, Settings.HEIGHT)
        screen.blit(end_text, (150, 100))

        if obstacle_count > Settings.high_score:
            Settings.high_score = obstacle_count
        obstacle_text = Settings.font.render(f"High score: {Settings.high_score}", True, Settings.HEIGHT)
        screen.blit(obstacle_text, (210, 125))
        pygame.display.update()
    
    Game()
if __name__ == "__main__":
    Game()
