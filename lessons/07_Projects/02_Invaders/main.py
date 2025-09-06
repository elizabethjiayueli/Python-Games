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

class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(assets/'bomb.png')
        self.image = pygame.transform.scale(self.original_image, (Settings.width, Settings.height))
        self.rect = self.image.get_rect()

    

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
        
        super().update()
    
class Game:
    def __init__(self):
        self.player = Player(self)
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.projectiles = pygame.sprite.Group()
        self.full_background = self.make_tiled_bg(Settings.screen, assets/'space.png')
    
    def make_tiled_bg(self, screen, background):
        # Scale background to match the screen height
        
        bg_tile = pygame.image.load(background).convert()
        
        background_height = Settings.screen.get_height()
        bg_tile = pygame.transform.scale(bg_tile, (bg_tile.get_width(), Settings.screen.get_height()))
        # Get the dimensions of the background after scaling
        background_width = bg_tile.get_width()
        return bg_tile
    

     
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip() 

        
    

    
    clock.tick(Settings.FPS)