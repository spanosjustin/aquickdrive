import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
COIN_SPEED = 3
COIN_SPAWN_RATE = 100
MAX_MISSED_COINS = 5
NIGHT_COLOR = (0, 0, 255, 100)
HEADLIGHT_RADIUS = 200

# Initialize best score and best percentage
best_score_all_time = 0
best_percentage_all_time = 0.0

# Initialize Pygame fonts
font = pygame.font.Font(None, 36)
blue_font = pygame.font.Font(None, 24)
game_over_font = pygame.font.Font(None, 48)

# Create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("A Quick Ride")

# Load images
background_image = pygame.image.load("track.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
player_image = pygame.transform.scale(pygame.image.load("car.png"), (60, 100))
coin_image = pygame.transform.scale(pygame.image.load("coin.png"), (40, 40))
# Load the snowflake image
snowflake_image = pygame.image.load("snowflake.png")
snowflake_image = pygame.transform.scale(snowflake_image, (20, 20))  # Adjust the size as needed

# Load the retry button image and scale it
retry_button_image = pygame.transform.scale(pygame.image.load("retry_button.png"), (100, 50))

# Get the rect of the retry button for collision detection
retry_button_rect = retry_button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140))


# Initialize player and coin lists
player_rect = player_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
coins = []
# Create a list to store snowflake positions
snowflakes = []

# Load best score from file
try:
    with open("best_score.txt", "r") as file:
        best_score_all_time = int(file.read())
except FileNotFoundError:
    best_score_all_time = 0

# Load best percentage from file
try:
    with open("best_percentage.txt", "r") as file:
        best_percentage_all_time = float(file.read())
except FileNotFoundError:
    best_percentage_all_time = 0.0

# Function to spawn a coin
def spawn_coin():
    coin_rect = coin_image.get_rect()
    coin_rect.x = random.randint(100, SCREEN_WIDTH - 100)
    coin_rect.y = -coin_rect.height
    coins.append(coin_rect)

# Function to check collisions
def check_collision():
    global score, missed_coins, game_over
    for coin_rect in coins:
        if player_rect.colliderect(coin_rect):
            score += 1
            coins.remove(coin_rect)
            break
    else:
        if coins and coins[0].y > SCREEN_HEIGHT:
            missed_coins += 1
            coins.pop(0)
            if missed_coins >= MAX_MISSED_COINS:
                game_over = True

# Function to spawn snowflakes
def spawn_snowflake():
    snowflake_rect = snowflake_image.get_rect()
    snowflake_rect.x = random.randint(0, SCREEN_WIDTH)
    snowflake_rect.y = -snowflake_rect.height
    snowflakes.append(snowflake_rect)

# Initialize game variables
score = 0
missed_coins = 0
game_over = False

# Initialize current_percentage
current_percentage = 0.0

# Define the ratio_text AKA the percentage here
ratio_text = font.render(f"Percentage: 0.0%", True, (255, 255, 0))

# Create a transparent surface for the headlight effect
headlight_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

# Initialize a flag to control the game loop
running = True


