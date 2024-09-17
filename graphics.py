# import pygame
# import sys
# import random
#
# # Initialize Pygame
# pygame.init()
#
# # Set up display
# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Simple Shooting Game")
#
# # Colors
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
#
# # Player settings
# player_width, player_height = 50, 50
# player_x, player_y = (WIDTH - player_width) // 2, HEIGHT - player_height - 50
# player_speed = 5
#
# # Bullet settings
# bullet_width, bullet_height = 10, 20
# bullet_speed = 10
# bullets = []
#
# # Target settings
# target_width, target_height = 50, 50
# target_speed = 3
# targets = []
#
# # Score
# score = 0
# font = pygame.font.Font(None, 36)
#
# # Game loop
# running = True
# while running:
#     # Event handling
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE:
#                 bullet_x = player_x + (player_width - bullet_width) // 2
#                 bullet_y = player_y
#                 bullets.append([bullet_x, bullet_y])
#
#     # Key input
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_LEFT]:
#         player_x -= player_speed
#     if keys[pygame.K_RIGHT]:
#         player_x += player_speed
#
#     # Boundaries for player
#     if player_x < 0:
#         player_x = 0
#     elif player_x > WIDTH - player_width:
#         player_x = WIDTH - player_width
#
#     # Move bullets
#     for bullet in bullets:
#         bullet[1] -= bullet_speed
#
#     # Remove bullets that have gone off screen
#     bullets = [bullet for bullet in bullets if bullet[1] > 0]
#
#     # Spawn targets
#     if random.randint(1, 100) == 1:
#         target_x = random.randint(0, WIDTH - target_width)
#         targets.append([target_x, 0])
#
#     # Move targets
#     for target in targets:
#         target[1] += target_speed
#
#     # Remove targets that have gone off screen
#     targets = [target for target in targets if target[1] < HEIGHT]
#
#     # Check for bullet-target collisions
#     for bullet in bullets:
#         for target in targets:
#             if (bullet[0] < target[0] + target_width and
#                 bullet[0] + bullet_width > target[0] and
#                 bullet[1] < target[1] + target_height and
#                 bullet[1] + bullet_height > target[1]):
#                 targets.remove(target)
#                 bullets.remove(bullet)
#                 score += 1
#
#     # Check for target-player collisions
#     for target in targets:
#         if (player_x < target[0] + target_width and
#             player_x + player_width > target[0] and
#             player_y < target[1] + target_height and
#             player_y + player_height > target[1]):
#             running = False  # Game over if collision occurs
#
#     # Fill the background
#     screen.fill(WHITE)
#
#     # Draw player
#     pygame.draw.rect(screen, BLACK, (player_x, player_y, player_width, player_height))
#
#     # Draw bullets
#     for bullet in bullets:
#         pygame.draw.rect(screen, BLACK, (bullet[0], bullet[1], bullet_width, bullet_height))
#
#     # Draw targets
#     for target in targets:
#         pygame.draw.rect(screen, RED, (target[0], target[1], target_width, target_height))
#
#     # Draw score
#     text = font.render("Score: " + str(score), True, BLACK)
#     screen.blit(text, (10, 10))
#
#     # Update display
#     pygame.display.flip()
#
#     # Cap the frame rate
#     pygame.time.Clock().tick(60)
#
# # Quit Pygame
# pygame.quit()
# sys.exit()

import pygame
import random

# Game settings
screen_width = 800
screen_height = 600
background_color = (255, 255, 255)

# Game objects
circle_x = random.randint(0, screen_width)
circle_y = random.randint(0, screen_height)
circle_radius = 20
circle_color = (0, 0, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mouse Interactive Game")

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Detect left mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Check if mouse clicked on circle
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (mouse_x - circle_x)**2 + (mouse_y - circle_y)**2 <= circle_radius**2:
                    # Move circle to a new random position
                    circle_x = random.randint(0, screen_width)
                    circle_y = random.randint(0, screen_height)

    # Clear screen
    screen.fill(background_color)

    # Draw circle
    pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()