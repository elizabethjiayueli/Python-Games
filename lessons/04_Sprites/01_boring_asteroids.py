import pygame
import math
from pathlib import Path


assets = Path(__file__).parent / "images"
# Settings class to store game configuration
class Settings:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.fps = 60
        self.triangle_size = 20
        self.projectile_speed = 5
        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0)
        }
# Spaceship class to handle player movement and drawing
class Spaceship(pygame.sprite.Sprite):
    """Class representing the spaceship."""

    def __init__(self, settings):
        super().__init__()

        ...

        self.angle = 0
        self.original_image = self.create_spaceship_image()

        # For Sprites, the image and rect attributes are part of the Sprite class
        # and are important. The image is the surface that will be drawn on the screen
        self.settings = settings
        self.image = self.original_image
        self.position = pygame.Vector2(self.settings.width // 2, self.settings.height // 2)
        self.rect = self.image.get_rect(center=self.position)
        
        
        self.angle = 0
        # self.point = self.position + 
        self.vel = pygame.math.Vector2(0, 2)
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle -= 5
        if keys[pygame.K_RIGHT]:
            self.angle += 5
        if keys[pygame.K_UP]:
            self.position -= self.vel.rotate(self.angle)
        if keys[pygame.K_DOWN]:
            self.position += self.vel.rotate(self.angle)
    def draw(self, surface):
        points = [
            pygame.Vector2(0, -self.settings.triangle_size),  # top point
            pygame.Vector2(-self.settings.triangle_size / 2, self.settings.triangle_size),  # left side point
            pygame.Vector2(self.settings.triangle_size / 2, self.settings.triangle_size)  # right side point
        ]
        rotated_points = [point.rotate(self.angle) + self.position for point in points]
        pygame.draw.polygon(surface, self.settings.colors['white'], rotated_points)

# Projectile class to handle projectile movement and drawing
class Projectile:
    def __init__(self, position, angle, settings):
        self.position = position.copy()
        self.direction = pygame.Vector2(0, -1).rotate(angle)
        self.settings = settings

    def move(self):
        self.position += self.direction * self.settings.projectile_speed

    def draw(self, surface):
        pygame.draw.circle(surface, self.settings.colors['red'], (int(self.position.x), int(self.position.y)), 5)
class AlienSpaceship(Spaceship):
    
    def create_spaceship_image(self):
        """Creates the spaceship shape as a surface."""
        
        return pygame.image.load(assets/'alien2.gif')
# Game class to manage the game loop and objects
class Game:
    """Class to manage the game loop and objects."""

    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        pygame.display.set_caption("Really Boring Asteroids")
        self.clock = pygame.time.Clock()
        self.running = True
        self.spaceship = AlienSpaceship(self.settings)
        self.projectiles = []
    def add(self, sprite):

        self.all_sprites.add(sprite)

    ...

 
        

        
    
        

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Create and fire a projectile
                    new_projectile = Projectile(self.spaceship.position, self.spaceship.angle, self.settings)
                    self.projectiles.append(new_projectile)

    def update(self):
        # Update spaceship
        self.spaceship.handle_input()
        self.all_sprites.update()
        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile.move()
            if not (0 <= projectile.position.x <= self.settings.width) or not (0 <= projectile.position.y <= self.settings.height):
                self.projectiles.remove(projectile)

    def draw(self):
        self.screen.fill(self.settings.colors['black'])
        self.spaceship.draw(self.screen)
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        pygame.display.flip()
        self.all_sprites.draw(self.screen)
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.settings.fps)
        pygame.quit()

# Start the game
if __name__ == "__main__":
    game = Game()
    game.run()
