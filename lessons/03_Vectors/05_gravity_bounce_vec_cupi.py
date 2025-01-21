"""
Gravity bounce using Vectors. 

This version of the Gravity Bounce program uses Pygame's Vector2 class to handle
the player's position and velocity. This makes the code more readable and
understandable, and makes it easier to add more complex features to the game.


"""
import pygame
from dataclasses import dataclass

class Settings:
    """A class to store all settings for the game."""
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    PLAYER_SIZE = 20
    LINE_COLOR = (0, 255, 0)
    PLAYER_COLOR = (0, 0, 255)
    BACKGROUND_COLOR = (255, 255, 255)
    TEXT_COLOR = (0, 0, 0)
    FPS = 30
    ANGLE_CHANGE = 10
    LENGTH_CHANGE = 5
    INITIAL_LENGTH = 100
    FONT_SIZE = 24
clock = pygame.time.Clock()
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption("Player with Direction Vector")
class Colors:
    """Constants for Colors"""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    PLAYER_COLOR = (100, 200, 200)
    BACKGROUND_COLOR = (255, 255, 255)


@dataclass
class GameSettings:
    """Settings for the game"""
    width: int = 500
    height: int = 500
    gravity: float = 0.3
    player_start_x: int = 100
    player_start_y: int = None
    player_v_y: float = 0  # Initial y velocity
    player_v_x: float = 0  # Initial x velocity
    player_width: int = 20
    player_height: int = 20
    player_x_vel= pygame.Vector2(10, 0)
    player_jump_velocity= pygame.Vector2(10,0)
    frame_rate: int = 30
    player_thrust: int = 3


class Game:
    """Main object for the top level of the game. Holds the main loop and other
    update, drawing and collision methods that operate on multiple other
    objects, like the player and obstacles."""
    
    def __init__(self, settings: GameSettings):
        pygame.init()

        self.settings = settings
        self.running = True

        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        self.clock = pygame.time.Clock()

        # Turn Gravity into a vector
        self.gravity = pygame.Vector2(0, self.settings.gravity)

    def run(self):
        """Main game loop"""
        player = Player(self)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False

            player.update()

            self.screen.fill(Colors.BACKGROUND_COLOR)
            player.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.settings.frame_rate)

        pygame.quit()


