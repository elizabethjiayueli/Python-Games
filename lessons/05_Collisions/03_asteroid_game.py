from pathlib import Path


assets = Path(__file__).parent / "images"
import pygame
import math  
from pygame.math import Vector2
import random
from pathlib import Path
images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"
pygame.init()
class Settings:
    """Class to store game configuration."""

    width = 600
    height = 600
    fps = 60
    triangle_size = 20 
    triangle_speed = 5
    projectile_speed = 5
    projectile_size = 11
    shoot_delay = 250       # 250 milliseconds between shots, or 4 shots per second
    colors = {"white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0)}
    OBSTACLE_HEIGHT = 20 
    OBSTACLE_WIDTH = 20
    green = (0,255,0)
    white = (255,255,255)
    obstacle_speed = 1
    font = pygame.font.SysFont("Tahoma", 26)
# Notice that this Spaceship class is a bit different: it is a subclass of
# Sprite. Rather than a plain class, like in the previous examples, this class
# inherits from the Sprite class. The main additional function of a Sprite is
# that it can be added and removed from groups. This is useful for handling
# multiple objects of the same type, like projectiles.
class Spaceship(pygame.sprite.Sprite): 
    """Class representing the spaceship."""

    def __init__(self, settings, position):
        super().__init__()

        self.game = None  # will be set in Game.add()
        self.settings = settings

        self.angle = 0
        self.original_image = self.create_spaceship_image()

        self.velocity = pygame.Vector2(0, 0)

        # For Sprites, the image and rect attributes are part of the Sprite class
        # and are important. The image is the surface that will be drawn on the screen

        self.image = self.original_image.copy() 
        self.rect = self.image.get_rect(center=position)

        # These values help us limit the rate of fire
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = self.settings.shoot_delay  

    def create_spaceship_image(self):
        """Creates the spaceship shape as a surface."""
        image = pygame.Surface( (self.settings.triangle_size * 2, self.settings.triangle_size * 2),pygame.SRCALPHA)
        points = [
            (self.settings.triangle_size, 0),  # top point
            (0, self.settings.triangle_size * 2),  # left side point
            (self.settings.triangle_size * 2,self.settings.triangle_size * 2, ),  # right side point
        ]
        pygame.draw.polygon(image, self.settings.colors["white"], points)
        return image

    def ready_to_shoot(self):
        """Checks if the spaceship is ready to shoot again."""
        if pygame.time.get_ticks() - self.last_shot > self.shoot_delay:
            self.last_shot = pygame.time.get_ticks()
            return True
        return False
            

    def fire_projectile(self):
        """Creates and fires a projectile."""

        new_projectile = Projectile(
            self.settings,
            position=self.rect.center,
            angle=self.angle,
            velocity=self.settings.projectile_speed,
        )

        # Important! The game will update all of the sprites in the group, so we
        # need to add the projectile to the group to make sure it is updated.
        self.game.projectiles.add(new_projectile)
        self.game.add(new_projectile)


    # The Sprite class defines an update method that is called every frame. We
    # can override this method to add our own functionality. In this case, we
    # are going to handle input and update the image of the spaceship. However,
    # we also need to call the update method of the parent class, so we use
    # super().update()
    def update(self):
        if self.rect.center[0] > 600:
            print("x")
            self.rect.center = (0, self.rect.center[1])
        if self.rect.center[0] < 0:
            self.rect.center = (600, self.rect.center[1])

        if self.rect.center[1] > 800:
            print("x")
            self.rect.center = (self.rect.center[0], 0)
        if self.rect.center[1] < 0:
            self.rect.center = (self.rect.center[0], 800)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.angle -= 5

        if keys[pygame.K_RIGHT]:
            self.angle += 5

        if keys[pygame.K_SPACE] and self.ready_to_shoot():
            self.fire_projectile()

        if keys[pygame.K_UP]:
            self.velocity += pygame.Vector2(0, -0.1).rotate(self.angle)
        if keys[pygame.K_DOWN]:
            self.velocity -= pygame.Vector2(0, -0.1).rotate(self.angle)

        self.image = pygame.transform.rotate(self.original_image, -self.angle)

        # Reassigning the rect because the image has changed.
        self.rect = self.image.get_rect(center=self.rect.center)
        
        self.rect.center += self.velocity

        # Dont forget this part! If you don't call the Sprite update method, the
        # sprite will not be drawn
        super().update()

    # WAIT! Where is the draw method? We don't need to define it because the
    # Sprite class already has a draw method that will draw the image on the
    # screen. We only need to add the sprite to a group and the group will take
    # care of drawing the sprite.

        

class Projectile(pygame.sprite.Sprite):
    """Class to handle projectile movement and drawing."""

    def __init__(self, settings, position, velocity, angle):
        super().__init__()
        #self.rect = self.image.get_rect(center=position)
        self.game = None  # will be set in Game.add()
        self.settings = settings
        
        # The (0,-1) part makes the vector point up, and the rotate method
        # rotates the vector by the given angle. Finally, we multiply the vector
        # by the velocity (scalar) to get the final velocity vector.
        self.velocity = pygame.Vector2(0, -1).rotate(angle) * velocity

        # Dont forget to create the image and rect attributes for the sprite
        self.image = pygame.Surface(
            (self.settings.projectile_size, self.settings.projectile_size),
            pygame.SRCALPHA,
        )
        self.rect = self.image.get_rect(center=position)
        half_size = self.settings.projectile_size // 2

        pygame.draw.circle(
            self.image,
            self.settings.colors["red"],
            center=(half_size + 1, half_size + 1),
            radius=half_size,
        )

        # Notice that we are using the rect attribute to store the position of the projectile
        
        
    def update(self):
        self.rect.center += self.velocity
        if self.rect[0] > 589:
            self.kill()
            
        if self.rect[0] < 0:
            self.kill()

        if self.rect[1] > 800:
            self.kill()
        if self.rect[1] < 0:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(assets/'asteroid1.png')
        self.x_vel = random.uniform(-1, 1) * Settings.obstacle_speed
        self.y_vel = random.uniform(-1, 1)* Settings.obstacle_speed
        self.image = pygame.transform.scale(self.original_image, (100, 70))
        self.rect = self.image.get_rect()
        self.rect.x = Settings.width - 50.5
        self.rect.y = Settings.height - Settings.OBSTACLE_HEIGHT - 300.2
        self.pos = Vector2(self.rect.x, self.rect.y)
        self.explosion = pygame.image.load(images_dir / "explosion1.gif")

    def update(self):
        self.pos.x -= self.x_vel
        self.pos.y -= self.y_vel
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        
        # Remove the obstacle if it goes off screen
        if self.rect.right < 0:
            self.pos.x =600
            

        if self.rect.left > 600:
            self.pos.x =0
        
        if self.rect.top < 0:
            self.pos.y =530

        if self.rect.bottom > 600:
            self.pos.y =0
    def explode(self):
        """Replace the image with an explosition image."""
        
        # Load the explosion image
        self.image = self.explosion
        self.image = pygame.transform.scale(self.image, (Settings.OBSTACLE_WIDTH, Settings.OBSTACLE_HEIGHT))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.x_vel = 0
        self.y_vel = 0
# def add_obstacle(obstacles_list):
#     # random.random() returns a random float between 0 and 1, so a value
#     # of 0.25 means that there is a 25% chance of adding an obstacle. Since
#     # add_obstacle() is called every 100ms, this means that on average, an
#     # obstacle will be added every 400ms.
#     # The combination of the randomness and the time allows for random
#     # obstacles, but not too close together. 
    
#     if random.random() < 1 :
#         obstacle = Obstacle()
#         Game.obstacles.add(obstacle)
#         return 1
#     return 0 


class AlienSpaceship(Spaceship):
    
    def create_spaceship_image(self):
        """Creates the spaceship shape as a surface."""
        
        return pygame.image.load(assets/'alien2.gif')
class Game:
    """Class to manage the game loop and objects."""

    def __init__(self, settings):
        pygame.init()
        pygame.key.set_repeat(1250, 1250)
        self.obstacles = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.settings = settings
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        self.last_obstacle_time = pygame.time.get_ticks()
        self.obstacle_count = 0
        pygame.display.set_caption("Asteroids")
        self.energy = 125
        self.clock = pygame.time.Clock( )
        self.running = True

        self.all_sprites = pygame.sprite.Group()

    def add(self, sprite):
        """Adds a sprite to the game. Really important! This group is used to
        update and draw all of the sprites."""

        sprite.game = self

        self.all_sprites.add(sprite)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        self.obstacles.update()
        #Check for collisions
        
        killer_asteroid = pygame.sprite.spritecollide(spaceship, self.obstacles, dokill=False)
        if killer_asteroid:
            killer_asteroid[0].explode()
            self.energy -=25 
            print("OOF")
            self.obstacles.remove(killer_asteroid[0])
        for projectile in self.projectiles:
            
                
            collider = pygame.sprite.spritecollide(projectile, self.obstacles, dokill=False)
            if collider:
                collider[0].explode()
                Settings.obstacle_speed += 0.01
                print("Great Shot!!!!")
                self.obstacles.remove(collider[0])
                self.obstacle_count += 1
                projectile.kill()
        self.update()
                
        # for obstacle in self.obstacles:
        #     #print(obstacle)
        #     self.obstacles.remove()
            

        pygame.display.flip()
                
    def update(self):
        if pygame.time.get_ticks() - self.last_obstacle_time > 500:
            self.last_obstacle_time = pygame.time.get_ticks()
            self.add_obstacle()

        self.obstacles.update()

        # We only need to call the update method of the group, and it will call
        # the update method of all sprites But, we have to make sure to add all
        # of the sprites to the group, so they are updated.
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(self.settings.colors["black"])
        self.obstacles.draw(self.screen)
        # The sprite group has a draw method that will draw all of the sprites in
        # the group.
        self.all_sprites.draw(self.screen)
        score_text = Settings.font.render(f"Score: {self.obstacle_count}", True, Settings.white)
        self.screen.blit(score_text, (240, 10))
        pygame.draw.rect(self.screen, Settings.green, (20, 20, self.energy, 20))
        pygame.display.update()
        
    
        pygame.display.flip()

    def run(self):
        """Main Loop for the game."""
        settings = Settings()

        game = Game(settings)
        spaceship = AlienSpaceship(
        settings, position=(settings.width//2 , settings.height// 2)
        )
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.settings.fps)
    def add_obstacle(self):
        # random.random() returns a random float between 0 and 1, so a value
        # of 0.25 means that there is a 25% chance of adding an obstacle. Since
        # add_obstacle() is called every 100ms, this means that on average, an
        # obstacle will be added every 400ms.
        # The combination of the randomness and the time allows for random
        # obstacles, but not too close together. 
        
        if random.random() < 0.25 :
            obstacle = Obstacle()
            self.obstacles.add(obstacle)
            return 1
        return 0 

        pygame.quit()
        


if __name__ == "__main__":

    
    
    settings = Settings()

    game = Game(settings)
    spaceship = AlienSpaceship(
    settings, position=(settings.width//2 , settings.height// 2)
        )

    game.add(spaceship)
    game.add_obstacle()
    game.run()
