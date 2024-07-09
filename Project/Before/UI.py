import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the screen object
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the window
pygame.display.set_caption('Simple Pygame Example')

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define the square's properties
square_size = 50
square_x = screen_width // 2
square_y = screen_height // 2
square_speed = 5

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current state of the keyboard
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        square_x -= square_speed
    if keys[pygame.K_RIGHT]:
        square_x += square_speed
    if keys[pygame.K_UP]:
        square_y -= square_speed
    if keys[pygame.K_DOWN]:
        square_y += square_speed

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the red square
    pygame.draw.rect(screen, RED, (square_x, square_y, square_size, square_size))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