# Main game loop
while running:
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
    night_color = (15, 0, 255, 135)
    night_surface.fill(night_color)

    # Calculate the position of the headlight effect based on the player's position
    headlight_center = (player_rect.centerx, player_rect.centery - 600)

    # Create a transparent surface for the headlight effect
    headlight_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    # Draw the triangular headlight on the headlight_surface
    headlight_color = (100, 100, 0, 100)
    headlight_points = [
        (headlight_center[0], headlight_center[1] + 600),  # Tip of the triangle
        (headlight_center[0] - 200, headlight_center[1] + 80),  # Left point
        (headlight_center[0] + 200, headlight_center[1] + 80)  # Right point
    ]
    pygame.draw.polygon(headlight_surface, headlight_color, headlight_points)

    # In your main loop, after checking for collisions, spawn new snowflakes
    if random.randint(1, 20) == 1:  # Adjust the spawn rate as needed
        spawn_snowflake()

    # Blit the background image onto the screen
    screen.blit(background_image, (0, 0))

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

    # Inside your main loop
    for snowflake_rect in snowflakes:
        snowflake_rect.y += 2  # Adjust the speed of falling snowflakes
        screen.blit(snowflake_image, snowflake_rect)

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

    pygame.display.flip()

    # Limit the frame rate
    pygame.time.delay(10)

    # Check if the game is over
    if missed_coins >= MAX_MISSED_COINS:
        game_over = True

    if game_over:
        # Save the best score and best percentage back to the file when a new best score is achieved
        if score > best_score_all_time:
            best_score_all_time = score
            with open("best_score.txt", "w") as file:
                file.write(str(best_score_all_time))

            # Update the best_all_time_text when there's a new high score
            best_all_time_text = blue_font.render(f"High Score: {best_score_all_time}", True, (255, 255, 255))

        # Calculate the percentage for the current game session
        if score + missed_coins > 0:
            current_percentage = round((score / (score + missed_coins)) * 100, 1)
        else:
            current_percentage = 0.0

        # Check for a new best percentage
        if current_percentage > best_percentage_all_time:
            best_percentage_all_time = current_percentage
            # Save the new best percentage to the file
            with open("best_percentage.txt", "w") as file:
                file.write(str(best_percentage_all_time))
                
       # Define the game_over_text here
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))

        # Get the rect for the game over text to center it vertically and horizontally
        game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

        # Define the vertical spacing between text elements
        text_spacing = 40

        # Calculate vertical positions for text elements
        game_over_y = SCREEN_HEIGHT // 2 - 3 * text_spacing
        score_y = game_over_y + text_spacing
        missed_y = score_y + text_spacing
        ratio_y = missed_y + text_spacing
        best_all_time_y = ratio_y + text_spacing
        best_percentage_y = best_all_time_y + text_spacing

        # Calculate the center position for horizontal alignment
        text_center_x = SCREEN_WIDTH // 2

        # Center-align text elements
        game_over_text_rect.center = (text_center_x, game_over_y)
        score_text_rect = score_text.get_rect(center=(text_center_x, score_y))
        missed_text_rect = missed_text.get_rect(center=(text_center_x, missed_y))
        ratio_text_rect = ratio_text.get_rect(center=(text_center_x, ratio_y))
        best_all_time_text_rect = best_all_time_text.get_rect(center=(text_center_x, best_all_time_y))

        # Display the game over screen elements
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if retry_button_rect.collidepoint(mouse_pos):
                        # Reset the game by reinitializing the game variables
                        score = 0
                        missed_coins = 0
                        game_over = False
                        player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
                        coins = []
                        snowflakes = []

                    else:
                        # User wants to quit the game entirely
                        running = False
                        game_over = False

            # Calculate the current_percentage
            if score + missed_coins > 0:
                current_percentage = round((score / (score + missed_coins)) * 100, 1)
            else:
                current_percentage = 100.0

            # Clear the screen
            screen.fill((0, 0, 0))

            # Display game over text
            screen.blit(game_over_text, game_over_text_rect)

            # Display score, missed coins, best percentage, best score, and the retry button
            screen.blit(score_text, score_text_rect)
            screen.blit(missed_text, missed_text_rect)
            screen.blit(ratio_text, ratio_text_rect)
            screen.blit(best_all_time_text, best_all_time_text_rect)

            # Define best_percentage_text here
            best_percentage_text = blue_font.render(f"Best Percentage: {best_percentage_all_time}%", True, (255, 255, 255))

            # Calculate the position for best_percentage_text_rect
            best_percentage_text_rect = best_percentage_text.get_rect(center=(text_center_x, best_percentage_y))

            # Display best_percentage_text
            screen.blit(best_percentage_text, best_percentage_text_rect)

            # Blit the retry button image
            screen.blit(retry_button_image, retry_button_rect)

            pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
