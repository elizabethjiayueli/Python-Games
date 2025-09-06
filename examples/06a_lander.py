# From https://gist.github.com/HaileyStorm/956a9525eaf6ac2586f579c874c9d2be

import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Lunar Lander")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define game objects
lander_width, lander_height = 50, 50
lander_speed = 0
lander_acceleration = 0.1
fuel = 100
fuel_consumption = 0.2
lander_speed_x = 0

fuel_cell_width, fuel_cell_height = 30, 30
fuel_cells = []

landing_pad_width, landing_pad_height = 100, 20
landing_pad_speed = 1

# Game statistics
score = 0
high_score = 0
wins = 0
losses = 0

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Reset game state
    lander = pygame.Rect(width // 2 - lander_width // 2, 50, lander_width, lander_height)
    lander_speed = 0
    lander_speed_x = 0
    fuel = 100
    fuel_cells = []
    landing_pad = pygame.Rect(width // 2 - landing_pad_width // 2, height - 70, landing_pad_width, landing_pad_height)
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and fuel > 0:
            lander_speed -= lander_acceleration
            fuel -= fuel_consumption
        if keys[pygame.K_LEFT]:
            lander_speed_x -= 0.1
        if keys[pygame.K_RIGHT]:
            lander_speed_x += 0.1

        # Update lander position
        lander.y += lander_speed
        lander.x += lander_speed_x
        lander_speed += 0.05  # Gravity

        # Keep the lander within the screen boundaries
        if lander.left < 0:
            lander.left = 0
            lander_speed_x = 0
        elif lander.right > width:
            lander.right = width
            lander_speed_x = 0

        # Spawn fuel cells randomly
        if random.randint(1, 50) == 1:
            fuel_cell = pygame.Rect(random.randint(0, width - fuel_cell_width), 0, fuel_cell_width, fuel_cell_height)
            fuel_cells.append(fuel_cell)

        # Update fuel cell positions
        for cell in fuel_cells:
            cell.y += 2
            if lander.colliderect(cell):
                fuel_cells.remove(cell)
                fuel += 10
                score += 10
            elif cell.top > height:
                fuel_cells.remove(cell)

        # Move the landing pad
        landing_pad.x += landing_pad_speed
        if landing_pad.left < 0 or landing_pad.right > width:
            landing_pad_speed *= -1

        # Check for collision with the landing pad
        if lander.colliderect(landing_pad):
            if lander_speed < 2:
                print("Congratulations! You landed safely.")
                wins += 1
                score += 100
            else:
                print("Oops! You landed too hard.")
                losses += 1
            game_over = True
        elif lander.bottom >= height:
            print("Game Over! You crashed.")
            losses += 1
            game_over = True

        # Update high score
        high_score = max(high_score, score)

        # Draw game objects
        window.fill(BLACK)
        pygame.draw.rect(window, WHITE, lander)
        for cell in fuel_cells:
            pygame.draw.rect(window, GREEN, cell)
        pygame.draw.rect(window, BLUE, landing_pad)
        pygame.draw.rect(window, RED, (0, height - 50, width, 50))  # Ground

        # Draw fuel bar
        pygame.draw.rect(window, GREEN, (10, 10, fuel, 20))

        # Draw score and high score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        window.blit(score_text, (10, 40))
        window.blit(high_score_text, (10, 80))

        pygame.display.flip()
        clock.tick(60)

    # Display win/lose stats and wait for key press to start next game
    font = pygame.font.Font(None, 48)
    wins_text = font.render(f"Wins: {wins}", True, GREEN)
    losses_text = font.render(f"Losses: {losses}", True, RED)
    window.blit(wins_text, (width // 2 - wins_text.get_width() // 2, height // 2 - 50))
    window.blit(losses_text, (width // 2 - losses_text.get_width() // 2, height // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting = False
            elif event.type == pygame.KEYDOWN:
                score = 0
                waiting = False

pygame.quit()