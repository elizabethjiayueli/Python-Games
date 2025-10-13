import pygame
import random
import time
import math
# Initialize Pygame
pygame.init()
from pathlib import Path
assets = Path(__file__).parent / 'images'
background = pygame.image.load(assets/'frogger_road_bg.png')

clock = pygame.time.Clock()

class Settings: 
    # Screen
    screen_width = 288
    screen_height = 420
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('FROGGER')  
    FPS = 30
    obstacle_speed = 10
    width, height = 48, 56
    WIDTH, HEIGHT = 600, 300
    PLAYER_SIZE = 25
    position = (100, 1000)


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        pass

class Car(pygame.sprite.Sprite):
    def __init__(self, game, direction):
        super().__init__()
        pass

class Log(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        pass

class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.logs = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.create_obstacles()

    def create_obstacles(self):
        # Create cars and logs and add them to their respective groups
        pass