class Player:
    """Player class, just a bouncing rectangle"""
    
    def __init__(self, game: Game):
        self.game = game
        settings = self.game.settings
        
        self.width = settings.player_width
        self.height = settings.player_height
    
        # Vector for our jump velocity, which is just up
        self.v_jump = pygame.Vector2(10, -15)
        self.moving = False
        # Player position
        self.pos = pygame.Vector2(settings.player_start_x, 
                                  settings.player_start_y if settings.player_start_y is not None else settings.height - self.height)
        self.thrust = pygame.Vector2(2, -settings.player_thrust)
        # Player's velocity
        self.direction_vector = pygame.math.Vector2(Settings.INITIAL_LENGTH+2, 0)  # Initial direction vector
        self.vel = pygame.Vector2(settings.player_v_x, settings.player_v_y)  # Velocity vector



    # Direction functions. IMPORTANT! Using these functions isn't really
    # necessary, but it makes the code more readable. You could just use
    # self.vel.x < 0, but writing "self.going_left()" is a lot easier to read and
    # understand, it makes the code self-documenting. 

    def going_up(self):
        """Check if the player is going up"""
        return self.vel.y < 0
    
    def going_down(self):
        """Check if the player is going down"""
        return self.vel.y > 0
    
    def going_left(self):
        """Check if the player is going left"""
        return self.vel.x < 0
    
    def going_right(self):
        """Check if the player is going right"""
        return self.vel.x > 0
    
    
    # Location Fuctions
    
    def at_top(self):
        """Check if the player is at the top of the screen"""
        return self.pos.y <= 0
    
    def at_bottom(self):
        """Check if the player is at the bottom of the screen"""
        return self.pos.y >= self.game.settings.height - self.height

    def at_left(self):
        """Check if the player is at the left of the screen"""
        return self.pos.x <= 0
    
    def at_right(self):
        """Check if the player is at the right of the screen"""
        return self.pos.x >= self.game.settings.width - self.width
    def move(self):
        # end_position = self.pos + self.direction_vector
        # """Moves the player in the direction of the current angle."""
        # self.pos.x == end_position
        # self.pos.y == end_position
        
        init_position = self.pos # Save the initial position for the animation
        
        # Calculate the final position after moving. Its just addition!
        final_position = self.pos + self.direction_vector
        
        # The rest is just for animation
        length = self.direction_vector.length()
        N = int(length // 3)
        step = (final_position - self.pos) / N
       
        for i in range(N):
            self.pos += step
            screen.fill(Settings.BACKGROUND_COLOR)
            self.draw(show_line=False)
            pygame.draw.line(screen, Settings.LINE_COLOR, init_position, final_position, 2)
            pygame.display.flip()
            clock.tick(Settings.FPS)
        self.moving = False
    # Updates
    
    def update(self):
        """Update player position, continuously jumping"""
        if not self.moving: 
            self.update_jump()
            self.update_v()
            self.update_pos()
            self.update_input()

    def update_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.vel += self.thrust
        if keys[pygame.K_LEFT]:
            
            #self.v_jump += settings.player_jump_velocity
            self.pos -= settings.player_x_vel
        if keys[pygame.K_RIGHT]:
            #self.v_jump -= settings.player_jump_velocity
            self.pos += settings.player_x_vel
        
        key_limit = 0
        key_limit += 1    
        if key_limit%3 == 1: # Limit frequency of key presses so the user can set exact angles
            if keys[pygame.K_d]:
                self.direction_vector = self.direction_vector.rotate(-Settings.ANGLE_CHANGE)
            elif keys[pygame.K_a]: 
                self.direction_vector = self.direction_vector.rotate(Settings.ANGLE_CHANGE)
                
        if keys[pygame.K_w]:
            self.direction_vector.scale_to_length(self.direction_vector.length() + Settings.LENGTH_CHANGE)
        elif keys[pygame.K_s]:
            self.direction_vector.scale_to_length(self.direction_vector.length() - Settings.LENGTH_CHANGE)
        elif keys[pygame.K_RETURN]:
            self.move()
            # self.moving = True
            
            
    def update_v(self):
        """Update the player's velocity based on gravity and bounce on edges"""
        
        self.vel += self.game.gravity  # Add gravity to the velocity

        if self.at_bottom() and self.going_down():
            self.vel.y = 0

        if self.at_top() and self.going_up():
            self.vel.y = -self.vel.y # Bounce off the top. 
        
        # If the player hits one side of the screen or the other, bounce the
        # player. we are also checking if the player has a velocity going farther
        # off the screeen, because we don't want to bounce the player if it's
        # already going away from the edge
        
        if (self.at_left() and self.going_left() ) or ( self.at_right() and self.going_right()):
            self.vel.x = -self.vel.x
            
    def update_pos(self):
        """Update the player's position based on velocity"""
        drag = -self.vel *0.0474
        self.pos += self.vel + drag # Update the player's position based on the current velocity
        
        # If the player is at the bottom, stop the player from falling and
        # stop the jump
        
        if self.at_bottom():
            self.pos.y = self.game.settings.height - self.height

        if self.at_top():
            self.pos.y = 0

        # Don't let the player go off the left side of the screen
        if self.at_left():
            self.pos.x = 0
  
        # Don't let the player go off the right side of the screen
        elif self.at_right():
            self.pos.x = self.game.settings.width - self.width

    def update_jump(self):
        """Handle the player's jumping logic"""
        
        # Notice that we've gotten rid of self.is_jumping, because we can just
        # check if the player is at the bottom. 
        #if self.at_bottom():
            #self.vel += self.v_jump
         
        
        # self.pos = pygame.math.Vector2(settings.player_start_x, 
        #                           settings.player_start_y if settings.player_start_y is not None else settings.height - self.height)
        

    def draw(self, show_line=True):
        """Draws the player and the direction vector on the screen."""
        #pygame.draw.rect(screen, Settings.PLAYER_COLOR, (self.position.x - Settings.PLAYER_SIZE // 2, self.position.y - Settings.PLAYER_SIZE // 2, Settings.PLAYER_SIZE, Settings.PLAYER_SIZE))
        
        # The end position of the direction vector is the player's position plus the direction vector
        self_center = pygame.math.Vector2(self.pos.x + self.width/2, self.pos.y + self.height/2)
        end_position = self_center + self.direction_vector
        if show_line:
            pygame.draw.line(screen, Settings.LINE_COLOR, self_center, end_position, 3)

        pygame.draw.rect(screen, Colors.PLAYER_COLOR, (self.pos.x, self.pos.y, self.width, self.height))
        #pygame.draw.line(screen, Settings.LINE_COLOR, self.position, end_position, 2)

settings = GameSettings()
game = Game(settings)
game.run()
