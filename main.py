"""
A Quick Ride
Author: Justin Spanos
Date: September 21, 2023
Copyright (c) 2023 Justin Spanos
License: MIT License
"""

import pygame  # Import the Pygame library for game development
import sys     # Import the sys module for system-related functionality
import random
import math

pygame.init()

# Initialize the best score of all time
try:
    with open("best_score.txt", "r") as file:
        best_score_all_time = int(file.read())
except FileNotFoundError:
    best_score_all_time = 0

# Initialize the best percentage of all time
try:
    with open("best_percentage.txt", "r") as file:
        best_percentage_all_time = float(file.read())
except FileNotFoundError:
    best_percentage_all_time = 0.0

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
COIN_SPEED = 3
COIN_SPAWN_RATE = 100  # Adjust this for the frequency of coins
MAX_MISSED_COINS = 5  # Maximum number of missed coins before game over
NIGHT_COLOR = (0, 0, 255, 100)  # Dark color for night effect (RGBA format)
HEADLIGHT_RADIUS = 200  # Radius of the headlight effect

# Initialize the best score of all time
best_score_all_time = 0
best_percentage_all_time = 0.0  # Initialize the best percentage of all time

# Define fonts
font = pygame.font.Font(None, 36)  # Font for displaying the score
blue_font = pygame.font.Font(None, 24)  # Font for displaying missed coins count in blue
game_over_font = pygame.font.Font(None, 48)  # Font for the game over text

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("A Quick Ride")

