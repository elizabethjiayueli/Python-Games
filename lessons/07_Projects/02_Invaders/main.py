import pygame
import random
import time
import math
# Initialize Pygame
pygame.init()
from pathlib import Path
assets = Path(__file__).parent / 'images'
background = pygame.image.load(assets/'space.png')



clock = pygame.time.Clock()



class Settings:
    # Screen
    screen_width = 288
    screen_height = 420
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('SPACE INVADERS')  
    FPS = 30
    red = (255, 8, 0)

    projectile_speed = 10
    shoot_delay = 250  # 250 milliseconds between shots, or 4 shots per second   
    width, height = 48, 56
    WIDTH, HEIGHT = 600, 300
    PLAYER_SIZE = 25
    position = (100, 1000)

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.original_image = pygame.image.load(assets/'rocket.png')
        self.settings = Settings
        self.game = game
        self.image = pygame.transform.scale(self.original_image, (Settings.width, Settings.height))
        self.rect = self.image.get_rect(center = Settings.position)
        self.rect.x = 50
        self.rect.y = Settings.HEIGHT - Settings.PLAYER_SIZE -7
        print(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        self.rect = self.image.get_rect()
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = Settings.shoot_delay  
        self.rect.y +=350

    
    def ready_to_shoot(self):
        """Checks if the spaceship is ready to shoot again."""
        if pygame.time.get_ticks() - self.last_shot > self.shoot_delay:
            self.last_shot = pygame.time.get_ticks()
            return True
        return False
            

    def fire_projectile(self):
        """Creates and fires a projectile."""
        print("firing projectile")
        new_projectile = Projectile(
            position=self.rect.midtop,
            velocity=self.settings.projectile_speed,
        )

        # Important! The game will update all of the sprites in the group, so we
        # need to add the projectile to the group to make sure it is updated.
        game.projectiles.add(new_projectile)
        #game.add(new_projectile)
    def update(self): 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5
        if keys[pygame.K_SPACE] and self.ready_to_shoot():
            self.fire_projectile()
        if self.rect.topleft[0] <= 0:
            self.rect.x = 0
        if self.rect.topright[0] >= 288:
            self.rect.x = 240
        if self.rect.y <= 0:
            self.rect.y= 0
        if self.rect.bottom >= 420:
            self.rect.bottom= 420

        super().update()
            
            
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(assets/'alien.png')
        self.image = pygame.transform.scale(self.original_image, (Settings.width, Settings.height))
        self.rect = self.image.get_rect()
class Bomb(pygame.sprite.Sprite):
    def __init__(self, position, velocity=Settings.projectile_speed/2):
        super().__init__()
        self.original_image = pygame.image.load(assets/'bomb.gif')
        self.image = pygame.transform.scale(self.original_image, (10, 15))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.velocity = pygame.Vector2(0, 1)  * velocity
        self.explosion = pygame.image.load(assets / "explosion1.gif")
    def explode(self):
        """Replace the image with an explosition image."""
        
        # Load the explosion image
        self.image = self.explosion
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.x_vel = 0
        self.y_vel = 0
        print("exploded")
    def update(self):
        self.rect.center += self.velocity
        if self.rect.y >= Settings.screen_height:
            self.kill()
            print("bomb killed")
        
        super().update()
def add_obstacle(obstacles):
    # random.random() returns a random float between 0 and 1, so a value
    # of 0.25 means that there is a 25% chance of adding an obstacle. Since
    # add_obstacle() is called every 100ms, this means that on average, an
    # obstacle will be added every 400ms.
    # The combination of the randomness and the time allows for random
    # obstacles, but not too close together. 
    key = pygame.key.get_pressed()
    if key[pygame.K_b]:
        bomb = Bomb(
            position=(100, 100)
        )
        print("bomb released")
        game.bombs.add(bomb)
        return 1
    return 0

    

class Projectile(pygame.sprite.Sprite):
    def __init__(self, position, velocity):
        super().__init__()
        self.original_image = pygame.image.load(assets/'projectile.png')
        self.image = pygame.transform.scale(self.original_image, (10, 15))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.velocity = pygame.Vector2(0, -1)  * velocity
        
    def update(self):
        self.rect.center += self.velocity
        if self.rect.center[1] <= 0 or self.rect.y >= Settings.screen_height:
            self.kill()
            print("projectile killed")
        
        super().update()
    
class Game:
    def __init__(self):
        #sprite groups
        self.player = Player(self)
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.projectiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        

        #health
        self.health = 3
        self.health_bars = None

        #background
        self.full_background = self.make_tiled_bg(Settings.screen, assets/'space.png')
        pygame.draw.rect(Settings.screen, Settings.red, self.player.rect)
        #pygame.draw.rect(Settings.screen, Settings.red, self.bombs.rect)
    def make_tiled_bg(self, screen, background):
        # Scale background to match the screen height
        bg_tile = pygame.image.load(background).convert()
        background_height = Settings.screen.get_height()
        bg_tile = pygame.transform.scale(bg_tile, (bg_tile.get_width(), Settings.screen.get_height()))
        # Get the dimensions of the background after scaling
        background_width = bg_tile.get_width()
        return bg_tile
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            collider = pygame.sprite.spritecollide(self.player, self.bombs, False)
            if collider:
                collider[0].explode()
                print("hit by bomb")
        
game = Game()

running = False
run = True
running = True
while running:
    Settings.screen.blit(game.full_background, (0,0))
    game.player_group.update()
    game.player_group.draw(Settings.screen)
    game.projectiles.update()
    game.projectiles.draw(Settings.screen)
    game.enemies.update()
    game.enemies.draw(Settings.screen)
    add_obstacle(game.bombs)
    game.bombs.update()
    game.bombs.draw(Settings.screen)
    game.handle_events()
    health_1 = pygame.draw.circle(Settings.screen, Settings.red, (129, 410), 5)
    health_2 = pygame.draw.circle(Settings.screen, Settings.red, (144, 410), 5)
    health_3 = pygame.draw.circle(Settings.screen, Settings.red, (159, 410), 5)
    game.health_bars = [health_1, health_2, health_3]
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip() 

        
    

    
    clock.tick(Settings.FPS)