# Load the track background image
original_background_image = pygame.image.load("track.png")  # Replace "track.png" with your track image file
background_image = pygame.transform.scale(original_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_rect = background_image.get_rect()

# Load and resize the car image
original_player_image = pygame.image.load("car.png")  # Replace "car.png" with your car image file
player_image = pygame.transform.scale(original_player_image, (60, 100))  # Resize the car image
player_rect = player_image.get_rect()
player_rect.centerx = SCREEN_WIDTH // 2
player_rect.centery = SCREEN_HEIGHT - 100

# Load and resize the coin image
original_coin_image = pygame.image.load("coin.png")  # Replace "coin.png" with your coin image file
coin_image = pygame.transform.scale(original_coin_image, (40, 40))  # Resize the coin image

# Coins
coins = []

def spawn_coin():
    coin_rect = coin_image.get_rect()
    coin_rect.x = random.randint(100, SCREEN_WIDTH - 100)
    coin_rect.y = -coin_rect.height
    coins.append(coin_rect)

score = 0  # Initialize the score
missed_coins = 0  # Initialize the missed coins count
game_over = False  # Initialize the game over flag


# Load the best score from the file
try:
    with open("best_score.txt", "r") as file:
        best_score = int(file.read())
except FileNotFoundError:
    best_score = 0
    
def check_collision():
    global score, missed_coins, game_over  # Declare 'score', 'missed_coins', and 'game_over' as global variables
    for coin_rect in coins:
        if player_rect.colliderect(coin_rect):
            score += 1  # Increment the score when a collision occurs
            coins.remove(coin_rect)  # Remove the collided coin
            break  # Exit the loop after detecting one collision
    else:
        # Check if the first coin in the list has gone beyond the screen
        if coins and coins[0].y > SCREEN_HEIGHT:
            missed_coins += 1  # Increment the missed coins count
            coins.pop(0)  # Remove the missed coin from the list
            if missed_coins >= MAX_MISSED_COINS:
                game_over = True  # Set the game over flag
    

font = pygame.font.Font(None, 36)  # Font for displaying the score
blue_font = pygame.font.Font(None, 24)  # Font for displaying missed coins count in blue


clock = pygame.time.Clock()

# Load the best percentage of all time from the file
try:
    with open("best_percentage.txt", "r") as file:
        best_percentage_all_time = float(file.read())
except FileNotFoundError:
    best_percentage_all_time = 0.0

# Create a transparent surface for the headlight effect
headlight_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

clock = pygame.time.Clock()

# Inside your game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
        player_rect.x += PLAYER_SPEED

    # Create a transparent surface for the night effect
    night_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    night_color = (15, 0, 255, 135)  # Blue night filter with alpha
    night_surface.fill(night_color)

    # Calculate the position of the headlight effect based on the player's position
    headlight_center = (player_rect.centerx, player_rect.centery - 40)

    # Create a transparent surface for the headlight effect
    headlight_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    # Draw the yellow headlight on the headlight_surface
    headlight_color = (100, 100, 0, 100)  # Yellow headlight with alpha
    pygame.draw.circle(headlight_surface, headlight_color, headlight_center, HEADLIGHT_RADIUS)

    # Blit the background image onto the screen
    screen.blit(background_image, background_rect)

    # Blit the coins and player on the screen
    for coin_rect in coins:
        coin_rect.y += COIN_SPEED
        screen.blit(coin_image, coin_rect)

    # Blit the night surface to apply the blue night filter
    screen.blit(night_surface, (0, 0))

    # Check for collisions
    check_collision()

    # Spawn new coins
    if random.randint(1, COIN_SPAWN_RATE) == 1:
        spawn_coin()

    # Blit the headlight surface to apply the yellow headlight
    screen.blit(headlight_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    screen.blit(player_image, player_rect)

    # Display the score in red letters
    score_text = font.render(f"Score: {score}", True, (255, 0, 0))
    screen.blit(score_text, (10, 10))

    # Display the missed coins count in dark red letters
    missed_text = blue_font.render(f"Missed: {missed_coins}", True, (128, 0, 0))
    screen.blit(missed_text, (10, 50))

    # Display the best score of all time in white letters
    best_all_time_text = blue_font.render(f"High Score: {best_score_all_time}", True, (255, 255, 255))
    screen.blit(best_all_time_text, (630, 10))

    # Calculate the percentage for the current game session
    if missed_coins > 0:
        current_percentage = round((score / (score + missed_coins)) * 100, 1)
    else:
        current_percentage = 100.0

    # Check for a new best percentage
    if current_percentage > best_percentage_all_time:
        best_percentage_all_time = current_percentage
        # Save the new best percentage to the file
        with open("best_percentage.txt", "w") as file:
            file.write(str(best_percentage_all_time))
            
    # Calculate the percentage for the current game session
    if missed_coins > 0:
        current_percentage = round((score / (score + missed_coins)) * 100, 1)
    else:
        current_percentage = 100.0

    # Check for a new best percentage
    if current_percentage > best_percentage_all_time:
        best_percentage_all_time = current_percentage
        # Save the new best percentage to the file
        with open("best_percentage.txt", "w") as file:
            file.write(str(best_percentage_all_time))

    pygame.display.flip()
    clock.tick(60)

# Check if the game is over
if game_over:
    # Save the best score and best percentage back to the file when a new best score is achieved
    if score > best_score:
        with open("best_score.txt", "w") as file:
            file.write(str(score))

    if score > best_score_all_time:
        best_score_all_time = score
        with open("best_percentage.txt", "w") as file:
            file.write(str(best_percentage_all_time))

    # Define the game_over_text here
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))

    # Get the rect for the game over text to center it vertically and horizontally
    game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

    # Define the vertical spacing between text elements
    text_spacing = 60

    # Calculate vertical positions for text elements
    game_over_y = SCREEN_HEIGHT // 2 - 3 * text_spacing
    score_y = game_over_y + text_spacing
    missed_y = score_y + text_spacing
    ratio_y = missed_y + text_spacing
    best_all_time_y = ratio_y + text_spacing
    best_percentage_y = best_all_time_y + text_spacing


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Load the best percentage of all time from the file
        try:
            with open("best_percentage.txt", "r") as file:
                best_percentage_all_time = float(file.read())
        except FileNotFoundError:
            best_percentage_all_time = 0.0

        # Calculate and round the ratio as a percentage for the current game session
        if missed_coins > 0:
            ratio_percentage = round((score / (score + missed_coins)) * 100, 1)
        else:
            ratio_percentage = 100.0

        # Display the best score of all time in white letters (within the game loop)
        best_all_time_text = blue_font.render(f"High Score: {best_score_all_time}", True, (255, 255, 255))
        screen.blit(best_all_time_text, (630, 10))

        
        # Display the best percentage of all time on the game over screen
        best_percentage_text = font.render(f"Best Percentage: {best_percentage_all_time}%", True, (255, 255, 255))
        screen.blit(best_percentage_text, (SCREEN_WIDTH // 2 - best_percentage_text.get_width() // 2, best_percentage_y))

        # Define the ratio_text AKA the percentage
        ratio_text = font.render(f"Percentage: {ratio_percentage}%", True, (255, 255, 0))

        # Clear the screen
        screen.fill((0, 0, 0))

        
        # Blit the game over text and other texts, centering them both vertically and horizontally
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, game_over_y))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, score_y))
        screen.blit(missed_text, (SCREEN_WIDTH // 2 - missed_text.get_width() // 2, missed_y))
        screen.blit(ratio_text, (SCREEN_WIDTH // 2 - ratio_text.get_width() // 2, ratio_y))
        screen.blit(best_all_time_text, (SCREEN_WIDTH // 2 - best_all_time_text.get_width() // 2, best_all_time_y))
        screen.blit(best_percentage_text, (SCREEN_WIDTH // 2 - best_percentage_text.get_width() // 2, best_percentage_y))

        pygame.display.flip()
